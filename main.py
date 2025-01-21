from window_line_point import *

def main():
    win = Window(800, 600)
    #testing info below - no need to keep
    point1 = Point(50, 50)
    point2 = Point(200, 200)
    line1 = Line(point1, point2)
    win.draw_line(line1, "black")
    point3 = Point(69, 420)
    line2 = Line(point2, point3)
    win.draw_line(line2, "red")
    #testing info above - no need to keep
    win.wait_for_close()

if __name__ == "__main__":
    main()