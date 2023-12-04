# Reading bytes as variables from file
def get_byte(f):
    return int.from_bytes(f.read(1), "little")


def get_int(f):
    return int.from_bytes(f.read(4), "little")


def get_short(f):
    return int.from_bytes(f.read(2), "little")


def get_flags(f):
    return list(map(lambda x: True if x == "1" else False,
                    "{0:b}".format(get_byte(f)).zfill(8)))


def get_buffer(f, length):
    return f.read(length)


def get_buffered_string(f, length):
    return get_buffer(f, length).split(b"\0")[0]


def get_string(f, length):
    string = ""
    for i in range(length):
        value = f.read(1)
        string += value.decode()
    return string[:-1]


def get_string_array(f, length):
    return get_string(f, length).split("\0")
