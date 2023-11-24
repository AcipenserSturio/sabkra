from .tile import Tile
from .world import World
from .utils import (
    get_byte,
    get_int,
    get_flags,
    get_string,
    get_string_array,
)


def get_world_data_from_file(f):
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

    return (
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


def read_world_data(input_file_path):
    with open(input_file_path, 'rb') as f:
        world = World(*get_world_data_from_file(f))

        tilemap = []

        # Map data
        for row in range(world.height):
            tilemap.append([])
            for col in range(world.width):
                tile = Tile.from_file(world, row, col, f)
                tilemap[row].append(tile)
    return world, tilemap
