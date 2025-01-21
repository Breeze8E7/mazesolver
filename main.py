from window_line_point import *

def main():
    win = Window(800, 600)
    #testing info below - no need to keep
    point1 = Point(50, 50)
    point2 = Point(200, 200)
    a_test_cell = Cell(point1, point2, win)
    a_test_cell.has_bottom_wall = False
    a_test_cell.draw()
    point3 = Point(350, 350)
    point4 = Point(500, 500)
    b_test_cell = Cell(point3, point4, win)
    b_test_cell.has_top_wall = False
    b_test_cell.draw()
    b_test_cell.draw_move(a_test_cell, True)
    #testing info above - no need to keep
    win.wait_for_close()

if __name__ == "__main__":
    main()