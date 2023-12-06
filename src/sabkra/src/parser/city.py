from dataclasses import dataclass

from .utils import (
    get_byte,
    get_int,
    get_short,
    get_buffer,
    get_buffered_string,
)


@dataclass
class City:
    name: str
    owner_id: int
    settings: int  # TODO: split up
    population: int
    health: int
    building_data: bytes  # TODO: parse

    @classmethod
    def from_file(cls, version, f):
        name = get_buffered_string(f, 64)
        owner_id = get_byte(f)
        settings = get_byte(f)
        population = get_short(f)
        health = get_int(f)
        building_data = get_buffer(f, 64 if version == 12 else 32)
        return cls(
            name,
            owner_id,
            settings,
            population,
            health,
            building_data,
        )
