from window_line_point import *

def main():
    win = Window(1920, 1080)
    maze = Maze(Point(50, 50), 23, 45, 40, win, None)
    win.set_maze(maze)  # Store the maze in the window
    win.root.bind('<space>', win.handle_keypress)  # Bind space key
    win.wait_for_close()

if __name__ == "__main__":
    main()