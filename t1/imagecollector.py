from tkinter import *
# from tkFileDialog import askopenfilename
from PIL import ImageTk, Image

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

root = Tk()

#setting up a tkinter canvas with scrollbars
frame = Frame(root, bd=2, relief=SUNKEN)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

xscroll = Scrollbar(frame, orient=HORIZONTAL)
yscroll = Scrollbar(frame)

xscroll.grid(row=1, column=0, sticky=E+W)
yscroll.grid(row=0, column=1, sticky=N+S)

canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)

xscroll.config(command=canvas.xview)
yscroll.config(command=canvas.yview)

frame.pack(fill=BOTH, expand=1)

#adding the image
# File = askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
file = '/home/aszdrick/Pictures/AREA51.jpg'

source = Image.open(file)
img = ImageTk.PhotoImage(source)
# img = PhotoImage(i)

canvas.create_image(0, 0, image=img, anchor="nw")
canvas.config(scrollregion=canvas.bbox(ALL))

#function to be called when mouse is clicked
def printcoords(event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    #outputting x and y coords to console
    # print(event.x,event.y)
    # print(source)
    canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill='white', outline='white')
    # canvas.create_circle(event.x, event.y, 1, fill="white", outline="white", width=1)
    # source[event.x, event.y] = (1,1,1)

canvas.bind("<B1-Motion>", printcoords)

root.geometry('800x600')
root.mainloop()
