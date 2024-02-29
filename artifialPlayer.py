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

# Function to print the grid with red color for 1s and legend numbers
def print_grid_with_color_and_legend(grid, chosen_row=None, chosen_col=None):
    for i, row in enumerate(grid):
        # Print row index
        print(f"{i:2d} ", end="")
        for j, val in enumerate(row):
            if i == chosen_row and j == chosen_col:
                print("\033[92m#\033[0m", end=" ")  # Print chosen cell with green '#'
            elif val == 1:
                print("\033[91m#\033[0m", end=" ")  # ANSI escape code for red color
            else:
                print(".", end=" ")
            # Print legend numbers for each column
            print(f"{j:2d}", end="")
        print()

# Function to allow a player to choose a cell
def choose_cell():
    while True:
        try:
            row = int(input("Enter row number (0-19): "))
            col = int(input("Enter column number (0-19): "))
            if 0 <= row <= 19 and 0 <= col <= 19:
                return row, col
            else:
                print("Please enter valid row and column numbers (0-19).")
        except ValueError:
            print("Please enter integers for row and column numbers.")

# Print the grid with color and legend numbers
print_grid_with_color_and_legend(grid)

# Allow the player to choose a cell
chosen_row, chosen_col = choose_cell()
print(f"You chose cell ({chosen_row}, {chosen_col}).")

# Print the grid with the chosen cell marked
print_grid_with_color_and_legend(grid, chosen_row, chosen_col)
