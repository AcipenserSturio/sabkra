import os
import pygame

from .display.scene import Scene

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 25)


fps = 60


def on_event(event):
    print(event)


def display_world(file_path, ui, frame):
    wb = Scene(file_path, ui)

    if frame:
        frame.bind('<Enter>', on_event)
        frame.bind('<Leave>', on_event)
        frame.bind('<Motion>', on_event)
        frame.bind('<B1-Motion>', on_event)
        frame.bind('<B2-Motion>', on_event)
        frame.bind('<B3-Motion>', on_event)

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
