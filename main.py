from window_line_point import *

def main():
    win = Window(1920, 1080)
    #testing info below - no need to keep
    maze = Maze(Point(50, 50), 23, 45, 40, win, None)
    #testing info above - no need to keep
    win.wait_for_close()

if __name__ == "__main__":
    main()