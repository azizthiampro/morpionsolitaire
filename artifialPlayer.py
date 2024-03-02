import numpy as np

# Initialize a 20x20 grid with zeros
grid = np.zeros((20, 20), dtype=int)

score=0
# Define the points for a Greek cross
cross_points = [
    (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5),
    (14, 8), (13, 8), (12, 8), (11, 8), (11, 7), (11, 6), (11, 5),
    (10, 5), (9, 5), (5, 9), (5, 10), (5, 11), (14, 9), (14, 10), (14, 11), (13, 11),
    (12, 11), (11, 11), (6, 11), (7, 11), (8, 11), (8, 12), (8, 13), (8, 14), (11, 12),
    (11, 13), (11, 14), (9, 14), (10, 14)
]

# Mark the points for the Greek cross on the grid
for x, y in cross_points:
    grid[x, y] = 1

# List to store previously chosen cells
previous_cells = []

played_sequences = []





def print_grid(grid, previous_cells):
    for i, row in enumerate(grid):
        # Print row index
        print(f"{i:2d} ", end="")
        for j, val in enumerate(row):
            if (i, j) in previous_cells:
                print(" \033[93m#\033[0m", end=" ")  # Print previously chosen cell with yellow '#'
            elif val == 1:
                print(" \033[91m#\033[0m", end=" ")  # ANSI escape code for red color
            else:
                print(" .", end=" ")
            # Print legend numbers for each column
            print(f"{j:2d}", end="")
        print()
 # New line after each row

def is_adjacent_to_chosen_or_cross(row, col):
    relevant_points = cross_points + previous_cells
    for point in relevant_points:
        if abs(point[0] - row) <= 1 and abs(point[1] - col) <= 1:
            return True
    return False

def is_adjacent_to_chosen_or_cross(row, col, cross_points, previous_cells):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (row + dx, col + dy) in cross_points or (row + dx, col + dy) in previous_cells:
                return True
    return False


def validate_sequence(chosen_cell, start_row, start_col, end_row, end_col, cross_points, previous_cells):
    # Initialize sequence coordinates
    sequence_coordinates = []

    # Determine direction of the sequence
    if start_row == end_row:  # Horizontal
        step = 1 if end_col > start_col else -1
        for i in range(start_col, end_col + step, step):
            sequence_coordinates.append((start_row, i))
    elif start_col == end_col:  # Vertical
        step = 1 if end_row > start_row else -1
        for i in range(start_row, end_row + step, step):
            sequence_coordinates.append((i, start_col))
    elif abs(start_row - end_row) == abs(start_col - end_col):  # Diagonal
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        for i in range(abs(end_row - start_row) + 1):
            sequence_coordinates.append((start_row + i * row_step, start_col + i * col_step))
    else:
        return False, "Sequence must be horizontal, vertical, or diagonal.", []

    # Check if the chosen cell is within the sequence and the sequence contains valid cells
    if chosen_cell not in sequence_coordinates:
        return False, "Chosen cell is not part of the sequence.", []

    valid_cells_count = sum(
        cell in cross_points or cell in previous_cells or cell == chosen_cell for cell in sequence_coordinates)

    # Ensure the sequence is exactly 5 cells and all are valid
    if len(sequence_coordinates) == 5 and valid_cells_count == 5:
        return True, "Sequence is valid", sequence_coordinates
    else:
        return False, "Sequence does not contain exactly 5 valid cells or contains invalid cells.", []


def choose_cell_and_sequence():
    try:
        chosen_row, chosen_col = map(int, input("Enter chosen cell row and column numbers (0-19), separated by a space: ").split())
        if not is_adjacent_to_chosen_or_cross(chosen_row, chosen_col, cross_points, previous_cells):
            print("Bad Move Try again")
            return None, None  # Ensure function returns a tuple even in case of error
        start_row, start_col = map(int, input("Enter start cell row and column numbers for the sequence (0-19), separated by a space: ").split())
        end_row, end_col = map(int, input("Enter end cell row and column numbers for the sequence (0-19), separated by a space: ").split())

        return (chosen_row, chosen_col), (start_row, start_col, end_row, end_col)
    except ValueError:
        print("Error: Please enter integers for row and column numbers.")
        return None, None  # Ensure function returns a tuple even in case of error

# Initial display of the grid
print("Welcome to the game! Here's the current grid:")
print_grid(grid, previous_cells)

# Game loop
while True:
    chosen_cell, sequence_input = choose_cell_and_sequence()
    if chosen_cell and sequence_input:
        start_row, start_col, end_row, end_col = sequence_input
        # Directly use the chosen_cell for validation against cross_points and previous_cells
        if chosen_cell in cross_points or chosen_cell in previous_cells:
            print("Error: Chosen cell is already marked. Please choose another cell.")
            continue

        valid, message, sequence_coords = validate_sequence(chosen_cell, start_row, start_col, end_row, end_col,
                                                            cross_points, previous_cells)
        if valid:
            previous_cells.append(chosen_cell)
            played_sequences.extend(sequence_coords)  # Store the valid sequence of coordinates
            score += 1
            print(f"Chosen cell: {chosen_cell}, Valid Sequence: {sequence_coords}")
            print("Your score is: \033[94m" + str(score) + "\033[0m")
            print_grid(grid, previous_cells)
        else:
            print("Error:", message)
    else:
        print("Thank you for playing!")
        break
