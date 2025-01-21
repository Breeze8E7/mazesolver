from window_line_point import *

def main():
    win = Window(800, 600)
    #testing info below - no need to keep
    maze = Maze(Point(50, 50), 10, 8, 40, win)
    #testing info above - no need to keep
    win.wait_for_close()

if __name__ == "__main__":
    main()