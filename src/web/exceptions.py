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