"""A collection of various Python utilities."""

from collections.abc import Collection
from enum import Enum
from typing import (
    Generic,
    Iterator,
    List,
    Mapping,
    Optional,
    TypeVar,
    Union,
    overload,
)


KT = TypeVar('KT')
DT = TypeVar('DT')
VT = TypeVar('VT')


class StrEnum(str, Enum):
    """An Enum that is also a str."""

    def __str__(self):
        return str(self.value)


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

    @overload
    def __getitem__(self, key: int) -> VT:
        pass

    @overload
    def __getitem__(self, key: slice) -> List[VT]:  # type: ignore[misc]
        pass

    @overload
    def __getitem__(self, key: KT) -> VT:
        pass

    def __getitem__(self, key: Union[KT, int, slice]):
        # Also allow indexing by an ordinary int or slice
        # HACK: Creating a temp list every time is kinda janky, but it makes the logic easier.
        if isinstance(key, (int, slice)):
            return list(self._mapping.values())[key]
        return self._mapping[key]

    @overload
    def get(self, key: KT) -> Optional[VT]:
        pass

    @overload
    def get(self, key: KT, default: Optional[DT] = None) -> Union[VT, Optional[DT]]:
        pass

    def get(self, key: KT, default: Optional[DT] = None):
        return self._mapping.get(key, default=default)
