from dataclasses import dataclass

from .world import World

from .utils import (
    get_byte,
    get_flags,
)


@dataclass
class Tile:
    world: World
    row: int
    col: int
    terrain_id: int
    resourse_id: int
    feature_id: int
    river_southwest: bool
    river_southeast: bool
    river_east: bool
    elevation_id: int
    wonder_id: int

    @classmethod
    def from_file(cls, world, row, col, f):
        terrain = get_byte(f)
        resourse = get_byte(f)
        feature = get_byte(f)
        (_, _, _, _, _,
         river_southwest,
         river_southeast,
         river_east) = get_flags(f)
        elevation = get_byte(f)
        _ = get_byte(f)
        wonder = get_byte(f)
        _ = get_byte(f)

        return cls(
            world,
            row,
            col,
            terrain,
            resourse,
            feature,
            river_southwest,
            river_southeast,
            river_east,
            elevation,
            wonder,
        )

    def get_terrain(self):
        if not self.terrain_id == 255:
            return self.world.terrain[self.terrain_id]

    def get_resourse(self):
        if not self.resourse_id == 255:
            return self.world.resourse[self.resourse_id]

    def get_feature(self):
        if not self.feature_id == 255:
            return self.world.feature[self.feature_id]

    def get_elevation(self):
        if not self.elevation_id == 255:
            return self.world.elevation[self.elevation_id]

    def get_wonder(self):
        if not self.wonder_id == 255:
            return self.world.wonder[self.wonder_id]

    def get_river_state(self):
        return ("".join([
            str(int(self.river_southwest)),
            str(int(self.river_southeast)),
            str(int(self.river_east)),
        ]))
