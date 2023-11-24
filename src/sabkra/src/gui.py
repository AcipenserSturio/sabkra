import tkinter as tk
from tkinter import filedialog as fd
from . import world_display
from threading import Thread
import os
import platform

root = tk.Tk()
root.title("Sabkra - Civ 5 World previewer")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width
window_height = screen_height - 50

sidebar_width = 500

world_display.default_window_width = screen_width
world_display.default_window_height = screen_height - 50

# calculate x and y coordinates for the Tk root window
x = screen_width - window_width
y = screen_height - window_height

# set the dimensions of the screen
# and where it is placed
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))


"""label1 = Label(root, text="Hello World!")
label2 = Label(root, text="First program yo")
label1.grid(row=0, column=0)
label2.grid(row=1, column=0)"""


def select_file():
    filetypes = (
        ('Civilization V Map', '*.civ5map'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open',
        initialdir=r"~/.local/share/Aspyr/Sid Meier's Civilization 5/MODS/gedemon's ynaemp (v 25)/",
        filetypes=filetypes)

    p = Thread(target=world_display.display_world, args=(filename, tile_label))
    p.start()

    print('got here')


menu = tk.Menu(root)
root.config(menu=menu)
menu.add_command(
    label='Open',
    command=select_file
)
pygame_frame = tk.Frame(
    root,
    width=window_width - sidebar_width,
    height=window_height,
    highlightbackground='#595959',
    highlightthickness=2,
)
sidebar_frame = tk.Frame(
    root,
    width=sidebar_width,
    height=window_height,
    highlightbackground='#595959',
    highlightthickness=2,
)
tile_label = tk.Message(sidebar_frame, text='')
tile_label.pack(fill=None, expand=False)
pygame_frame.pack(side="left", fill="both")
sidebar_frame.pack(side="right", fill="both")

os.environ['SDL_WINDOWID'] = str(pygame_frame.winfo_id())
system = platform.system()
if system == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'
elif system == "Linux":
    os.environ['SDL_VIDEODRIVER'] = 'x11'

root.mainloop()
