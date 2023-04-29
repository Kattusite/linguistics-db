"""A collection of various Python utilities."""

from collections.abc import (
    ItemsView,
    KeysView,
    ValuesView,
)
from typing import Generic, Iterator, Mapping, Optional, TypeVar, Union


KT = TypeVar('KT')
DT = TypeVar('DT')
VT = TypeVar('VT')


class ValueMapping(Mapping[KT, VT]):
    """Like a Mapping[KT, VT], whose __iter__ and __contains__ operate on its values.

    Unfortunately, that signature isn't compatible with Mapping[KT, VT],
    so we can't inherit any of the interface ourselves.
    """

    __slots__ = '_mapping',

    def __init__(self, mapping: Mapping[KT, VT]) -> None:
        self._mapping = mapping

    def __getitem__(self, key: KT) -> VT:
        return self._mapping[key]

    def __iter__(self) -> Iterator[VT]:
        return iter(self._mapping.values())

    def __len__(self) -> int:
        return len(self._mapping)

    def __contains__(self, key: object) -> bool:
        return key in self._mapping.values() or key in self._mapping.keys()

    def keys(self) -> KeysView[KT]:
        return self._mapping.keys()

    def items(self) -> ItemsView[KT, VT]:
        return self._mapping.items()

    def values(self) -> ValuesView[VT]:
        return self._mapping.values()

    def get(self, key: KT, default: Optional[DT] = None) -> Union[VT, Optional[DT]]:
        return self._mapping.get(key, default=default)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Mapping):
            return NotImplemented
        return dict(self.items()) == dict(other.items())

    def __ne__(self, other: object) -> bool:
        return self != other
