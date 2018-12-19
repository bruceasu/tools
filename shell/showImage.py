#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' tk_image_view_url_io.py
display an image from a URL using Tkinter, PIL and data_stream
tested with Python27 and Python33  by  vegaseat  01mar2013
'''

import io
# allows for image formats other than gif
from PIL import Image, ImageTk
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk


root = tk.Tk()
root.wm_attributes('-topmost',1)

fname = 'e:/he.png'
pil_image = Image.open(fname)
pil_image.show()

# optionally show image info
# get the size of the image
w, h = pil_image.size
# split off image file name

sf = "{} ({}x{})".format(fname, w, h)
root.title(sf)

# convert PIL image object to Tkinter PhotoImage object
tk_image = ImageTk.PhotoImage(pil_image)

# put the image on a typical widget
label = tk.Label(root, image=tk_image, bg='brown')
label.pack(padx=5, pady=5)

root.mainloop()


