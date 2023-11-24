from .tile import Tile
from .world import World


def read_world_data(input_file_path):
    with open(input_file_path, 'rb') as f:
        world = World.from_file(f)

        tilemap = []

        # Map data
        for row in range(world.height):
            tilemap.append([])
            for col in range(world.width):
                tile = Tile.from_file(world, row, col, f)
                tilemap[row].append(tile)
    return world, tilemap
