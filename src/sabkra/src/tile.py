class Tile:
    def __init__(self,
                 world,
                 row,
                 col,
                 terrain_id,
                 resourse_id,
                 feature_id,
                 river_southwest,
                 river_southeast,
                 river_east,
                 elevation_id,
                 wonder_id,
                 ):
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
        string += "Row\n{}\n".format(self.row)
        string += "Col\n{}\n".format(self.col)
        string += "Terrain\n{}\n".format(self.get_terrain())
        string += "Resourse\n{}\n".format(self.get_resourse())
        string += "Feature\n{}\n".format(self.get_feature())
        string += "River (SW, SE, E)\n{} {} {}\n".format(
            self.river_southwest, self.river_southeast, self.river_east)
        string += "Elevation\n{}\n".format(self.get_elevation())
        string += "Wonder\n{}\n".format(self.get_wonder())
        return string

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

