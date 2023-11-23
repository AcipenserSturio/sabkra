import pygame, os
from . import civ5map_parser

path_by_default = "./src/sabkra/Maps/lungorajapan_ai.Civ5Map"

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 25)

default_window_width = 1920
default_window_height = 1080

fps = 60
background_colour = (0, 0, 0)

image_tiling_width = 34
image_tiling_height = 30
image_tiling_height_full = 40

scale_factor = 1.2
scale_upper_bound = 8
scale_lower_bound = 0.24

def get_tile_world_pos(tile):
    x = int(tile.col * image_tiling_width + tile.row%2 * image_tiling_width/2)
    y = int(- tile.row * image_tiling_height)
    return (x, y)
def get_tile_centre_world_pos(tile):
    x, y = get_tile_world_pos(tile)
    x += int(image_tiling_width/2)
    y += int(image_tiling_height_full/2)
    return (x, y)
def pythagoras(x1, y1, x2, y2):
    return (x1-x2)**2 + (y1-y2)**2
def vector_diff(vec_a, vec_b):
    return (vec_a[0] - vec_b[0], vec_a[1] - vec_b[1])
def vector_sum(vec_a, vec_b):
    return (vec_a[0] + vec_b[0], vec_a[1] + vec_b[1])
def mouse_pos():
    return pygame.mouse.get_pos()
class Camera:
    def __init__(self, worldbuilder):
        self.worldbuilder = worldbuilder
        self.x = 0
        self.y = 0
        self.scale = 1
    def drag(self, vector):
        self.x -= int(vector[0] / self.scale)
        self.y -= int(vector[1] / self.scale)
        print(self.x, self.y)
    def clean_rescale(self, direction):
        if direction > 0:
            if self.scale > scale_upper_bound:
                return
            self.rescale(scale_factor)
        else:
            if self.scale < scale_lower_bound:
                return
            self.rescale(1/scale_factor)
    def rescale(self, factor):
        self.scale *= factor
        mouse_x, mouse_y = mouse_pos()
        self.y += int((1/self.scale) * (1 - factor) * mouse_y)
        self.x += int((1/self.scale) * (1 - factor) * mouse_x)
        self.worldbuilder.rescale_all_sprites()
        print(self.scale)
    def get_canvas_pos_from_world_pos(self, worldpos):
        return ((worldpos[0] + self.x) * self.scale,
                (worldpos[1] + self.y) * self.scale)
    def get_world_pos_from_canvas_pos(self, canvaspos):
        return (canvaspos[0] / self.scale - self.x,
                canvaspos[1] / self.scale - self.y)
