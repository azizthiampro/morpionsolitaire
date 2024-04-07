EMPTY = "."
CROSS = "X"

# Initialize the board
board_size = 20
board = [[EMPTY for _ in range(board_size)] for _ in range(board_size)]

# Place crosses on predefined cross points
# Place crosses on predefined cross points
cross_points = [
    (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5),
    (14, 8), (13, 8), (12, 8), (11, 8), (11, 7), (11, 6), (11, 5),
    (10, 5), (9, 5), (5, 9), (5, 10), (5, 11), (14, 9), (14, 10), (14, 11), (13, 11),
    (12, 11), (11, 11), (6, 11), (7, 11), (8, 11), (8, 12), (8, 13), (8, 14), (11, 12),
    (11, 13), (11, 14), (9, 14), (10, 14)
]
for x, y in cross_points:
    board[x][y] = CROSS

played_sequences = []  # Stores dictionaries for each line: {'coords': [(x1, y1),...], 'direction': (dx, dy)}
chosen_cell = None
last_added_cell = None



def print_board():
    RED = '\033[91m'  # ANSI color code for red
    print("   " + " ".join([chr(ord('A') + i) for i in range(board_size)]))
    for i, row in enumerate(board):
        row_str = ""
        for j, cell in enumerate(row):
            if (i, j) in cross_points:
                row_str += RED + cell + "\033[0m"  # Reset color after printing
            else:
                row_str += cell
            row_str += " "
        print(f"{i + 1:2d} {row_str}")


def overlaps_with_existing_line(new_line_coords, new_line_direction):
    for sequence in played_sequences:
        # Check if the new line is in the same direction as the existing one.
        if sequence['direction'] == new_line_direction:
            sequence_coords_set = set(sequence['coords'])
            new_line_coords_set = set(new_line_coords)

            # Check for overlaps excluding the allowed start/end points.
            overlap = new_line_coords_set & sequence_coords_set

            # If there's any overlap...
            if overlap:
                # Allow overlap only if it's at the start or the end of the existing sequence.
                allowed_overlap_points = {sequence['coords'][0], sequence['coords'][-1]}
                if not overlap <= allowed_overlap_points:
                    return True

                # Special case handling if the new line is exactly overlapping in reverse.
                if len(overlap) == 2 and not (new_line_coords[0] in allowed_overlap_points and new_line_coords[-1] in allowed_overlap_points):
                    return True
    return False




def complete_line(start_row, start_col, end_row, end_col):
    global chosen_cell, played_sequences, last_added_cell

    dx = int((end_row - start_row) / max(1, abs(end_row - start_row))) if end_row != start_row else 0
    dy = int((end_col - start_col) / max(1, abs(end_col - start_col))) if end_col != start_col else 0
    direction = (dx, dy)
    line_cells = [(start_row + dx * i, start_col + dy * i) for i in
                  range(max(abs(end_row - start_row), abs(end_col - start_col)) + 1)]

    if overlaps_with_existing_line(line_cells, direction):
        print("Cannot add this line; it overlaps with an existing line in the same direction.")
        return False, None

    x_count = sum(1 for x, y in line_cells if board[x][y] == CROSS)
    empty_cells = [(x, y) for x, y in line_cells if board[x][y] == EMPTY]

    if x_count == 4 and len(empty_cells) == 1:  # Exactly one empty cell to complete the line
        fill_row, fill_col = empty_cells[0]
        board[fill_row][fill_col] = CROSS
        chosen_cell = (fill_row, fill_col)
        last_added_cell = (fill_row, fill_col)
        played_sequences.append({'coords': line_cells, 'direction': direction})
        return True, line_cells
    return False, None


def process_input(input_str):
    try:
        positions = input_str.split("-")
        if len(positions) == 2:
            start_col, start_row = ord(positions[0][0].upper()) - ord('A'), int(positions[0][1:]) - 1
            end_col, end_row = ord(positions[1][0].upper()) - ord('A'), int(positions[1][1:]) - 1
            return start_row, start_col, end_row, end_col
    except ValueError:
        print("Invalid input format.")
    return None


while True:
    print_board()
    input_str = input("Enter the start and end cell (e.g., 'A1-A5'): ")
    input_result = process_input(input_str)

    if input_result:
        start_row, start_col, end_row, end_col = input_result
        valid_line, line_cells = complete_line(start_row, start_col, end_row, end_col)
        if valid_line:
            print(f"Line completed from ({start_row + 1},{chr(start_col + 65)}) to ({end_row + 1},{chr(end_col + 65)})")
            print(played_sequences)
        else:
            print("Could not complete a line with the input provided.")
    else:
        print("Please try again with valid input.")
