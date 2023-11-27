import os
import pygame

from .scene import Scene

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 25)


fps = 60


def display_world_tk(file_path, ui, frame):
    sc = Scene(file_path, ui)

    def on_click(event):
        sc.set_current_tile_to_mouse((event.x, event.y))

    def on_click_drag(event):
        sc.mouse.update(event.x, event.y)
        sc.set_current_tile_to_mouse((event.x, event.y))

    def on_motion(event):
        sc.mouse.update(event.x, event.y)

    def on_drag(event):
        sc.mouse.update(event.x, event.y)
        sc.camera.drag(sc.mouse.vector())

    def on_zoom_in(event):
        sc.camera.clean_rescale(1)
        sc.draw()

    def on_zoom_out(event):
        sc.camera.clean_rescale(-1)
        sc.draw()

    frame.bind('<Button-1>', on_click)
    frame.bind('<B1-Motion>', on_click_drag)
    frame.bind('<B3-Motion>', on_drag)
    frame.bind('<Motion>', on_motion)
    # TODO: Windows scroll support
    frame.bind("<Button-4>", on_zoom_in)
    frame.bind("<Button-5>", on_zoom_out)

    sc.draw()


def display_world(file_path, ui):
    sc = Scene(file_path, ui)

    clock = pygame.time.Clock()
    drag_mode = False
    run = True
    while run:
        clock.tick(fps)
        # print(clock)
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                # Close the window
                run = False
            if event.type == pygame.VIDEORESIZE:
                # Resize the window
                sc.on_resize_window(event.w, event.h)
            if event.type == pygame.MOUSEWHEEL:
                # Wheel scroll
                sc.camera.clean_rescale(event.y)
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
                    sc.set_current_tile_to_mouse(event.pos)
                else:
                    # Left click / wheel click ended
                    drag_mode = False
        if drag_mode:
            sc.camera.drag(sc.mouse.vector())
        sc.mouse.update(*pygame.mouse.get_pos())
        sc.draw()
    pygame.display.quit()