class Worldbuilder:
    def __init__(self, file_path, ui):
        self.camera = Camera(self)
        self.ui = ui
        self.window = None
        self.worldinfo = None
        self.map = None
        self.current_tile = None
        self._sprites = {}
        self._sprites_scaled = {}

        self.mouse_vector = (0, 0)
        self._previous_mouse_position = None
        self._current_mouse_position = None

        self.load_worldinfo_map_from_path(file_path)
        self.create_window()
        self.load_sprites()
        self.give_tiles_worldpos()

        self.position_camera_by_default()
        self.mouse_by_default()

    # Setup
    def create_window(self):
        self.on_resize_window(default_window_width, default_window_height)
        pygame.display.set_caption("World Display")
    def load_worldinfo_map_from_path(self, file_path):
        self.worldinfo, self.map = civ5map_parser.read_world_data(file_path)
        self.set_current_tile(self.map[0][0])
    def load_sprites(self):
        for terrain in self.worldinfo.terrain:
            self.add_sprite(terrain, './src/sabkra/Assets/Terrain/{}.png'.format(terrain.replace("TERRAIN_", "").lower()))
        for feature in self.worldinfo.feature:
            self.add_sprite(feature, './src/sabkra/Assets/Feature/{}.png'.format(feature.replace("FEATURE_", "").lower()))
        self.add_sprite('selected', './src/sabkra/Assets/selected.png')
    def position_camera_by_default(self):
        middle_tile = self.map[self.worldinfo.height//2][self.worldinfo.width//2]
        tile_x, tile_y = middle_tile.worldpos_centre
        window_width, window_height = pygame.display.get_window_size()
        centre_x = tile_x - window_width/2
        centre_y = tile_y - window_height/2
        self.camera.drag((centre_x, centre_y))
        pass
    def mouse_by_default(self):
        self._previous_mouse_position = mouse_pos()
        self._current_mouse_position = mouse_pos()
    def give_tiles_worldpos(self):
        for row in self.map:
            for tile in row:
                tile.worldpos = get_tile_world_pos(tile)
                tile.worldpos_centre = get_tile_centre_world_pos(tile)
    # Event handling
    def on_resize_window(self, width, height):
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    # Current tile
    def set_current_tile_to_mouse(self, mousepos):
        tile = self.get_nearest_tile_from_canvas_pos(mousepos)
        self.set_current_tile(tile)
    def get_nearest_tile_from_canvas_pos(self, canvaspos):
        # Bad code. Rewrite when you can think of a better structure
        world_x, world_y = self.camera.get_world_pos_from_canvas_pos(canvaspos)
        min_distance = 99999999999
        nearest_tile = self.map[0][0]
        for row in self.map:
            for tile in row:
                tile_world_x, tile_world_y = tile.worldpos_centre
                distance = pythagoras(tile_world_x, tile_world_y, world_x, world_y)
                if distance < min_distance:
                    nearest_tile = tile
                    min_distance = distance
        #print(*nearest_tile.worldpos_centre, world_x, world_y)
        return nearest_tile
    def set_current_tile(self, tile):
        self.current_tile = tile
        #tell the ui to update here
        if self.ui:
        	self.ui.configure(text=self.get_info_from_tile(tile))
        	self.ui.update()
    def get_info_from_tile(self, tile):
        return "{}\n\n{}".format(self.worldinfo, tile)
    # Image manipulation
    def add_sprite(self, name, path):
        print(name, path)
        image = pygame.image.load(path).convert_alpha()
        self._sprites[name] = image
        self.rescale_sprite(name, image)
        print('added', name)
    def get_sprite(self, name):
        if name in self._sprites_scaled.keys():
            return self._sprites_scaled[name]
    def rescale_all_sprites(self):
        for name, image in self._sprites.items():
            self.rescale_sprite(name, image)
    def rescale_sprite(self, name, image):
        self._sprites_scaled[name] = self.get_scaled_image(image,)
    def get_scaled_image(self, image):
        return pygame.transform.scale(image, (int(image.get_width()*self.camera.scale), int(image.get_height()*self.camera.scale)))

    # Get image for tile
    def get_terrain_image(self, tile):
        return self.get_sprite(tile.get_terrain())
    def get_feature_image(self, tile):
        return self.get_sprite(tile.get_feature())

    # Coordinates
    def update_mouse_vector(self):
        self._previous_mouse_position = self._current_mouse_position
        self._current_mouse_position = mouse_pos()
        self.mouse_vector = vector_diff(self._previous_mouse_position, self._current_mouse_position)
        #print(self._current_mouse_position)
    def get_tile_canvaspos(self, tile):
        worldpos = tile.worldpos
        canvaspos = self.camera.get_canvas_pos_from_world_pos(worldpos)
        return canvaspos

    # Draw
    def draw(self):
        self.window.fill(background_colour)
        for row in self.map:
            for tile in row:
                self.draw_tile(tile, self.get_tile_canvaspos(tile))
        # Draw tile selection
        self.draw_sprite(self.get_sprite('selected'), self.get_tile_canvaspos(self.current_tile))        
        pygame.display.update()
    def draw_tile(self, tile, pos):
        # Draw terrain
        terrain = self.get_terrain_image(tile)
        if terrain:
            self.draw_sprite(terrain, pos)
        # Draw feature
        feature = self.get_feature_image(tile)
        if feature:
            self.draw_sprite(feature, pos)
        #print('tile drawn at', pos)
    def draw_sprite(self, image, canvaspos):
        self.window.blit(image, canvaspos)

                
def display_world(file_path, ui):
    wb = Worldbuilder(file_path, ui)

    clock = pygame.time.Clock()
    drag_mode = False
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Close the window
                run = False
            if event.type == pygame.VIDEORESIZE:
                # Resize the window
                wb.on_resize_window(event.w, event.h)
            if event.type == pygame.MOUSEWHEEL:
                # Wheel scroll
                wb.camera.clean_rescale(event.y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Right click
                    pass
                else:
                    # Left click / wheel click
                    drag_mode = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Right click ended
                    wb.set_current_tile_to_mouse(event.pos)
                else:
                    # Left click / wheel click ended
                    drag_mode = False
        if drag_mode:
            wb.camera.drag(wb.mouse_vector)
        wb.update_mouse_vector()
        wb.draw()
    pygame.display.quit()

display_world(path_by_default, None)
