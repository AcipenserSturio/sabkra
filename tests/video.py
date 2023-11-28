import pygame
from pygame._sdl2 import Renderer, Window

HEIGHT, WIDTH = 200, 200

pygame.init()

print("=============================")
print("Found drivers:")
print(list(pygame._sdl2.get_drivers()), sep="\n")

display = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)
window = Window.from_display_module()
renderer = Renderer.from_window(window)


def run():
    while True:
        events = pygame.event.get()
        for e in events:
            if (e.type == pygame.QUIT or e.type == pygame.KEYDOWN
                    and e.key == pygame.K_ESCAPE):
                return

        renderer.draw_color = (255, 40, 40, 255)
        renderer.fill_rect((5, 5, 120, 120))
        renderer.present()


run()
