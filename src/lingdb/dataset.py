"""The dataset module contains helpers for loading datasets from JSON."""

from enum import StrEnum
from pathlib import Path
from typing import List

from lingdb.language import LanguageSet


DATASETS_PATH = Path(__file__).parent.parent.parent / 'data' / 'datasets'


class Dataset(StrEnum):
    """The names of all datasets from current and past semesters.

    Datasets can be loaded from their JSON files with the .load() method.

    NOTE: The order in which datasets are defined here is significant;
        the last defined dataset will be the one returned by `latest()`.
    """

    # Test datasets
    TEST = "_test"
    """An internal dataset used only for testing."""

    TEST2 = "_test2"
    """An internal dataset used only for testing."""

    S19TEST = "S19test"
    """An internal version of the Spring 2019 dataset used to test the survey parser."""

    # Semester datasets
    F17 = "F17"
    """The Fall 2017 dataset."""

    S19 = "S19"
    """The Spring 2019 dataset."""

    F19 = "F19"
    """The Fall 2019 dataset."""

    F21 = "F21"
    """The Fall 2021 dataset."""

    F22 = "F22"
    """The Fall 2022 dataset."""

    def is_test(self) -> bool:
        """Return True if this dataset is for testing use only."""
        return 'test' in self.value

    def load(self) -> LanguageSet:
        """Load the Dataset from its associated JSON file."""
        # e.g. $DATASETS_PATH/F22/F22.json
        filepath = DATASETS_PATH / self / f'{self}.json'
        return LanguageSet.from_json(filepath)

    @classmethod
    def latest(cls) -> 'Dataset':
        """Return the latest (i.e. most recently defined) Dataset."""
        datasets: List[Dataset] = list(cls.__members__.values())
        return datasets[-1]
