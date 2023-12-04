from dataclasses import dataclass
import pygame

from ..parser.tile import Tile


image_tiling_width = 76
image_tiling_height = 65
image_tiling_height_full = 86


@dataclass
class TilePygame(Tile):
    def __post_init__(self):
        self._highlight = None

    def __hash__(self):
        return (self.col, self.row).__hash__()

    @property
    def highlight(self):
        return self._highlight

    @highlight.setter
    def highlight(self, value):
        self._highlight = value
        self.rerender()

    @Tile.terrain.setter
    def terrain(self, value):
        index = self.world.terrain.index(value) if value else -1
        if self.terrain != value:
            self.terrain_id = index
            self.rerender()

    @Tile.elevation.setter
    def elevation(self, value):
        index = self.world.elevation.index(value) if value else -1
        if self.elevation != value:
            self.elevation_id = index
            self.rerender()

    @Tile.feature.setter
    def feature(self, value):
        index = self.world.feature.index(value) if value else -1
        if self.feature != value:
            self.feature_id = index
            self.rerender()

    @Tile.resource.setter
    def resource(self, value):
        index = self.world.resource.index(value) if value else -1
        if self.resource != value:
            self.resource_id = index
            self.rerender()

    @Tile.continent.setter
    def continent(self, value):
        index = self.world.continent.index(value) if value else -1
        if self.continent != value:
            self.continent_id = index
            self.rerender()

    @Tile.wonder.setter
    def wonder(self, value):
        index = self.world.wonder.index(value) if value else -1
        if self.wonder != value:
            self.wonder_id = index
            self.rerender()

    # Draw
    def render(self):
        # Draw terrain
        if terrain := self.get_image(self.terrain):
            self.world.canvas.blit(terrain, self.pos)
        # Draw elevation
        if elevation := self.get_image(self.elevation):
            self.world.canvas.blit(elevation, self.pos)
        # Draw feature
        if feature := self.get_image(self.feature):
            self.world.canvas.blit(feature, self.pos)
        # Draw feature
        if resource := self.get_image(self.resource):
            self.world.canvas.blit(resource, self.pos)
        # Draw grid
        # self.world.canvas.blit(self.get_image("grid"), self.pos)
        # Draw river
        for river in self.get_river_state():
            self.world.canvas.blit(self.get_image(river), self.pos)
        # Draw road
        for road in self.get_road_state():
            self.world.canvas.blit(self.get_image(road), self.pos)
        # Draw city
        if self.improvement.city_id != -1:
            self.world.canvas.blit(self.get_image("city"), self.pos)
        # Draw current tile selector
        if self.highlight:
            self.world.canvas.blit(self.get_image("selected"), self.pos)

    def rerender(self):
        if not self.world.canvas:
            return
        self.render()
        self.world.texture.update(
            self.world.canvas.subsurface(
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
        return self.world.images.get(name)

    @property
    def x(self):
        return int(self.col * image_tiling_width
                   + self.row % 2 * image_tiling_width / 2)

    @property
    def y(self):
        return int(
            (self.world.height - self.row) * image_tiling_height
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
