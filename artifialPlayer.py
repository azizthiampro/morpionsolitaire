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

def print_grid(grid, previous_cells):
    for i, row in enumerate(grid):
        # Print row index
        print(f"{i:2d} ", end="")
        for j, val in enumerate(row):
            if (i, j) in previous_cells:
                print("\033[93m#\033[0m", end=" ")  # Print previously chosen cell with yellow '#'
            elif val == 1:
                print("\033[91m#\033[0m", end=" ")  # ANSI escape code for red color
            else:
                print(".", end=" ")
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

def validate_sequence(start_row, start_col, end_row, end_col):
    # Determine the direction of the sequence
    if start_row == end_row:
        direction = 'horizontal'
        step = 1 if end_col >= start_col else -1
    elif start_col == end_col:
        direction = 'vertical'
        step = 1 if end_row >= start_row else -1
    elif abs(start_row - end_row) == abs(start_col - end_col):
        if start_row < end_row:
            direction = 'diagonal_down' if start_col < end_col else 'diagonal_up'
        else:
            direction = 'diagonal_up' if start_col < end_col else 'diagonal_down'
        step = 1 if end_col >= start_col else -1
    else:
        return False, "Sequence must be horizontal, vertical, or diagonal."

    # Validate sequence length
    length = max(abs(end_row - start_row), abs(end_col - start_col)) + 1
    if length != 5:
        return False, "Sequence must contain exactly 5 cells."

    # Validate each cell in the sequence
    for i in range(5):
        if direction == 'horizontal':
            row, col = start_row, start_col + i * step
        elif direction == 'vertical':
            row, col = start_row + i * step, start_col
        elif direction in ['diagonal_down', 'diagonal_up']:
            row_increment = i if direction == 'diagonal_down' else -i
            row, col = start_row + row_increment, start_col + i * step

        if not is_adjacent_to_chosen_or_cross(row, col) and (row, col) not in previous_cells and (row, col) not in cross_points:
            return False, f"Cell at ({row}, {col}) is not adjacent to chosen or Greek cross points."

    return True, ""

def choose_cell_and_sequence():
    while True:
        try:
            chosen_row, chosen_col = map(int, input("Enter chosen cell row and column numbers (0-19), separated by a space: ").split())
            start_row, start_col = map(int, input("Enter start cell row and column numbers for the sequence (0-19), separated by a space: ").split())
            end_row, end_col = map(int, input("Enter end cell row and column numbers for the sequence (0-19), separated by a space: ").split())

            if not (0 <= chosen_row <= 19 and 0 <= chosen_col <= 19 and 0 <= start_row <= 19 and 0 <= start_col <= 19 and 0 <= end_row <= 19 and 0 <= end_col <= 19):
                print("Error: Please enter valid numbers for row and column (0-19).")
                continue

            if (chosen_row, chosen_col) in cross_points or (chosen_row, chosen_col) in previous_cells:
                print("Error: Chosen cell is already marked. Please choose another cell.")
                continue

            valid, message = validate_sequence(start_row, start_col, end_row, end_col)
            if not valid:
                print("Error: " + message)
                continue

            # If the sequence is valid, break from the loop
            return (chosen_row, chosen_col), (start_row, start_col, end_row, end_col)
        except ValueError:
            print("Error: Please enter integers for row and column numbers.")

# Initial display of the grid
print("Welcome to the game! Here's the current grid:")
print_grid(grid, previous_cells)

# Game loop
while True:
    chosen_cell, sequence = choose_cell_and_sequence()
    if chosen_cell and sequence:
        # Update the game state based on the chosen cell and sequence
        previous_cells.append(chosen_cell)
        # Update the grid based on the sequence
        print(f"Chosen cell: {chosen_cell}, Sequence: {sequence}")
        score+=1
        print("Your score is: \033[94m" + str(score) + "\033[0m")
        print_grid(grid, previous_cells)  # Display the updated grid
    else:
        print("Thank you for playing!")
        break
