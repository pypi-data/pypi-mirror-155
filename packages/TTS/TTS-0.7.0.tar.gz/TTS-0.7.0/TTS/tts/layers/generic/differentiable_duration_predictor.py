# adopted from https://github.com/keonlee9420/Parallel-Tacotron2

import numpy as np
import torch
import torch.nn.functional as F
from torch import nn

from TTS.tts.utils.helpers import sequence_mask

from ..generic.normalization import LayerNorm


class DurationPredictor(nn.Module):
    """Glow-TTS duration prediction model.

    ::

        [2 x (conv1d_kxk -> relu -> layer_norm -> dropout)] -> conv1d_1x1 -> durs

    Args:
        in_channels (int): Number of channels of the input tensor.
        hidden_channels (int): Number of hidden channels of the network.
        kernel_size (int): Kernel size for the conv layers.
        dropout_p (float): Dropout rate used after each conv layer.
    """

    def __init__(self, in_channels, hidden_channels, kernel_size, dropout_p, cond_channels=None, language_emb_dim=None):
        super().__init__()

        # add language embedding dim in the input
        if language_emb_dim:
            in_channels += language_emb_dim

        # class arguments
        self.in_channels = in_channels
        self.filter_channels = hidden_channels
        self.kernel_size = kernel_size
        self.dropout_p = dropout_p
        # layers
        self.drop = nn.Dropout(dropout_p)
        self.conv_1 = nn.Conv1d(in_channels, hidden_channels, kernel_size, padding=kernel_size // 2)
        self.norm_1 = LayerNorm(hidden_channels)
        self.conv_2 = nn.Conv1d(hidden_channels, hidden_channels, kernel_size, padding=kernel_size // 2)
        self.norm_2 = LayerNorm(hidden_channels)
        # output layer
        self.proj = nn.Conv1d(hidden_channels, 1, 1)
        if cond_channels is not None and cond_channels != 0:
            self.cond = nn.Conv1d(cond_channels, in_channels, 1)

        if language_emb_dim != 0 and language_emb_dim is not None:
            self.cond_lang = nn.Conv1d(language_emb_dim, in_channels, 1)

    def forward(self, x, x_mask, g=None, lang_emb=None):
        """
        Shapes:
            - x: :math:`[B, C, T]`
            - x_mask: :math:`[B, 1, T]`
            - g: :math:`[B, C, 1]`
        """
        if g is not None:
            x = x + self.cond(g)

        if lang_emb is not None:
            x = x + self.cond_lang(lang_emb)

        x = self.conv_1(x * x_mask)
        x = torch.relu(x)
        x = self.norm_1(x)
        x = self.drop(x)
        x = self.conv_2(x * x_mask)
        x = torch.relu(x)
        x = self.norm_2(x)
        v = self.drop(x)
        x = self.proj(v * x_mask)
        x = F.softplus(x)
        return x * x_mask, v * x_mask


class LinearNorm(nn.Module):
    """LinearNorm Projection"""

    def __init__(self, in_features, out_features, bias=False):
        super(LinearNorm, self).__init__()
        self.linear = nn.Linear(in_features, out_features, bias)

        nn.init.xavier_uniform_(self.linear.weight)
        if bias:
            nn.init.constant_(self.linear.bias, 0.0)

    def forward(self, x):
        x = self.linear(x)
        return x


class SwishBlock(nn.Module):
    """Swish Block"""

    def __init__(self, in_channels, hidden_dim, out_channels):
        super(SwishBlock, self).__init__()
        self.layer = nn.Sequential(
            LinearNorm(in_channels, hidden_dim, bias=True),
            nn.SiLU(),
            LinearNorm(hidden_dim, out_channels, bias=True),
            nn.SiLU(),
        )

    def forward(self, S, E, V):

        out = torch.cat(
            [
                S.unsqueeze(-1),
                E.unsqueeze(-1),
                V.unsqueeze(1).expand(-1, E.size(1), -1, -1),
            ],
            dim=-1,
        )
        out = self.layer(out)

        return out


class ConvNorm(nn.Module):
    """1D Convolution"""

    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size=1,
        stride=1,
        padding=None,
        dilation=1,
        bias=True,
        w_init_gain="linear",
    ):
        super(ConvNorm, self).__init__()

        if padding is None:
            assert kernel_size % 2 == 1
            padding = int(dilation * (kernel_size - 1) / 2)

        self.conv = nn.Conv1d(
            in_channels,
            out_channels,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            dilation=dilation,
            bias=bias,
        )

    def forward(self, signal):
        conv_signal = self.conv(signal)

        return conv_signal


class ConvBlock(nn.Module):
    """Convolutional Block"""

    def __init__(self, in_channels, out_channels, kernel_size, dropout, activation=nn.ReLU()):
        super(ConvBlock, self).__init__()

        self.conv_layer = nn.Sequential(
            ConvNorm(
                in_channels,
                out_channels,
                kernel_size=kernel_size,
                stride=1,
                padding=int((kernel_size - 1) / 2),
                dilation=1,
                w_init_gain="tanh",
            ),
            nn.BatchNorm1d(out_channels),
            activation,
        )
        self.dropout = dropout
        self.layer_norm = nn.LayerNorm(out_channels)

    def forward(self, enc_input, mask=None):
        enc_output = enc_input.contiguous().transpose(1, 2)
        enc_output = F.dropout(self.conv_layer(enc_output), self.dropout, self.training)

        enc_output = self.layer_norm(enc_output.contiguous().transpose(1, 2))
        if mask is not None:
            enc_output = enc_output.masked_fill(mask.unsqueeze(-1), 0)

        return enc_output


# def get_mask_from_lengths(lengths, max_len=None):
#     batch_size = lengths.shape[0]
#     if max_len is None:
#         max_len = torch.max(lengths).item()

#     ids = torch.arange(0, max_len).unsqueeze(0).expand(batch_size, -1).to(lengths.device)
#     breakpoint()
#     mask = ids >= lengths.unsqueeze(1).expand(-1, max_len)

#     return mask


class LearnedUpsampling(nn.Module):
    """Learned Upsampling"""

    def __init__(
        self,
        in_out_channels=256,
        conv_out_size=8,
        kernel_size=3,
        dropout=0.0,
        w_channels=16,
        c_channels=2,
        max_seq_len=1000,
    ):
        super(LearnedUpsampling, self).__init__()
        self.max_seq_len = max_seq_len
        # Attention (W)
        self.conv_w = ConvBlock(in_out_channels, conv_out_size, kernel_size, dropout=dropout, activation=nn.SiLU())
        self.swish_w = SwishBlock(conv_out_size + 2, w_channels, w_channels)
        self.linear_w = LinearNorm(w_channels, 1, bias=True)
        self.softmax_w = nn.Softmax(dim=2)

        # Auxiliary Attention Context (C)
        self.conv_c = ConvBlock(in_out_channels, conv_out_size, kernel_size, dropout=dropout, activation=nn.SiLU())
        self.swish_c = SwishBlock(conv_out_size + 2, c_channels, c_channels)

        # Upsampled Representation (O)
        self.linear_einsum = LinearNorm(c_channels, in_out_channels)  # A
        self.layer_norm = nn.LayerNorm(in_out_channels)

    def forward(self, duration, V, src_len, src_mask, max_src_len):
        device = duration.device
        batch_size = duration.shape[0]

        # Duration Interpretation
        mel_len = torch.round(duration.sum(-1)).type(torch.LongTensor).to(device)
        mel_len = torch.clamp(mel_len, max=self.max_seq_len, min=1)
        max_mel_len = mel_len.max().item()
        mel_mask = sequence_mask(mel_len, max_mel_len)

        # Prepare Attention Mask
        attn_mask = torch.unsqueeze(src_mask, -1) * torch.unsqueeze(mel_mask, 2)
        attn_mask = attn_mask.squeeze(1).transpose(1, 2).bool()

        # Token Boundary Grid
        duration = duration.squeeze(1)
        e_k = torch.cumsum(duration, dim=1)
        s_k = e_k - duration
        e_k = e_k.unsqueeze(1).expand(batch_size, max_mel_len, -1)
        s_k = s_k.unsqueeze(1).expand(batch_size, max_mel_len, -1)
        t_arange = (
            torch.arange(1, max_mel_len + 1, device=device)
            .unsqueeze(0)
            .unsqueeze(-1)
            .expand(batch_size, -1, max_src_len)
        )
        S, E = (t_arange - s_k).masked_fill(~attn_mask, 0), (e_k - t_arange).masked_fill(~attn_mask, 0)

        # Attention (W)
        V = V.transpose(1, 2)
        W = self.swish_w(S, E, self.conv_w(V))  # [B, T, K, w_channels]
        src_mask_ = ~src_mask.expand(-1, attn_mask.shape[1], -1).bool()
        W = self.linear_w(W).squeeze(-1).masked_fill(src_mask_, -np.inf)  # [B, T, K]
        W = self.softmax_w(W)  # [B, T, K]
        mel_mask_ = ~mel_mask.expand(-1, attn_mask.shape[2], -1).transpose(1, 2).bool()
        W = W.masked_fill(mel_mask_, 0.0)

        # Auxiliary Attention Context (C)
        C = self.swish_c(S, E, self.conv_c(V))  # [B, T, K, c_channels]

        # Upsampled Representation (O)
        upsampled_rep = torch.matmul(W, V) + self.linear_einsum(torch.einsum("btk,btkp->btp", W, C))  # [B, T, M]
        upsampled_rep = self.layer_norm(upsampled_rep)
        upsampled_rep = upsampled_rep * mel_mask.transpose(1, 2)
        return upsampled_rep, mel_mask, mel_len, W
