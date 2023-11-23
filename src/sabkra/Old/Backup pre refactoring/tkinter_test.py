import tkinter as tk
from tkinter import filedialog as fd
import world_display
from threading import Thread

root = tk.Tk()
root.geometry('300x500')

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
        initialdir=r"C:\Users\Максим\Documents\My Games\Sid Meier's Civilization 5\Maps",
        filetypes=filetypes)

    p = Thread(target=world_display.display_world, args=(filename,))
    p.start()

    print('got here')

open_button = tk.Button(
    root,
    text='Open',
    command=select_file
)
open_button.pack(expand=True)

root.mainloop()
