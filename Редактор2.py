from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from Figures import Line
from math import *
canvas_widht = 1000
canvas_height = 500
brush_size = 3
color = "black"
mouse_first = True # Если True то первая точка линии
line_point = None
rectangle_point = None
figures = []
selected_figure = None
left_button = False
dx = 0
dy = 0


LINES = 1
RECTANGLES = 2
CIRCLES = 3
SELECTION = 4
MOVE = 5
tool = SELECTION


class Figure:
    def __init__(self, p1, p2, color):
        self.p1 = p1
        self.p2 = p2
        self.color = color

    def cross(self, x, y):
        """
        Функция проверки пересечения фигуры и курсора

        :param x: координата x курсора
        :param y: координата y курсора
        :return: True если пересекает, иначе False
        """
        #print(x, y, self.p1, self.p2)
        min_x = min(self.p1[0], self.p2[0])
        min_y = min(self.p1[1], self.p2[1])
        max_x = max(self.p1[0], self.p2[0])
        max_y = max(self.p1[1], self.p2[1])
        return x >= min_x and x <= max_x and y >= min_y and y <= max_y

        
class Line(Figure):
    pass
        
class Rectangle(Figure):
    def __init__(self, p1, p2, color, border_color=color):
        super().__init__(p1, p2, color)
        self.p4 = (self.p1[0], self.p2[1])
        self.p3 = self.p2
        self.p2 = (self.p2[0], self.p1[1])
        self.border_color = color
        
    def cross(self, x, y):
        min_x = min(self.p1[0], self.p3[0])
        min_y = min(self.p1[1], self.p3[1])
        max_x = max(self.p1[0], self.p3[0])
        max_y = max(self.p1[1], self.p3[1])
        return x >= min_x and x <= max_x and y >= min_y and y <= max_y

class Circle(Rectangle):
    def __init__(self, p1, p2, color, border_color=color):
        
        super().__init__(p1, p2,color) 
        radius = p2[0] - p1[0]#int(math.sqrt((p2[0] - p1[0])^2 + (p2[1] - p1[1])^2))
        self.p1 = (self.p1[0] - radius, self.p1[1] - radius)
        self.p2 = (self.p1[0] + 2 * radius, self.p1[1] + 2 * radius)

def add_figure(p1, p2):
    print(f'figures = {figures}')
    if tool == LINES:
        figures.append(Line(p1, p2, color))
    elif tool == RECTANGLES:
        figures.append(Rectangle(p1, p2, color))
    elif tool == CIRCLES:
        figures.append(Circle(p1, p2, color))
    
    
def create_figure(event):
    global mouse_first
    global line_point
    x = event.x
    y = event.y
    if mouse_first:
        line_point = (x, y)
    else:
        add_figure(line_point, (x, y))
        redraw()
    mouse_first = not mouse_first


def draw_figure(figure):
    if figure == selected_figure:
        color = 'red'
    else:
        color = figure.color
    if isinstance(figure, Line):
        w.create_line(figure.p1[0], figure.p1[1], figure.p2[0],
                          figure.p2[1], fill=color, width=1)
    elif isinstance(figure, Circle):
            w.create_oval(figure.p1[0], figure.p1[1], figure.p2[0],
                          figure.p2[1], fill=color, width=1)
    elif isinstance(figure, Rectangle):
            w.create_polygon(figure.p1[0], figure.p1[1],
                             figure.p2[0],figure.p2[1],
                             figure.p3[0], figure.p3[1],
                             figure.p4[0],figure.p4[1],

                             fill=color, width=1)

def redraw():
    w.delete('all')
    #print('sel', selected_figure)
    for figure in figures:
        draw_figure(figure)
        

def brush_size_change(new_size):
    global brush_size
    brush_size = new_size

def color_change (new_color):
    global color
    color = new_color

def keydown(e):
    global tool
    global mouse_first
    mouse_first = True
    if e.char == 'r':
        tool = RECTANGLES
    elif e.char == 'l':
        tool = LINES
    elif e.char == 'c':
        tool = CIRCLES
    elif e.char == 's':
        tool = SELECTION
    elif e.char == "m":
        tool = MOVE
        
def RemoveAll():
    w.delete('all')
    figures.clear()

def ColorChange():
    global color
    global selected_figure
    
    change = colorchooser.askcolor()
    if selected_figure == None:
        color = change[1]
    elif selected_figure != None:
        selected_figure.color = change[1]
        selected_figure = None
        redraw()

def mouse_down(e):
    global selected_figure
    global left_button
    global dx, dy
    left_button = True
    if selected_figure != None:
        dx = e.x - selected_figure.p1[0]
        dy = e.y - selected_figure.p1[1]
    if tool != SELECTION and tool != MOVE:
        create_figure(e)
    else:
        selected_figure = None
        for i in range(len(figures) - 1, -1, -1):
            f = figures[i]
            if f.cross(e.x, e.y):
                selected_figure = f
                break
        redraw()

def mouse_up(e):
    global left_button
    left_button = False
    
def mouse_move(e):
    if selected_figure != None and left_button:
        if tool == MOVE:
            w = selected_figure.p2[0] - selected_figure.p1[0]
            h = selected_figure.p2[1] - selected_figure.p1[1]
            selected_figure.p1 = (e.x - dx, e.y - dy)
            selected_figure.p2 = (e.x + w - dx, e.y + h - dy)
        elif tool == ROTATE:
            selected_figure.rotate(e.y - dy)
        redraw()
        

def Remove():
    if selected_figure != None:
        figures.remove(selected_figure)
        redraw()
        

    
window = Tk()
window.title("Редактор")
toolbar = Frame(window, bd=1, relief=RAISED)
toolbar.grid(row=0, column=0,
       columnspan=7, padx=5,
       pady=5, sticky=E+W+S+N)
but_del = Button(toolbar, text = "Remove all", command = RemoveAll)
but_del.pack(side=LEFT)

but_del = Button(toolbar, text = "Change color", command = ColorChange)
but_del.pack(side=LEFT)

but_del = Button(toolbar, text = "Remove", command = Remove)
but_del.pack(side=LEFT)


w = Canvas(window,
            width = canvas_widht,
            height= canvas_height,
            bg = "white")
w.bind('<ButtonPress>', mouse_down)
w.bind('<ButtonRelease>', mouse_up)
window.bind("<KeyPress>", keydown)
w.bind("<Motion>", mouse_move)


w.grid(row=2, column=0,
       columnspan=7, padx=5,
       pady=5, sticky=E+W+S+N)
w.columnconfigure(6, weight=1)
w.rowconfigure(2, weight=1)

window.mainloop()
