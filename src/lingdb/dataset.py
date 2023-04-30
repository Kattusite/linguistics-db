"""The dataset module contains helpers for loading datasets from JSON."""

from pathlib import Path

from lingdb.language import LanguageSet
from lingdb.utils import StrEnum


DATASETS_PATH = Path(__file__).parent.parent / 'data' / 'datasets'


class Datasets(StrEnum):
    """The names of all datasets from current and past semesters.

    Datasets can be loaded from their JSON files with the .load() method.
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

    def load(self) -> LanguageSet:
        """Load the Dataset from its associated JSON file."""
        # e.g. $DATASETS_PATH/F22/F22.json
        filepath = DATASETS_PATH / self / f'{self}.json'
        return LanguageSet.from_json(filepath)


