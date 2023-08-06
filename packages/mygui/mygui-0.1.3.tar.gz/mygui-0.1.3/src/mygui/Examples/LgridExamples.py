
import os

import create_icon

try:

    from mygui import lgrid
except:
    os.system('pip install mygui --upgrade')
    from mygui import lgrid

from tkinter import Tk

root = Tk()

# Add Icon to window Titlebar
if os.name == 'nt':
    homepath = os.path.expanduser('~')
    tempFile = '%s\Caveman Software\%s' % (homepath, 'Icon\icon.ico')

    if (os.path.exists(tempFile) == True):
        root.wm_iconbitmap(default=tempFile)

    else:
        import create_icon
        print('File Created')
        root.wm_iconbitmap(default=tempFile)

root.minsize(300, 100)

lgrid(root, 'Label placed in grid 5,5', 5, 5)
lgrid(root, 'Label placed in grid 6,6', 6, 6)

root.mainloop()
