from tkinter import *
from PIL import ImageTk, Image
import numpy as np

def collect(path):
    window = Tk()
    source = Image.open(path)
    pixels = source.load()
    img = ImageTk.PhotoImage(source)
    border = 15

    width, height = source.size
    swidth = min(window.winfo_screenwidth(), width + border)
    sheight = min(window.winfo_screenheight(), height + border)

    window.maxsize(width=width + border, height=height + border)
    window.geometry('%dx%d' % (swidth,  sheight))

    xscroll = Scrollbar(window, orient=HORIZONTAL)
    yscroll = Scrollbar(window)

    yscroll.pack(side=RIGHT, fill=Y)
    xscroll.pack(side=BOTTOM, fill=X)

    canvas = Canvas(window, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)

    canvas.pack(fill=BOTH, expand=YES)

    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    sample = {}
    def collect_pixels(event):
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)

        for i in range(-1, 2):
            for j in range(-1, 2):
                nx = x + i
                ny = y + j
                if nx >= 0 and nx < width and ny >= 0 and ny < height:
                    sample[nx, ny] = (pixels[nx, ny])
        
        if x >= 0 and x < width and y >= 0 and y < height:
            canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill='white', outline='white')

    canvas.bind("<B1-Motion>", collect_pixels)

    window.mainloop()

    data = {}
    for x in range(width):
        for y in range(height):
            data[x, y] = pixels[x, y]
    # array = np.array(source)
    # data = list(tuple(pixel) for pixel in array)
    # print(width, height)
    # print(len(array))
    # print(len(array[0]))
    # print(len(data))
    # print(len(data[0]))
    return (sample, data)

# print(collect_sample('datasets/flowers.jpg')[0])
