"""web.exceptions contains several exceptions that might arise during request handling."""


class NoSuchDataset(ValueError):
    """An exception indicating the dataset of the requested name could not be found."""

    def __init__(self, dataset_name: str):
        self.dataset = dataset_name
        super().__init__(f'No such dataset: {dataset_name}')


class FailedLoadingDataset(ValueError):
    """An exception indicating the dataset of the requested name could not be loaded."""

    def __init__(self, dataset_name: str):
        self.dataset = dataset_name
        super().__init__(f'Failed to load dataset: {dataset_name}')


class UnrecognizedToken(ValueError):
    """An exception indicating that a token was not recognized."""

    def __init__(self, key: str, value: str, i: int):
        self.key = key
        self.value = value
        self.i = i
        super().__init__(f'token {i} was unrecognized: {key}={value}')
