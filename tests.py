from window_line_point import *
import unittest

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_rows = 10
        num_cols = 16
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10)
        self.assertEqual(
            len(m1.cells),  # The number of rows in the grid.
            num_rows,       # Should match the number of rows.
        )
        self.assertEqual(
            len(m1.cells[0]),  # The number of columns in a row.
            num_cols,          # Should match the number of columns.
        )

if __name__ == "__main__":
    unittest.main()