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


def init_world(file_path):
    with open(file_path, "rb") as f:
        world = World.from_file(f)
        world.init(f)
    return world


@dataclass
class World:
    version: int
    width: int
    height: int
    players: int
    randomgoodies: bool
    randomresources: bool
    wrap: bool
    terrain: list
    feature: list
    wonder: list
    resource: list
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

        _, _, _, _, _, randomgoodies, randomresources, wrap = get_flags(f)
        _ = get_byte(f)
        _ = get_byte(f)
        _ = get_byte(f)

        length_terrain = get_int(f)
        length_feature = get_int(f)
        length_wonder = get_int(f)
        length_resource = get_int(f)
        length_moddata = get_int(f)
        length_name = get_int(f)
        length_description = get_int(f)

        terrain = get_string_array(f, length_terrain)
        feature = get_string_array(f, length_feature)
        wonder = get_string_array(f, length_wonder)
        resource = get_string_array(f, length_resource)
        moddata = get_string(f, length_moddata)
        name = get_string(f, length_name)
        description = get_string(f, length_description)

        length_world_size = get_int(f)
        world_size = get_string_array(f, length_world_size)

        elevation = ["FLAT", "HILL", "MOUNTAIN"]

        return cls(
            version,
            width,
            height,
            players,
            randomgoodies,
            randomresources,
            wrap,
            terrain,
            feature,
            wonder,
            resource,
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
        if self.wrap:
            col = col % self.width
        if col >= self.width or col < 0:
            return
        if row >= self.height or row < 0:
            return
        return self.tilemap[row][col]

    def init(self, f):
        # Load tiles
        self.tilemap = []
        for row in range(self.height):
            self.tilemap.append([])
            for col in range(self.width):
                tile = Tile.from_file(self, row, col, f)
                self.tilemap[row].append(tile)
