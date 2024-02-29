import numpy as np

# Create a 20x20 grid initialized with zeros
grid = np.zeros((20, 20), dtype=int)

# Marking the points in a Greek cross
cross_points = [
    (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5),
    (14, 8), (13, 8), (12, 8), (11, 8), (11, 7), (11, 6), (11, 5),
    (10, 5), (9, 5), (5, 9), (5, 10), (5, 11), (14, 9), (14, 10), (14, 11), (13, 11),
    (12, 11), (11, 11), (6, 11), (7, 11), (8, 11), (8, 12), (8, 13), (8, 14), (11, 12),
    (11, 13), (11, 14), (9, 14), (10, 14)
]

# Setting the marked points to 1
for x, y in cross_points:
    grid[x, y] = 1

# Function to print the grid with red color for 1s
def print_grid_with_color(grid):
    for row in grid:
        for val in row:
            if val == 1:
                print("\033[91m" + str(val) + "\033[0m", end=" ")  # ANSI escape code for red color
            else:
                print(val, end=" ")
        print()

print_grid_with_color(grid)
