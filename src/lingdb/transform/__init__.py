"""The transform package defines Transformations and various variants thereof.

Transformations are callables mapping from arbitrary inputs to arbitrary outputs.
"""

from .extractors import (  # noqa: W0611
    Extractor,
)

from .predicates import (  # noqa: W0611
    Predicate,
)

from .transformations import (  # noqa: W0611
    Transformation,
)
