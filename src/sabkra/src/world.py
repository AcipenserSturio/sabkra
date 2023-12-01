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
from .scenario import Scenario


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
    continent: list

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
        continent = ["None", "Americas", "Asia", "Africa", "Europe"]

        self = cls(
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
            elevation,
            continent,
        )

        self.tilemap = [
            [
                Tile.from_file(self, row, col, f)
                for col in range(width)
            ]
            for row in range(height)
        ]

        self.scenario = Scenario.from_file(f)

        return self

    @classmethod
    def blank(cls, width, height):
        self = cls(
            version=12,  # or 140? unclear
            width=width,
            height=height,
            players=0,
            randomgoodies=False,
            randomresources=False,
            wrap=True,
            terrain=[
                "TERRAIN_GRASS",
                "TERRAIN_PLAINS",
                "TERRAIN_DESERT",
                "TERRAIN_TUNDRA",
                "TERRAIN_SNOW",
                "TERRAIN_COAST",
                "TERRAIN_OCEAN",
            ],
            feature=[
                "FEATURE_ICE",
                "FEATURE_JUNGLE",
                "FEATURE_MARSH",
                "FEATURE_OASIS",
                "FEATURE_FLOOD_PLAINS",
                "FEATURE_FOREST",
                "FEATURE_FALLOUT",
                "FEATURE_ATOLL",
            ],
            wonder=[
                "FEATURE_CRATER",
                "FEATURE_FUJI",
                "FEATURE_MESA",
                "FEATURE_REEF",
                "FEATURE_VOLCANO",
                "FEATURE_GIBRALTAR",
                "FEATURE_GEYSER",
                "FEATURE_FOUNTAIN_YOUTH",
                "FEATURE_POTOSI",
                "FEATURE_EL_DORADO",
                "FEATURE_SRI_PADA",
                "FEATURE_MT_SINAI",
                "FEATURE_MT_KAILASH",
                "FEATURE_ULURU",
                "FEATURE_LAKE_VICTORIA",
                "FEATURE_KILIMANJARO",
                "FEATURE_SOLOMONS_MINES",
            ],
            resource=[
                "RESOURCE_IRON",
                "RESOURCE_HORSE",
                "RESOURCE_COAL",
                "RESOURCE_OIL",
                "RESOURCE_ALUMINUM",
                "RESOURCE_URANIUM",
                "RESOURCE_WHEAT",
                "RESOURCE_COW",
                "RESOURCE_SHEEP",
                "RESOURCE_DEER",
                "RESOURCE_BANANA",
                "RESOURCE_FISH",
                "RESOURCE_STONE",
                "RESOURCE_WHALE",
                "RESOURCE_PEARLS",
                "RESOURCE_GOLD",
                "RESOURCE_SILVER",
                "RESOURCE_GEMS",
                "RESOURCE_MARBLE",
                "RESOURCE_IVORY",
                "RESOURCE_FUR",
                "RESOURCE_DYE",
                "RESOURCE_SPICES",
                "RESOURCE_SILK",
                "RESOURCE_SUGAR",
                "RESOURCE_COTTON",
                "RESOURCE_WINE",
                "RESOURCE_INCENSE",
                "RESOURCE_JEWELRY",
                "RESOURCE_PORCELAIN",
                "RESOURCE_COPPER",
                "RESOURCE_SALT",
                "RESOURCE_CRAB",
                "RESOURCE_TRUFFLES",
                "RESOURCE_CITRUS",
                "RESOURCE_ARTIFACTS",
                "RESOURCE_NUTMEG",
                "RESOURCE_CLOVES",
                "RESOURCE_PEPPER",
                "RESOURCE_HIDDEN_ARTIFACTS",
                "RESOURCE_BISON",
                "RESOURCE_COCOA"
                ],
            moddata="",
            name="",
            description="",
            elevation=["FLAT", "HILL", "MOUNTAIN"],
            continent=["None", "Americas", "Asia", "Africa", "Europe"],
        )

        self.tilemap = [
            [
                Tile.blank(self, row, col)
                for col in range(width)
            ]
            for row in range(height)
        ]

        # self.scenario = Scenario.blank()

        return self

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

    def get_tiles_in_radius(self, tile, radius):
        tiles = [(0, tile)]
        # counter acting as a secondary priority
        # to avoid comparisons between equal-priority objects
        for priority, tile in iter(tiles):
            priority += 1
            if priority > radius:
                continue
            for neighbour in tile.neighbours():
                if (priority, neighbour) in tiles:
                    continue
                tiles.append((priority, neighbour))
        return [tile for priority, tile in tiles]
