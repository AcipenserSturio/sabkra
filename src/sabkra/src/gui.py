import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from ttkthemes import ThemedTk
from . import world_display
import os
import platform

root = ThemedTk(theme="breeze")
root.title("Sabkra - Civ 5 World previewer")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width
window_height = screen_height - 50

sidebar_width = 250

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

    root.title(f"Sabkra - {filename}")
    world_display.display_world_tk(filename, update_sidebar, pygame_frame)


def update_sidebar(tile):
    sidebar_1["text"] = f"Plot: ({tile.row}, {tile.col})"
    sidebar_2["text"] = f"Terrain: {tile.get_terrain()}"
    sidebar_3["text"] = f"Features: {tile.get_feature()}"
    sidebar_4["text"] = f"Elevation: {tile.get_elevation()}"
    sidebar_5["text"] = f"Resources: {tile.get_resource()}"


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
sidebar_1 = ttk.Label(sidebar_frame)
sidebar_1.pack()
sidebar_2 = ttk.Label(sidebar_frame)
sidebar_2.pack()
sidebar_3 = ttk.Label(sidebar_frame)
sidebar_3.pack()
sidebar_4 = ttk.Label(sidebar_frame)
sidebar_4.pack()
sidebar_5 = ttk.Label(sidebar_frame)
sidebar_5.pack()
pygame_frame.pack(side="left", fill="both")
sidebar_frame.pack_propagate(False)
sidebar_frame.pack(side="right", fill="both")


os.environ['SDL_WINDOWID'] = str(pygame_frame.winfo_id())
os.environ['SDL_VIDEODRIVER'] = ('windib' if platform.system() == "Windows"
                                 else 'x11')

root.mainloop()
