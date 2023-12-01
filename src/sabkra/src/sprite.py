import pygame

image_tiling_width = 76
image_tiling_height = 65
image_tiling_height_full = 86


class Sprite:
    def __init__(self, scene, tile):
        self.scene = scene
        self.tile = tile
        self.highlight = None

    def __repr__(self):
        return f"Sprite({self.tile.col}, {self.tile.row})"

    @property
    def highlight(self):
        return self._highlight

    @highlight.setter
    def highlight(self, value):
        self._highlight = value
        self.rerender()

    @property
    def terrain(self):
        return self.tile.get_terrain()

    @terrain.setter
    def terrain(self, value):
        index = self.tile.world.terrain.index(value) if value else 255
        if self.terrain != value:
            self.tile.terrain_id = index
            self.rerender()

    @property
    def elevation(self):
        return self.tile.get_elevation()

    @elevation.setter
    def elevation(self, value):
        index = self.tile.world.elevation.index(value) if value else 255
        if self.elevation != value:
            self.tile.elevation_id = index
            self.rerender()

    @property
    def feature(self):
        return self.tile.get_feature()

    @feature.setter
    def feature(self, value):
        index = self.tile.world.feature.index(value) if value else 255
        if self.feature != value:
            self.tile.feature_id = index
            self.rerender()

    @property
    def resource(self):
        return self.tile.get_resource()

    @resource.setter
    def resource(self, value):
        index = self.tile.world.resource.index(value) if value else 255
        if self.resource != value:
            self.tile.resource_id = index
            self.rerender()

    @property
    def continent(self):
        return self.tile.get_continent()

    @continent.setter
    def continent(self, value):
        index = self.tile.world.continent.index(value) if value else 255
        if self.continent != value:
            self.tile.continent_id = index
            self.rerender()

    @property
    def wonder(self):
        return self.tile.get_wonder()

    @wonder.setter
    def wonder(self, value):
        index = self.tile.world.wonder.index(value) if value else 255
        if self.wonder != value:
            self.tile.wonder_id = index
            self.rerender()

    # Draw
    def render(self):
        # Draw terrain
        if terrain := self.get_image(self.tile.get_terrain()):
            self.scene.canvas.blit(terrain, self.pos)
        # Draw elevation
        if elevation := self.get_image(self.tile.get_elevation()):
            self.scene.canvas.blit(elevation, self.pos)
        # Draw feature
        if feature := self.get_image(self.tile.get_feature()):
            self.scene.canvas.blit(feature, self.pos)
        # Draw feature
        if resource := self.get_image(self.tile.get_resource()):
            self.scene.canvas.blit(resource, self.pos)
        # Draw grid
        # self.scene.canvas.blit(self.get_image("grid"), self.pos)
        # Draw river
        for river in self.tile.get_river_state():
            self.scene.canvas.blit(self.get_image(river), self.pos)
        # Draw current tile selector
        if self.highlight:
            self.scene.canvas.blit(self.get_image("selected"), self.pos)

    def rerender(self):
        if not self.scene.canvas:
            return
        self.render()
        self.scene.texture.update(
            self.scene.canvas.subsurface(
                self.x,
                self.y,
                image_tiling_width,
                image_tiling_height_full,
            ),
            area=(
                self.x,
                self.y,
                image_tiling_width,
                image_tiling_height_full,
            )
        )

    def get_image(self, name):
        return self.scene.images.get(name)

    @property
    def x(self):
        return int(self.tile.col * image_tiling_width
                   + self.tile.row % 2 * image_tiling_width / 2)

    @property
    def y(self):
        return int(
            (self.tile.world.height - self.tile.row) * image_tiling_height
        )

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def centre_pos(self):
        return (self.x + int(image_tiling_width / 2),
                self.y + int(image_tiling_height_full / 2))

    def canvas(self):
        return pygame.Surface((
            self.x + image_tiling_width*1.5,
            self.y + image_tiling_height_full,
        )).convert_alpha()
