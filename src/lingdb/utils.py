"""A collection of various Python utilities."""

from collections.abc import Collection

from typing import Generic, Iterator, Mapping, Optional, TypeVar, Union


KT = TypeVar('KT')
DT = TypeVar('DT')
VT = TypeVar('VT')


class MappedCollection(Generic[KT, VT], Collection[VT]):
    """A Collection[VT] that supports getting items by a key."""

    __slots__ = '_mapping',

    def __init__(self, mapping: Mapping[KT, VT]) -> None:
        self._mapping = mapping

    def __contains__(self, item: object) -> bool:
        return item in self._mapping.values()

    def __iter__(self) -> Iterator[VT]:
        return iter(self._mapping.values())

    def __len__(self) -> int:
        return len(self._mapping)

    def __getitem__(self, key: KT) -> VT:
        return self._mapping[key]

    def get(self, key: KT, default: Optional[DT] = None) -> Union[VT, Optional[DT]]:
        return self._mapping.get(key, default=default)
