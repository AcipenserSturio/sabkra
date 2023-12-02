from dataclasses import dataclass

from .utils import (
    get_byte,
    get_flags,
    get_int,
    get_short,
    get_string,
    get_string_array,
)


@dataclass
class City:
    name: str
    owner_id: int
    settings: int
    population: int
    health: int

    @classmethod
    def from_file(cls, version, f):
        name = "".join(map(chr, [get_byte(f) for _ in range(64)]))
        owner_id = get_byte(f)
        settings = get_byte(f)
        population = get_short(f)
        health = get_int(f)
        for _ in range(64 if version == 11 else 32):
            get_byte(f)  # TODO: Building data
        return cls(
            name,
            owner_id,
            settings,
            population,
            health,
        )
