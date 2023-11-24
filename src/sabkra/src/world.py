class World:
    def __init__(self,
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
                 elevation,
                 ):
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
        string += "Version\n{}\n".format(self.version)
        string += "Width\n{}\n".format(self.width)
        string += "Height\n{}\n".format(self.height)
        string += "Players\n{}\n".format(self.players)
        string += "Random goodies\n{}\n".format(self.randomgoodies)
        string += "Random resourses\t{}\n".format(self.randomresourses)
        string += "World wrap\n{}\n".format(self.wrap)
        # string += "Terrain\n{}\n".format(self.terrain)
        # string += "Feature\n{}\n".format(self.feature)
        # string += "Wonder\n{}\n".format(self.wonder)
        # string += "Resourse\n{}\n".format(self.resourse)
        string += "Mod data\n{}\n".format(self.moddata)
        string += "Name\n{}\n".format(self.name)
        string += "Description\n{}\n".format(self.description)
        string += "Elevation\n{}\n".format(self.elevation)
        return string

