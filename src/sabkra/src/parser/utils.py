from typing import (
    BinaryIO,
    List,
)


# Reading bytes as variables from file
def get_byte(f: BinaryIO) -> int:
    value = int.from_bytes(f.read(1), "little")
    return -1 if value == 255 else value


def get_short(f: BinaryIO) -> int:
    value = int.from_bytes(f.read(2), "little")
    return -1 if value == 65535 else value


def get_int(f: BinaryIO) -> int:
    value = int.from_bytes(f.read(4), "little")
    return -1 if value == 4294967295 else value


def get_flags(f: BinaryIO) -> List[bool]:
    return list(map(lambda x: True if x == "1" else False,
                    "{0:b}".format(get_byte(f)).zfill(8)))


def get_buffer(f: BinaryIO, length: int) -> bytes:
    return f.read(length)


def get_buffered_string(f: BinaryIO, length: int) -> bytes:
    return get_buffer(f, length).split(b"\0")[0]


def get_string(f: BinaryIO, length: int) -> str:
    string = ""
    for i in range(length):
        value = f.read(1)
        string += value.decode()
    return string[:-1]


def get_string_array(f: BinaryIO, length: int) -> str:
    return get_string(f, length).split("\0")
