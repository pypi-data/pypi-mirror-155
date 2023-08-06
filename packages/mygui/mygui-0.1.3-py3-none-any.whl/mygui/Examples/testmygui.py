import os
from tkinter import Tk

from mygui import egrid, lgrid

root = Tk()
root.minsize(300, 100)
lgrid(root, 'Label placed in grid 0,0', 0, 0, padx=15)
lgrid(root, 'Label placed in grid 1,1', 0, 1)
egrid(root, 2, 0, padx=15)
root.mainloop()
