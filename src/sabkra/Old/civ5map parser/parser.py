import json
input_file_path = "lungorajapan_ai.civ5map"


class World:
    def __init__(self, version, width, height, players, randomgoodies, randomresourses, wrap, terrain, feature, wonder, resourse, moddata, name, description, elevation):
        self.version = version
        self.width = width
        self.height = height
        self.players = players
        self.randomgoodies = randomgoodies
        self.randomresourses = randomresourses
        self.wrap = wrap
        self.terrain = terrain
        self.feature = feature
        self.wonder = wonder
        self.resourse = resourse
        self.moddata = moddata
        self.name = name
        self.description = description
        self.elevation = elevation
    def __repr__(self):
        string = ""
        string += "Version\t\t\t{}\n".format(self.version)
        string += "Width\t\t\t{}\n".format(self.width)
        string += "Height\t\t\t{}\n".format(self.height)
        string += "Players\t\t\t{}\n".format(self.players)
        string += "Random goodies\t\t{}\n".format(self.randomgoodies)
        string += "Random resourses\t{}\n".format(self.randomresourses)
        string += "World wrap\t\t{}\n".format(self.wrap)
        string += "Terrain\t\t\t{}\n".format(self.terrain)
        string += "Feature\t\t\t{}\n".format(self.feature)
        string += "Wonder\t\t\t{}\n".format(self.wonder)
        string += "Resourse\t\t{}\n".format(self.resourse)
        string += "Mod data\t\t{}\n".format(self.moddata)
        string += "Name\t\t\t{}\n".format(self.name)
        string += "Description\t\t{}\n".format(self.description)
        string += "Elevation\t\t{}\n".format(self.elevation)
        return string
class Tile:
    def __init__(self, world, row, col, terrain_id, resourse_id, feature_id, river_southwest, river_southeast, river_east, elevation_id, wonder_id):
        self.world = world
        self.row = row
        self.col = col
        self.terrain_id = terrain_id
        self.resourse_id = resourse_id
        self.feature_id = feature_id
        self.river_southwest = river_southwest
        self.river_southeast = river_southeast
        self.river_east = river_east
        self.elevation_id = elevation_id
        self.wonder_id = wonder_id
    def __repr__(self):
        string = ""
        string += "Row\t\t\t{}\n".format(self.row)
        string += "Col\t\t\t{}\n".format(self.col)
        string += "Terrain\t\t\t{}\n".format(self.get_terrain())
        string += "Resourse\t\t{}\n".format(self.get_resourse())
        string += "Feature\t\t\t{}\n".format(self.get_feature())
        string += "River (SW, SE, E)\t{} {} {}\n".format(self.river_southwest, self.river_southeast, self.river_east)
        string += "Elevation\t\t{}\n".format(self.get_elevation())
        string += "Wonder\t\t\t{}\n".format(self.get_wonder())
        return string
    def get_terrain(self):
        if not self.terrain_id == 255:
            return world.terrain[self.terrain_id]
    def get_resourse(self):
        if not self.resourse_id == 255:
            return world.resourse[self.resourse_id]
    def get_feature(self):
        if not self.feature_id == 255:
            return world.feature[self.feature_id]
    def get_elevation(self):
        if not self.elevation_id == 255:
            return world.elevation[self.elevation_id]
    def get_wonder(self):
        if not self.wonder_id == 255:
            return world.wonder[self.wonder_id]

# Reading bytes as variables from file
def get_byte(f):
    return int.from_bytes(f.read(1), "little")
def get_int(f):
    return int.from_bytes(f.read(4), "little")
def get_flags(f):
    return list(map(lambda x : True if x == '1' else False, '{0:b}'.format(get_byte(f)).zfill(8)))
def get_string(f, length):
    string = ""
    for i in range(length):
        value = f.read(1)
        string += value.decode()
    return string[:-1]
def get_string_array(f, length):
    return get_string(f, length).split("\0")

# Reading several variables from file as tile data
def get_tile_data_from_file(f):
    terrain = get_byte(f)
    resourse = get_byte(f)
    feature = get_byte(f)
    _, _, _, _, _, river_southwest, river_southeast, river_east = get_flags(f)
    elevation = get_byte(f)
    _ = get_byte(f)
    wonder = get_byte(f)
    _ = get_byte(f)
    return terrain, resourse, feature, river_southwest, river_southeast, river_east, elevation, wonder

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

    return version, width, height, players, randomgoodies, randomresourses, wrap, terrain, feature, wonder, resourse, moddata, name, description, elevation

def read_world_data():
    with open(input_file_path, 'rb') as f:
        world = World(*get_world_data_from_file(f))

        tilemap = []

        # Map data
        for row in range(world.height):
            tilemap.append([])
            for col in range(world.width):
                tile = Tile(world, row, col, *get_tile_data_from_file(f))
                tilemap[row].append(tile)
    return world, tilemap

world, tilemap = read_world_data()
