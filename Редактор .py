from tkinter import *
from tkinter import colorchooser
from Figures import figure
canvas_widht = 1000
canvas_height = 500
brush_size = 3
color = "black"
mouse_first = True # Если True то первая точка линии
line_point = None
lines = []


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


def add_line(p1, p2):
    lines.append(Line(p1, p2))

    
def mouse(event):
    global mouse_first
    global line_point
    x = event.x
    y = event.y
    if mouse_first:
        line_point = (x, y)
    else:
        add_line(line_point, (x, y))
        redraw()
    mouse_first = not mouse_first
    #x1 = event.x - brush_size
    #x2 = event.x + brush_size
    #y1 = event.y - brush_size
    #y2 = event.y + brush_size

def redraw():
    w.delete('all')
    for line in lines:
        w.create_line(line.p1[0], line.p1[1], line.p2[0], line.p2[1], fill=color, width=1)
    #w.create_oval (x1, y1, x2, y2,
     #              fill=color, outline=color)
        
def brush_size_change(new_size):
    global brush_size
    brush_size = new_size

def color_change (new_color):
    global color
    color = new_color

window = Tk()
window.title("Редактор")
#colorchooser.askcolor()
w = Canvas(window,
            width = canvas_widht,
            height= canvas_height,
            bg = "white")
w.bind('<Button-1>', mouse)
#draw()
w.grid(row=2, column=0,
       columnspan=7, padx=5,
       pady=5, sticky=E+W+S+N)
w.columnconfigure(6, weight=1)
w.rowconfigure(2, weight=1)

window.mainloop()
