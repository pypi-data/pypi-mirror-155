import io
import struct
import os
from enum import Enum
from typing import Union, Literal, Tuple, Optional

bytesType = bytes
floatType = float
intType = int


class WritemaTypes(Enum):
    """Various Writema types to Writema files with"""
    byte = "b"
    short = "h"
    int = "i"
    long = "q"


class WritemaFloatTypes(Enum):
    """Various Writema types to Writema files with"""
    float = "f"
    double = "d"


sizeLiteral = Literal["byte", "short", "int", "long", "float", "f", "double", "d"]
sizeType = Union[int, sizeLiteral, WritemaTypes, WritemaFloatTypes]


def get_type(size: str) -> str:
    if size in WritemaFloatTypes.__members__:
        return WritemaFloatTypes[size].value
    return WritemaTypes[size].value  # python enums kinda suck


class Writema:
    """Writema? What's Writema? WRITEMA FILE"""
    __type_shorthand = {
        1: "byte",
        2: "short",
        4: "int",
        8: "long"
    }

    __ts_rev = {
        "byte": 1,
        "short": 2,
        "int": 4,
        "long": 8
    }

    __float_shorthand = {
        "f": "float",
        "d": "double"
    }

    __fs_rev = {
        "float": "f",
        "double": "d"
    }

    __endianness = {
        "little": False,
        "big": True
    }

    def __init__(self, bytesio_or_path: Optional[Union[io.BytesIO, str]] = None):
        self.writepath = ""
        self.buffer = io.BytesIO()
        if bytesio_or_path is None:
            pass  # I dont need to actually do anything
        elif isinstance(bytesio_or_path, io.BytesIO):
            self.buffer = bytesio_or_path
        else:
            if os.path.isdir(bytesio_or_path):
                raise IsADirectoryError
            self.writepath = os.path.normpath(bytesio_or_path)

        self.endianness = self.__endianness["little"]

    def __make_fmt(self, size: sizeType, signed: bool) -> Tuple[str, int]:
        _str = ">" if self.endianness else "<"
        _size = 0
        if type(size) == int:
            if size in self.__type_shorthand:
                _size = size
                _str += get_type(self.__type_shorthand[size])
            else:
                raise TypeError
        elif type(size) == WritemaTypes:
            _size = self.__ts_rev[size.name]
            _str += size.value
        elif type(size) == WritemaFloatTypes:
            _size = 4 if size == WritemaFloatTypes.float else 8
            _str += "f" if size == WritemaFloatTypes.float else "d"
        elif type(size) == str:
            if size in WritemaTypes.__members__:
                _size = self.__ts_rev[size]
                _str += get_type(size)
            elif size in WritemaFloatTypes.__members__:
                _size = 4 if self.__fs_rev[size] == "f" else 8
                _str += get_type(size)
            elif size in self.__float_shorthand:
                _size = 4 if size == "f" else 8
                _str += size
            else:
                raise TypeError
        else:
            raise TypeError
        if not signed and type(size) != WritemaFloatTypes:
            _str = _str.upper()
        return _str, _size

    def set_endianness(self, endianness: Literal["little", "big"]) -> None:
        """ Sets endianness

        :param endianness: endianness to set [little | big]
        :return: None
        """
        self.endianness = self.__endianness[endianness]

    def bytes(self, buf: bytes) -> None:
        """ Writema bytes

        :param buf: number of bytes to write
        :return: self
        """
        self.buffer.write(buf)

    def write(self, _type: sizeType, to_write) -> None:
        """ Writema something signed

        :param _type: size type to write (Signed)
        :param to_write: value to write
        :return: self
        """
        rStr, rSize = self.__make_fmt(_type, True)
        buf = struct.pack(rStr, to_write)
        self.buffer.write(buf)

    def uwrite(self, _type: sizeType, to_write) -> None:
        """ Writema something unsigned

        :param _type: size type to write (Unsigned)
        :param to_write: value to write
        :return: self
        """
        rStr, rSize = self.__make_fmt(_type, False)
        buf = struct.pack(rStr, to_write)
        self.buffer.write(buf)

    def get_buffer(self) -> bytesType:
        """ Writema underlying buffer to memory

        :return: underlying buffer
        """
        pos = self.buffer.tell()
        self.buffer.seek(0)
        buf = self.buffer.read()
        self.buffer.seek(pos)
        return buf

    def get_io(self) -> io.BytesIO:
        """ Writema underlying BytesIO to memory

        :return: underlying BytesIO object
        """
        pos = self.buffer.tell()
        self.buffer.seek(0)
        buf = io.BytesIO(self.buffer.read())
        self.buffer.seek(pos)
        return buf

    def save(self, overwrite: bool = False, create_path: bool = False) -> None:
        """ Writema file to disk

        :param overwrite: Overwrite file?
        :param create_path: Create directory path to file if folders don't exist?
        :return: None
        """
        if self.writepath == "":
            raise ValueError("No valid path, or buffer is a BytesIO object.")
        elif os.path.isfile(self.writepath) and not overwrite:
            raise FileExistsError(f"File \"{self.writepath}\" exists, and overwrite flag is not set.")
        elif os.path.isdir(self.writepath):
            raise IsADirectoryError(f"Target path \"{self.writepath}\" is a directory.")
        if create_path:
            # create directories to path
            os.makedirs(os.path.dirname(os.path.abspath(self.writepath)), exist_ok=True)
        pos = self.buffer.tell()
        self.buffer.seek(0)
        buf = self.buffer.read()
        self.buffer.seek(pos)
        with open(self.writepath, "wb") as fp:
            fp.write(buf)
