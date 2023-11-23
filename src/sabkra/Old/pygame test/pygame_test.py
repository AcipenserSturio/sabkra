import pygame, civ5map_parser

WIDTH, HEIGHT = 900, 500
OFFSET_X, OFFSET_Y, SCALE = 0, 0, 1
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Worldbuilder")

FPS = 30
BLACK = (0, 0, 0)

image_x = 34
image_y = 40
image_y_tiled = 30

class IngameTile:
    def __init__(self, tile):
        self.tile = tile
        self.worldpos_x = tile.col * image_x + tile.row%2 * image_x/2
        self.worldpos_y = - tile.row * image_y_tiled
    def get_mask(self):
        return pygame.mask.from_surface(self.get_terrain_image(self))
    def get_terrain_image(self):
        terrain = self.tile.get_terrain()
        if terrain:
            return images[terrain]
    def get_feature_image(self):
        feature = self.tile.get_feature()
        if feature:
            return images[feature]
    def point_collide(self, point):
        mask = self.get_mask()
        x, y = point
        x -= mask.rect.x
        y -= mask.rect.y
        try:
            return mask.get_at((x,y))
        except IndexError:
            return False


def get_tile_screen_position(tile):

    left = 0
    bottom = HEIGHT-image_y

    correct_coord = ((left + tile.worldpos_x + OFFSET_X) * SCALE, (bottom + tile.worldpos_y + OFFSET_Y) * SCALE)
    return correct_coord

def pythagoras(x1, y1, x2, y2):
    return (x1-x2)**2 + (y1-y2)**2

def get_nearest_tile(coord):
    min_distance = 99999999999
    nearest_tile = None
    for row in ingametilemap:
        for tile in row:
            distance = pythagoras(get_tile_screen_position(tile)[0] + image_x/2*SCALE, get_tile_screen_position(tile)[1] + image_y/2*SCALE, *coord)
            if distance < min_distance:
                nearest_tile = tile
                min_distance = distance
    print(nearest_tile.tile)
    return nearest_tile
            
def add_image(key, path):
    #print(path)
    image = pygame.image.load(path).convert_alpha()
    images_unscaled[key] = image
    images[key] = image

def rescale_image(up):
    global OFFSET_X, OFFSET_Y, SCALE, terrain_images
    scale_factor = 1.2
    if up:
        print('up')
        if SCALE > 8:
            return
    else:
        print('down')
        if SCALE < 0.24:
            return
        scale_factor = 1/scale_factor
     
    SCALE *= scale_factor
    for key, value in images_unscaled.items():
        images[key] = pygame.transform.scale(value, (int(value.get_width()*SCALE), int(value.get_height()*SCALE)))
    current_mouse_position = pygame.mouse.get_pos()
    OFFSET_Y += int((1/SCALE) * (1 - scale_factor) * current_mouse_position[1])
    OFFSET_X += int((1/SCALE) * (1 - scale_factor) * current_mouse_position[0])
    print(SCALE)

def draw_window():
    WIN.fill(BLACK) #colour
    for row in ingametilemap:
        #print(len(row))
        for tile in row:
            terrain_image = tile.get_terrain_image()
            if terrain_image:
                WIN.blit(terrain_image, get_tile_screen_position(tile))
            feature_image = tile.get_feature_image()
            #print(feature_image)
            if feature_image:
                WIN.blit(feature_image, get_tile_screen_position(tile))
    WIN.blit(images['selected'], get_tile_screen_position(current_tile))
    pygame.display.update()

def main():
    global OFFSET_X, OFFSET_Y, HEIGHT, WIDTH, current_tile
    clock = pygame.time.Clock()
    
    run = True
    previous_mouse_position = None
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.VIDEORESIZE:
                WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                HEIGHT = event.h
                WIDTH = event.w
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass
                else:
                    previous_mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    current_tile = get_nearest_tile(event.pos)
                else:
                    previous_mouse_position = None
            if event.type == pygame.MOUSEWHEEL:
                rescale_image(True if event.y > 0 else False)
        if previous_mouse_position:
            current_mouse_position = pygame.mouse.get_pos()
            OFFSET_X += (current_mouse_position[0] - previous_mouse_position[0])/SCALE
            OFFSET_Y += (current_mouse_position[1] - previous_mouse_position[1])/SCALE
            previous_mouse_position = current_mouse_position
            #print(OFFSET_X, OFFSET_Y)
        #keys_pressed = pygame.keys.pressed()
        draw_window()
    pygame.quit()

world, tilemap = civ5map_parser.read_world_data()

images_unscaled = {}
images = {}
for terrain in world.terrain:
    add_image(terrain, 'Assets/Terrain/{}.png'.format(terrain.replace("TERRAIN_", "").lower()))
for feature in world.feature:
    add_image(feature, 'Assets/Feature/{}.png'.format(feature.replace("FEATURE_", "").lower()))
add_image('selected', 'Assets/selected.png')
ingametilemap = []
for row in tilemap:
    ingametilemap.append([])
    for tile in row:
        ingametilemap[-1].append(IngameTile(tile))
current_tile = ingametilemap[0][0]
main()
