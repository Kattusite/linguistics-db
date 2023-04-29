"""Just an entry point for use in interactive testing."""

# cspell:disable
# pylint: disable=unused-import

from pathlib import Path

from lingdb.language import (
    LanguageSet,
)
from lingdb.transform import (  # noqa: W0611
    GetConsonants,
    GetName,
    GetNumConsonants,
    GetEndangermentLevel,
    Intersection,
    Length,
)
from lingdb.query import Query

query = (
    Query()
    .apply(GetConsonants)
    .apply(Length)
    .extract_context()
)

DATASETS = Path(__file__).parent.parent / 'data' / 'datasets'
F22_JSON = DATASETS / 'F22' / 'F22.json'

F22 = LanguageSet.from_json(F22_JSON)


result = query.evaluate(F22)
