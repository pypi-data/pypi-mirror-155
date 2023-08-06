import struct
from typing import Type, TypeVar, Generic, BinaryIO, Optional

__all__ = ['CSTypes']

T = TypeVar('T')


class BaseCSType(Generic[T]):
    def __init__(self, name: str, pytype: Type) -> None:
        self.name: str = name
        self.pytype: Type = pytype

    def unpack(self, data: bytes) -> Optional[T]:
        return None

    def pack(self, value: T) -> bytes:
        return b''

    def calcsize(self) -> int:
        return -1

    def unpackFrom(self, f: BinaryIO) -> Optional[T]:
        return None


class SimpleCSType(BaseCSType[T]):
    def __init__(self, name: str, fmt: str, size: int, pytype: Type) -> None:
        super().__init__(name, pytype)
        self.format: str = fmt
        self.size: int = size

    def unpack(self, data: bytes) -> Optional[T]:
        sz: int = self.calcsize()
        if len(data) < sz:
            return None
        return struct.unpack(self.format, data[:sz])[0]

    def pack(self, value: T) -> bytes:
        return struct.pack(self.format, value)

    def calcsize(self) -> int:
        return self.size if self.size > 0 else struct.calcsize(self.format)

    def unpackFrom(self, f: BinaryIO) -> Optional[T]:
        sz: int = self.calcsize()
        data: bytes = f.read(sz)
        if len(data) < sz:
            return None
        return struct.unpack(self.format, data)[0]
