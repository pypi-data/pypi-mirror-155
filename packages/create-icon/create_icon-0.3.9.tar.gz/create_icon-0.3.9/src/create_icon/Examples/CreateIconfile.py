import os
from tkinter import Tk

root = Tk()
title = (os.path.basename(__file__)[0:-3])
root.title(title.title())
root.geometry('400x200')


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

root.mainloop()
