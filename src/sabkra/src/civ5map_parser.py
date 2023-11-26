from .world import World


def read_world_data(input_file_path):
    with open(input_file_path, 'rb') as f:
        world = World.from_file(f)
        world.init(f)
    return world
