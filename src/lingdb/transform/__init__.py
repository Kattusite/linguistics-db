"""The transform package defines Transformations and various variants thereof.

Transformations are callables mapping from arbitrary inputs to arbitrary outputs.
"""

from typing import Optional, Type, Union
from . import extractors, predicates, transformations

from .extractors import (  # noqa: W0611
    Extractor,
)

from .predicates import (  # noqa: W0611
    Predicate,
)

from .transformations import (  # noqa: W0611
    Transformation,
)


# HACK: This is quick and dirty but works for now.
#   We can replace with something more robust later.
def get_transformation(name: str) -> Optional[Union[Type[Transformation], Transformation]]:
    """Return the Transformation of the given name, or None if the name is unrecognized."""

    # TODO: It's possible multiple of these could define colliding names.
    #   We don't handle that case at the moment.
    found = (
        getattr(extractors, name, None) or
        getattr(predicates, name, None) or
        getattr(transformations, name, None)
    )

    if found is None:
        return None

    is_transformation_instance = isinstance(found, Transformation)
    is_transformation_type = isinstance(found, type) and issubclass(found, Transformation)

    # Make sure the found transformation is either an instance of Transformation,
    # or a subclass of Transformation.
    if not is_transformation_instance and not is_transformation_type:
        # Oops, we must have found something like a local variable or an import.
        # Just return None.
        return None

    # TODO: It's still possible we found something like an abstract Transformation.
    #   For example, we don't want to return Transformation itself!
    # For right now we just ignore this case; later we may wish to revisit.
    return found
