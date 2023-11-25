import os
import pygame

from .camera import Camera
from . import civ5map_parser
from .mouse import Mouse

background_colour = (0, 0, 0)

default_window_width = 1920
default_window_height = 1080

image_tiling_width = 34
image_tiling_height = 30
image_tiling_height_full = 40


def vector_diff(vec_a, vec_b):
    return (vec_a[0] - vec_b[0], vec_a[1] - vec_b[1])


def vector_sum(vec_a, vec_b):
    return (vec_a[0] + vec_b[0], vec_a[1] + vec_b[1])


def euclidean(x1, y1, x2, y2):
    return (x1-x2) ** 2 + (y1-y2) ** 2


def get_tile_world_pos(tile):
    x = int(tile.col * image_tiling_width
            + tile.row % 2 * image_tiling_width / 2)
    y = int(- tile.row * image_tiling_height)
    return (x, y)


def get_tile_centre_world_pos(tile):
    x, y = get_tile_world_pos(tile)
    x += int(image_tiling_width / 2)
    y += int(image_tiling_height_full / 2)
    return (x, y)


class Scene:
    def __init__(self, file_path, update_sidebar):
        self.camera = Camera(self)
        self.mouse = Mouse()
        self.update_sidebar = update_sidebar
        self.window = None
        self.worldinfo = None
        self.map = None
        self.current_tile = None
        self._sprites = {}
        self._sprites_scaled = {}

        # Load world info and map from path
        self.worldinfo, self.map = civ5map_parser.read_world_data(file_path)
        self.set_current_tile(self.map[0][0])

        # Create window
        self.on_resize_window(default_window_width, default_window_height)
        pygame.display.set_caption("World Display")

        # Load sprites
        for terrain in self.worldinfo.terrain:
            self.add_sprite(terrain, './src/sabkra/assets/terrain/{}.png'
                            .format(terrain.replace("TERRAIN_", "").lower()))
        for feature in self.worldinfo.feature:
            self.add_sprite(feature, './src/sabkra/assets/feature/{}.png'
                            .format(feature.replace("FEATURE_", "").lower()))
        self.add_sprite('selected', './src/sabkra/assets/selected.png')
        self.add_sprite('MOUNTAIN', './src/sabkra/assets/mountain.png')
        self.add_sprite('HILL', './src/sabkra/assets/hill.png')
        self.add_sprite('001', './src/sabkra/assets/rivers/001.png')
        self.add_sprite('010', './src/sabkra/assets/rivers/010.png')
        self.add_sprite('011', './src/sabkra/assets/rivers/011.png')
        self.add_sprite('100', './src/sabkra/assets/rivers/100.png')
        self.add_sprite('101', './src/sabkra/assets/rivers/101.png')
        self.add_sprite('110', './src/sabkra/assets/rivers/110.png')
        self.add_sprite('111', './src/sabkra/assets/rivers/111.png')

        # Give tiles world positions
        for row in self.map:
            for tile in row:
                tile.worldpos = get_tile_world_pos(tile)
                tile.worldpos_centre = get_tile_centre_world_pos(tile)

        # Position camera by default
        middle_tile = (
            self.map[self.worldinfo.height // 2][self.worldinfo.width // 2]
        )
        tile_x, tile_y = middle_tile.worldpos_centre
        window_width, window_height = pygame.display.get_window_size()
        centre_x = tile_x - window_width/2
        centre_y = tile_y - window_height/2
        self.camera.drag((centre_x, centre_y))

    # Event handling
    def on_resize_window(self, width, height):
        self.window = pygame.display.set_mode(
            (width, height), pygame.RESIZABLE
        )

    # Current tile
    def set_current_tile_to_mouse(self, mousepos):
        tile = self.get_nearest_tile_from_canvas_pos(mousepos)
        if tile == self.current_tile:
            return False
        self.set_current_tile(tile)
        return True

    def get_nearest_tile_from_canvas_pos(self, canvaspos):
        # Bad code. Rewrite when you can think of a better structure
        world_x, world_y = self.camera.get_world_pos_from_canvas_pos(canvaspos)
        min_distance = float("inf")
        nearest_tile = self.map[0][0]
        for row in self.map:
            for tile in row:
                tile_world_x, tile_world_y = tile.worldpos_centre
                distance = euclidean(tile_world_x, tile_world_y,
                                     world_x, world_y)
                if distance < min_distance:
                    nearest_tile = tile
                    min_distance = distance
        # print(*nearest_tile.worldpos_centre, world_x, world_y)
        return nearest_tile

    def set_current_tile(self, tile):
        self.current_tile = tile
        # tell the ui to update here
        if self.update_sidebar:
            self.update_sidebar(tile)

    def tiles(self):
        for row in self.map:
            for tile in row:
                yield tile

    def get_info_from_tile(self, tile):
        return "{}\n\n{}".format(self.worldinfo, tile)

    # Image manipulation
    def add_sprite(self, name, path):
        # print(name, path)
        # Skip missing images and hope they aren't used in the map!
        if not os.path.isfile(path):
            return
        image = pygame.image.load(path).convert_alpha()
        self._sprites[name] = image
        self.rescale_sprite(name, image)
        # print('added', name)

    def get_sprite(self, name):
        if name in self._sprites_scaled.keys():
            return self._sprites_scaled[name]

    def rescale_all_sprites(self):
        for name, image in self._sprites.items():
            self.rescale_sprite(name, image)
        # print(len(self._sprites_scaled))

    def rescale_sprite(self, name, image):
        self._sprites_scaled[name] = self.get_scaled_image(image,)

    def get_scaled_image(self, image):
        return pygame.transform.scale(
            image,
            (
                int(image.get_width()*self.camera.scale),
                int(image.get_height()*self.camera.scale)
            )
        )

    # Get image for tile
    def get_terrain_image(self, tile):
        return self.get_sprite(tile.get_terrain())

    def get_feature_image(self, tile):
        return self.get_sprite(tile.get_feature())

    def get_elevation_image(self, tile):
        return self.get_sprite(tile.get_elevation())

    def get_river_image(self, tile):
        return self.get_sprite(tile.get_river_state())

    # Draw
    def draw(self):
        self.window.fill(background_colour)

        # Draw terrain
        for tile in self.tiles():
            if terrain := self.get_terrain_image(tile):
                self.draw_tilesprite(terrain, tile)

        # Draw elevation
        for tile in self.tiles():
            if elevation := self.get_elevation_image(tile):
                self.draw_tilesprite(elevation, tile)

        # Draw feature
        for tile in self.tiles():
            if feature := self.get_feature_image(tile):
                self.draw_tilesprite(feature, tile)

        # Draw river
        for tile in self.tiles():
            if river := self.get_river_image(tile):
                self.draw_tilesprite(river, tile)

        # Draw tile selection
        self.draw_tilesprite(
            self.get_sprite('selected'),
            self.current_tile
        )
        pygame.display.update()

    def draw_tilesprite(self, image, tile):
        pos = self.get_tile_canvaspos(tile)
        self.window.blit(image, pos)

    def get_tile_canvaspos(self, tile):
        return self.camera.get_canvas_pos_from_world_pos(tile.worldpos)
