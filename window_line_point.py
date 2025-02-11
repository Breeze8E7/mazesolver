from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height, bg="black"):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.running = False
        self.canvas = Canvas(self.root, width=width, height=height, bg=bg)
        self.canvas.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.maze = None

    def set_maze(self, maze):
        self.maze = maze

    def handle_keypress(self, event):
        if self.maze:
            self.maze.solve()

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
    def __init__(self, a_point, b_point, window=None):
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
        self.visited = False

    def draw(self):
        if self.win is not None:
            if self.has_bottom_wall == True:
                Line(self.bl_corner, self.br_corner).draw(self.win.canvas, "white")
            else:
                Line(self.bl_corner, self.br_corner).draw(self.win.canvas, "black")

            if self.has_top_wall == True:
                Line(self.tl_corner, self.tr_corner).draw(self.win.canvas, "white")
            else:
                Line(self.tl_corner, self.tr_corner).draw(self.win.canvas, "black")

            if self.has_left_wall == True:
                Line(self.bl_corner, self.tl_corner).draw(self.win.canvas, "white")
            else:
                Line(self.bl_corner, self.tl_corner).draw(self.win.canvas, "black")

            if self.has_right_wall == True:
                Line(self.br_corner, self.tr_corner).draw(self.win.canvas, "white")
            else:
                Line(self.br_corner, self.tr_corner).draw(self.win.canvas, "black")

    def draw_move(self, to_cell, undo=False):
        if self.win is not None:
            color = "black" if undo else "purple"
            Line(self.center, to_cell.center).draw(self.win.canvas, color)

class Maze:
    def __init__(self, point, num_rows, num_cols, cell_size, win=None, seed=None):
        self.starting_point = point
        self.rows = num_rows
        self.columns = num_cols
        self.cell_size = cell_size
        self.win = win
        self.cells = []
        self.create_cells()
        if seed != None:
            random.seed(seed)

    def create_cells(self):
        top_level = []
        for i in range(self.rows):
            bottom_level = []
            for j in range(self.columns):
                x1 = self.starting_point.x + (j * self.cell_size)
                y1 = self.starting_point.y + (i * self.cell_size)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                point1 = Point(x1, y1)
                point2 = Point(x2, y2)
                bottom_level.append(Cell(point1, point2, self.win))
            top_level.append(bottom_level)
        self.cells = top_level
        self.break_entrance_and_exit()
        self.break_walls_recursive(0, 0)
        self.reset_cells_visited()
        for i in range(self.rows):
            for j in range(self.columns):
                self.draw_cell(i, j)
        
    def draw_cell(self, i, j):
        if self.win is not None:
            self.cells[i][j].draw()
            self.animate()
    
    def animate(self):
        if self.win is not None:
            self.win.redraw()
            time.sleep(0.01)

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.cells[self.rows - 1][self.columns - 1].has_bottom_wall = False

    def break_walls_recursive(self, i, j):
        current = self.cells[i][j]
        current.visited = True
        while True:
            neighbors = []
            if j-1 >= 0:
                if self.cells[i][j-1].visited == False:
                    neighbors.append([i, j-1])
            if j+1 < self.columns:
                if self.cells[i][j+1].visited == False:
                    neighbors.append([i, j+1])
            if i+1 < self.rows:
                if self.cells[i+1][j].visited == False:
                    neighbors.append([i+1, j])
            if i-1 >= 0:
                if self.cells[i-1][j].visited == False:
                    neighbors.append([i-1, j])
            if not neighbors:
                return
            next_cell = random.choice(neighbors)
            if next_cell[0] == i and next_cell[1] == j-1:  # Moving LEFT
               current.has_left_wall = False
               self.cells[i][j-1].has_right_wall = False
            elif next_cell[0] == i and next_cell[1] == j+1:  # Moving RIGHT
                current.has_right_wall = False
                self.cells[i][j+1].has_left_wall = False
            elif next_cell[0] == i+1 and next_cell[1] == j:  # Moving DOWN
                current.has_bottom_wall = False
                self.cells[i+1][j].has_top_wall = False
            elif next_cell[0] == i-1 and next_cell[1] == j:  # Moving UP
                current.has_top_wall = False
                self.cells[i-1][j].has_bottom_wall = False
            self.break_walls_recursive(next_cell[0], next_cell[1])

    def reset_cells_visited(self):
        for cells in self.cells:
            for cell in cells:
                cell.visited = False

    #testing only
    def print_visited_status(self):
        for row in self.cells:
            for cell in row:
                print(cell.visited, end=" ")
            print()  # Move to the next row

    def solve(self):
        return self.solve_recursive(0,0)
    
    def solve_recursive(self, i, j):
        current_cell = self.cells[i][j]
        goal_cell = self.cells[self.rows - 1][self.columns - 1]
        self.animate()
        current_cell.visited = True
        if current_cell == goal_cell:
            return True
        if current_cell.has_left_wall == False:    
            if j-1 >= 0:
                if self.cells[i][j-1].visited == False:
                    current_cell.draw_move(self.cells[i][j-1])
                    if self.solve_recursive(i,j-1):
                        return True
                    else:
                        current_cell.draw_move(self.cells[i][j-1], undo=True)
        if current_cell.has_right_wall == False:            
            if j+1 < self.columns:
                if self.cells[i][j+1].visited == False:
                    current_cell.draw_move(self.cells[i][j+1])
                    if self.solve_recursive(i,j+1):
                        return True
                    else:
                        current_cell.draw_move(self.cells[i][j+1], undo=True)
        if current_cell.has_bottom_wall == False:    
            if i+1 < self.rows:
                if self.cells[i+1][j].visited == False:
                    current_cell.draw_move(self.cells[i+1][j])
                    if self.solve_recursive(i+1,j):
                        return True
                    else:
                        current_cell.draw_move(self.cells[i+1][j], undo=True)
        if current_cell.has_top_wall == False:    
            if i-1 >= 0:
                if self.cells[i-1][j].visited == False:
                    current_cell.draw_move(self.cells[i-1][j])
                    if self.solve_recursive(i-1,j):
                        return True
                    else:
                        current_cell.draw_move(self.cells[i-1][j], undo=True)
        return False