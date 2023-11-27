import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from . import world_display
import os
import platform

root = tk.Tk()
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
        ("Civilization V Map", "*.civ5map"),
        ("All files", "*.*")
    )

    filename = fd.askopenfilename(
        title="Open",
        initialdir=r"~/.local/share/Aspyr/Sid Meier's Civilization 5/MODS/gedemon's ynaemp (v 25)/",
        filetypes=filetypes
    )
    root.title(f"Sabkra - {filename}")
    world_display.display_world_tk(filename, update_sidebar, pygame_frame)


def update_sidebar(sprite):
    sidebar_1["text"] = f"Plot: ({sprite.tile.row}, {sprite.tile.col})"
    sidebar_2["values"] = sprite.tile.world.terrain
    sidebar_2.set(sprite.tile.get_terrain())
    sidebar_3["values"] = sprite.tile.world.elevation
    sidebar_3.set(sprite.tile.get_elevation())
    sidebar_4["values"] = ["", *sprite.tile.world.feature]
    sidebar_4.set(sprite.tile.get_feature())
    sidebar_5["values"] = ["", *sprite.tile.world.resource]
    sidebar_5.set(sprite.tile.get_resource())


menu = tk.Menu(root)
root.config(menu=menu)
menu.add_command(
    label="Open",
    command=select_file
)
pygame_frame = tk.Frame(
    root,
    width=window_width - sidebar_width,
    height=window_height,
)
sidebar_frame = tk.Frame(
    root,
    width=sidebar_width,
    height=window_height,
    padx=15,
    pady=15,
)
sidebar_1 = ttk.Label(sidebar_frame)
sidebar_1.pack()
sidebar_2_var = tk.StringVar()
sidebar_2 = ttk.Combobox(sidebar_frame, state="readonly", textvariable=sidebar_2_var)
sidebar_2.pack(fill="x")
sidebar_3_var = tk.StringVar()
sidebar_3 = ttk.Combobox(sidebar_frame, state="readonly", textvariable=sidebar_3_var)
sidebar_3.pack(fill="x")
sidebar_4_var = tk.StringVar()
sidebar_4 = ttk.Combobox(sidebar_frame, state="readonly", textvariable=sidebar_4_var)
sidebar_4.pack(fill="x")
sidebar_5_var = tk.StringVar()
sidebar_5 = ttk.Combobox(sidebar_frame, state="readonly", textvariable=sidebar_5_var)
sidebar_5.pack(fill="x")
pygame_frame.pack(side="left", fill="both")
sidebar_frame.pack_propagate(False)
sidebar_frame.pack(side="right", fill="both")


os.environ["SDL_WINDOWID"] = str(pygame_frame.winfo_id())
os.environ["SDL_VIDEODRIVER"] = ("windib" if platform.system() == "Windows"
                                 else "x11")

root.mainloop()
