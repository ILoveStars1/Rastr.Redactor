class figure():
    def _init_(self):
        line_start = (0,0)

    def Line(self, event):
        x, y = event.x, event.y
        if not self.line_start:
            self.line_start = (x, y)
        else:
            x_origin, y_origin = self.line_start
            self.line_start = None
            line = (x_origin, y_origin, x, y)
            arrow = self.form.get_arrow()
            color = self.form.get_color()
            width = self.form.get_width()
            self.canvas.create_line(*line, arrow=arrow, fill=color, width=width)


    def Circle():
        origin = (x1, y1)

    def Rectangle():
        origin = (x1, y1)
