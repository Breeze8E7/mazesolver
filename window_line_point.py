from tkinter import Tk, BOTH, Canvas
import time

class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.running = False
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()
            time.sleep(0.01)
    
    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y    

class Line:
    def __init__(self, point_a, point_b):
        self.a = point_a
        self.b = point_b

    def draw(self, canvas, fill_color):
        canvas.create_line(self.a.x, self.a.y, self.b.x, self.b.y, fill=fill_color, width=2)
         
class Cell:
    def __init__(self, a_point, b_point, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.x1 = a_point.x
        self.y1 = a_point.y
        self.x2 = b_point.x
        self.y2 = b_point.y
        self.tl_corner = a_point
        self.br_corner = b_point
        self.tr_corner = Point(b_point.x, a_point.y)
        self.bl_corner = Point(a_point.x, b_point.y)
        self.center = Point(((a_point.x + b_point.x) // 2), ((a_point.y + b_point.y) // 2))
        self.win = window

    def draw(self):
        if self.has_bottom_wall == True:
            Line(self.bl_corner, self.br_corner).draw(self.win.canvas, "black")
        if self.has_top_wall == True:
            Line(self.tl_corner, self.tr_corner).draw(self.win.canvas, "black")
        if self.has_left_wall == True:
            Line(self.bl_corner, self.tl_corner).draw(self.win.canvas, "black")
        if self.has_right_wall == True:
            Line(self.br_corner, self.tr_corner).draw(self.win.canvas, "black")

    def draw_move(self, to_cell, undo=False):
        color = "gray" if undo else "red"
        Line(self.center, to_cell.center).draw(self.win.canvas, color)

class Maze:
    def __init__(self, point, num_rows, num_cols, cell_size, win):
        self.starting_point = point
        self.rows = num_rows
        self.columns = num_cols
        self.cell_size = cell_size
        self.win = win
        self.cells = []
        self.create_cells()

    def create_cells(self):
        top_level = []
        for i in range(self.columns):
            bottom_level = []
            for j in range(self.rows):
                x1 = self.starting_point.x + (i * self.cell_size)
                y1 = self.starting_point.y + (j * self.cell_size)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                point1 = Point(x1, y1)
                point2 = Point(x2, y2)
                bottom_level.append(Cell(point1, point2, self.win))
            top_level.append(bottom_level)
        self.cells = top_level
        for i in range(self.columns):
            for j in range(self.rows):
                self.draw_cell(i, j)

    def draw_cell(self, i, j):
        self.cells[i][j].draw()
        self.animate()
    
    def animate(self):
        self.win.redraw()
        time.sleep(0.05)
