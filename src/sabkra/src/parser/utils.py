# Reading bytes as variables from file
def get_byte(f):
    value = int.from_bytes(f.read(1), "little")
    return -1 if value == 255 else value


def get_short(f):
    value = int.from_bytes(f.read(2), "little")
    return -1 if value == 65535 else value


def get_int(f):
    value = int.from_bytes(f.read(4), "little")
    return -1 if value == 4294967295 else value


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
