import torch


class StandardScaler:
    def __init__(self, mean=None, std=None, epsilon=1e-7):
        """Standard Scaler.
        The class can be used to normalize PyTorch Tensors using native functions. The module does not expect the
        tensors to be of any specific shape; as long as the features are the last dimension in the tensor, the module
        will work fine.

        Args:
            mean: The mean of the features. The property will be set after a call to fit.
            std: The standard deviation of the features. The property will be set after a call to fit.
            epsilon: Used to avoid a Division-By-Zero exception.
        """
        self.mean = mean
        self.std = std
        self.epsilon = epsilon
        self.num_updates = 0

    def fit(self, values):
        self.num_updates = 1
        dims = list(range(values.dim() - 1))
        self.mean = torch.mean(values, dim=dims)
        self.std = torch.std(values, dim=dims)

    def transform(self, values):
        return (values - self.mean) / (self.std + self.epsilon)

    def update(self, values, momentum):
        dims = list(range(values.dim() - 1))
        self.mean_new = torch.mean(values, dim=dims)
        self.std_new = torch.std(values, dim=dims)
        self.mean = self.num_updates * self.mean + self.mean_new
        self.num_updates += 1

    def fit_transform(self, values):
        self.fit(values)
        return self.transform(values)
