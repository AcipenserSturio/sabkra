import tkinter as tk
from tkinter import filedialog as fd
from . import world_display
from threading import Thread

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 400
window_height = screen_height

world_display.default_window_width = screen_width - window_width
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
        ('Civilization V Map', '*.Civ5Map'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open',
        initialdir=r"~/.local/share/Aspyr/Sid Meier's Civilization 5/",
        filetypes=filetypes)

    p = Thread(target=world_display.display_world, args=(filename,tile_label))
    p.start()

    print('got here')

open_button = tk.Button(
    root,
    text='Open',
    command=select_file
)
open_button.pack()
tile_label = tk.Label(root, text='')
tile_label.pack()

root.mainloop()
