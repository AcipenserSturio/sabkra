from __future__ import annotations

from dataclasses import dataclass

from .utils import (
    get_byte,
    get_int,
    get_flags,
    get_string,
    get_string_array,
)

from .tile import Tile


@dataclass
class World:
    version: int
    width: int
    height: int
    players: int
    randomgoodies: bool
    randomresourses: bool
    wrap: bool
    terrain: list
    feature: list
    wonder: list
    resourse: list
    moddata: str
    name: str
    description: str
    elevation: list

    @classmethod
    def from_file(cls, f):

        version = get_byte(f)
        width = get_int(f)
        height = get_int(f)
        players = get_byte(f)

        _, _, _, _, _, randomgoodies, randomresourses, wrap = get_flags(f)
        _ = get_byte(f)
        _ = get_byte(f)
        _ = get_byte(f)

        terrain_length = get_int(f)
        feature_length = get_int(f)
        wonder_length = get_int(f)
        resourse_length = get_int(f)
        moddata_length = get_int(f)
        name_length = get_int(f)
        description_length = get_int(f)

        terrain = get_string_array(f, terrain_length)
        feature = get_string_array(f, feature_length)
        wonder = get_string_array(f, wonder_length)
        resourse = get_string_array(f, resourse_length)
        moddata = get_string(f, moddata_length)
        name = get_string(f, name_length)
        description = get_string(f, description_length)

        string3_length = get_int(f)
        string3 = get_string_array(f, string3_length)

        elevation = ['FLAT', 'HILL', 'MOUNTAIN']

        return cls(
            version,
            width,
            height,
            players,
            randomgoodies,
            randomresourses,
            wrap,
            terrain,
            feature,
            wonder,
            resourse,
            moddata,
            name,
            description,
            elevation
        )

    def tiles(self):
        for row in self.tilemap:
            for tile in row:
                yield tile

    def get_tile(self, row, col):
        return self.tilemap[row][col]

    def init(self, f):

        # Load tiles
        self.tilemap = []
        for row in range(self.height):
            self.tilemap.append([])
            for col in range(self.width):
                tile = Tile.from_file(self, row, col, f)
                self.tilemap[row].append(tile)

        #
