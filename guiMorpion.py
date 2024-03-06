import pygame
import sys

# Initialize Pygame
pygame.init()

# Grid settings
grid_size = 20
cell_size = 40  # Increased cell size for better visibility of the crosses
margin = 1
played_cell=[]
played_sequence=[]
# Initialize a list to track invalid moves and their display time
invalid_moves = []

# Window size
width = grid_size * (cell_size + margin) + margin
height = grid_size * (cell_size + margin) + margin

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("20x20 Morpion solitaire game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)

# Points to draw
cross_points = [
    (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5),
    (14, 8), (13, 8), (12, 8), (11, 8), (11, 7), (11, 6), (11, 5),
    (10, 5), (9, 5), (5, 9), (5, 10), (5, 11), (14, 9), (14, 10), (14, 11), (13, 11),
    (12, 11), (11, 11), (6, 11), (7, 11), (8, 11), (8, 12), (8, 13), (8, 14), (11, 12),
    (11, 13), (11, 14), (9, 14), (10, 14)
]

# Function to draw a cross in a cell




def draw_dot(x, y, color):
    # Calculate the center position of the cell
    center_x = x * (cell_size + margin) + margin + cell_size // 2
    center_y = y * (cell_size + margin) + margin + cell_size // 2

    # Define the radius of the dot
    radius = cell_size // 5  # Adjust this value to make the dot larger or smaller

    # Draw the dot
    pygame.draw.circle(screen, color, (center_x, center_y), radius)




def get_cell_from_mouse_pos(pos):
    x, y = pos
    grid_x = x // (cell_size + margin)
    grid_y = y // (cell_size + margin)
    return  grid_x,grid_y


def normalize_direction(direction):
    """Normalise la direction pour ignorer le sens."""
    dx, dy = direction
    return (abs(dx), abs(dy))

def is_sequence_overlapping(new_sequence, new_direction, played_sequences):
    """Vérifie si la nouvelle séquence chevauche des séquences existantes dans la même direction absolue."""
    normalized_new_direction = normalize_direction(new_direction)
    for seq, dir in played_sequences:
        if normalize_direction(dir) == normalized_new_direction and set(seq) & set(new_sequence):
            return True
    return False


def find_valid_sequence_with_center(new_cell, cross_points, played_sequences):
    directions = [
        # Liste des directions initiales
        (0, 1),  # Up
        (0, -1),  # Down
        (1, 0),  # Right
        (-1, 0),  # Left
        (1, 1),  # Diagonal up-right
        (-1, -1),  # Diagonal down-left
        (1, -1),  # Diagonal down-right
        (-1, 1),  # Diagonal up-left
    ]

    for direction in directions:
        for shift in range(-4, 1):
            sequence = []
            for i in range(5):
                next_cell = (new_cell[0] + (i + shift) * direction[0], new_cell[1] + (i + shift) * direction[1])
                sequence.append(next_cell)

            if all(cell in cross_points or cell == new_cell for cell in sequence):
                normalized_direction = normalize_direction(direction)
                if not is_sequence_overlapping(sequence, normalized_direction, played_sequences):
                    return True, sequence, normalized_direction

    return False, None, None

def draw_line_through_cells(sequence, color, width=5):
    # This function assumes 'sequence' is a list of tuples, where each tuple is (x, y) representing cell coordinates
    if len(sequence) < 2:
        return  # Need at least two points to draw a line

    # Convert cell coordinates to pixel coordinates (center of each cell)
    points = []
    for cell in sequence:
        center_x = cell[0] * (cell_size + margin) + margin + cell_size // 2
        center_y = cell[1] * (cell_size + margin) + margin + cell_size // 2
        points.append((center_x, center_y))

    # Draw the line through all points
    pygame.draw.lines(screen, color, False, points, width)


# Initialize the score outside the main loop
score = 0

# Define font for score display
font = pygame.font.Font(None, 36)
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            cell = get_cell_from_mouse_pos(pos)
            valid, sequence, direction = find_valid_sequence_with_center(cell, cross_points,played_sequence)
            if cell not in cross_points and valid:
                cross_points.append(cell)
                played_cell.append(cell)
                score += 1
                played_sequence.append((sequence, direction))  # Include direction
                print(f"played sequence: {played_sequence}")
            else:
                current_time = pygame.time.get_ticks()
                invalid_moves.append((cell, current_time))

    screen.fill(black)

    # Draw the grid and dots
    for x in range(grid_size):
        for y in range(grid_size):
            rect = pygame.Rect(x * (cell_size + margin) + margin, y * (cell_size + margin) + margin, cell_size, cell_size)
            pygame.draw.rect(screen, white, rect)
    for point in cross_points:
        draw_dot(*point, black)
    # draw lines
    for sequence, _ in played_sequence:
        draw_line_through_cells(sequence, green)  # Pass the sequence and a color for the line

    # Display visual feedback for invalid moves
    current_time = pygame.time.get_ticks()
    for move in invalid_moves[:]:
        cell, move_time = move
        if current_time - move_time <= 500:
            rect = pygame.Rect(cell[0] * (cell_size + margin) + margin, cell[1] * (cell_size + margin) + margin, cell_size, cell_size)
            pygame.draw.rect(screen, red, rect)
        else:
            invalid_moves.remove(move)

    # Display the score
    text = font.render(f'Score: {score}', True, white, red)
    text_rect = text.get_rect()
    text_rect.center = (width // 2, 20)
    screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()