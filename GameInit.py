import pygame
import sys


class GameInit:
    def __init__(self):
        pygame.init()

        # Grid settings
        self.grid_size = 20
        self.cell_size = 40  # Increased cell size for better visibility of the crosses
        self.margin = 1
        self.played_cell = []
        self.played_sequence = []
        self.invalid_moves = []  # Initialize a list to track invalid moves and their display time
        self.coord_font = pygame.font.Font(None, 20)  # Smaller font for coordinates

        self.all_valid_sequences = []  # Ajout pour stocker les séquences valides détectées
        self.sequence_ends = []

        # Window size
        self.width = self.grid_size * (self.cell_size + self.margin) + self.margin
        # Window size with extra space for the score display
        self.height = self.grid_size * (self.cell_size + self.margin) + self.margin + 50

        # Set up the display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("20x20 Morpion solitaire game")

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.green = (0, 255, 0)

        # Points to draw
        self.cross_points = [
            (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5),
            (14, 8), (13, 8), (12, 8), (11, 8), (11, 7), (11, 6), (11, 5),
            (10, 5), (9, 5), (5, 9), (5, 10), (5, 11), (14, 9), (14, 10), (14, 11), (13, 11),
            (12, 11), (11, 11), (6, 11), (7, 11), (8, 11), (8, 12), (8, 13), (8, 14), (11, 12),
            (11, 13), (11, 14), (9, 14), (10, 14)
        ]

        self.score = 0  # Initialize the score

        # Define font for score display
        self.font = pygame.font.Font(None, 32)

    def draw_dot(self, x, y, color):
        # Calculate the center position of the cell
        center_x = x * (self.cell_size + self.margin) + self.margin + self.cell_size // 2
        center_y = y * (self.cell_size + self.margin) + self.margin + self.cell_size // 2

        # Define the radius of the dot
        radius = self.cell_size // 5  # Adjust this value to make the dot larger or smaller

        # Draw the dot
        pygame.draw.circle(self.screen, color, (center_x, center_y), radius)

    def get_cell_from_mouse_pos(self, pos):
        x, y = pos
        grid_x = x // (self.cell_size + self.margin)
        grid_y = y // (self.cell_size + self.margin)
        return grid_x, grid_y

    def normalize_direction(self, direction):
        dx, dy = direction
        # Normalize horizontal and vertical directions
        if dx == 0:
            return (0, 1) if dy > 0 else (0, -1)
        elif dy == 0:
            return (1, 0) if dx > 0 else (-1, 0)
        # Normalize diagonal directions
        elif abs(dx) == abs(dy):
            return (1, 1) if dx > 0 and dy > 0 else (-1, -1) if dx < 0 and dy < 0 else (
            1, -1) if dx > 0 and dy < 0 else (-1, 1)
        # Fallback for any other case (should not occur with proper input)
        return (dx, dy)

    def is_sequence_overlapping(self, new_sequence, new_direction, played_sequences):
        normalized_new_direction = self.normalize_direction(new_direction)
        for seq, dir1 in played_sequences:
            normalized_existing_direction = self.normalize_direction(dir1)
            if normalized_new_direction == normalized_existing_direction or normalized_new_direction == tuple(
                    -x for x in normalized_existing_direction):
                if new_sequence[0] == seq[-1] or new_sequence[-1] == seq[0]:
                    continue
                if set(seq) & set(new_sequence):
                    return True
        return False

    def find_valid_sequence_with_center(self, new_cell):
        directions = [
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
            for shift in range(-4, 1):  # Décale le point de départ pour couvrir toutes les positions centrées possibles
                sequence = []
                for i in range(5):  # Construit une séquence de 5 cellules dans la direction donnée
                    next_cell = (new_cell[0] + (i + shift) * direction[0], new_cell[1] + (i + shift) * direction[1])
                    if 0 <= next_cell[0] < self.grid_size and 0 <= next_cell[
                        1] < self.grid_size:  # Vérifie si la cellule est dans la grille
                        sequence.append(next_cell)
                    else:
                        break  # Sort de la boucle si la cellule est hors de la grille

                if len(sequence) == 5 and all(cell in self.cross_points or cell == new_cell for cell in sequence):
                    normalized_direction = self.normalize_direction(direction)
                    if not self.is_sequence_overlapping(sequence, normalized_direction, self.played_sequence):
                        return True, sequence, normalized_direction
        return False, None, None

    def find_all_valid_sequences_with_center(self, new_cell):
        all_valid_sequences = []
        directions = [
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
                    if 0 <= next_cell[0] < self.grid_size and 0 <= next_cell[1] < self.grid_size:
                        sequence.append(next_cell)
                    else:
                        break

                if len(sequence) == 5 and all(cell in self.cross_points or cell == new_cell for cell in sequence):
                    normalized_direction = self.normalize_direction(direction)
                    if not self.is_sequence_overlapping(sequence, normalized_direction, self.played_sequence):
                        self.all_valid_sequences.append((sequence, normalized_direction))

        return self.all_valid_sequences

    def highlight_sequence_ends(self, all_valid_sequences):
        for sequence, _ in all_valid_sequences:
            # Prendre en compte uniquement les extrémités de chaque séquence
            for end in (sequence[0], sequence[-1]):
                self.draw_dot(*end, self.red)  # Dessiner les extrémités en bleu

    def is_click_on_end(self, cell):
        # Vérifier si le clic est sur l'une des extrémités des séquences valides
        return cell in self.sequence_ends


    def draw_line_through_cells(self, sequence, color, width=5):
        # This function assumes 'sequence' is a list of tuples, where each tuple is (x, y) representing cell coordinates
        if len(sequence) < 2:
            return  # Need at least two points to draw a line

        # Convert cell coordinates to pixel coordinates (center of each cell)
        points = []
        for cell in sequence:
            center_x = cell[0] * (self.cell_size + self.margin) + self.margin + self.cell_size // 2
            center_y = cell[1] * (self.cell_size + self.margin) + self.margin + self.cell_size // 2
            points.append((center_x, center_y))

        # Draw the line through all points
        pygame.draw.lines(self.screen, color, False, points, width)

    def can_create_line(self, points):
        directions = [(0, 1),  # Up
            (0, -1),  # Down
            (1, 0),  # Right
            (-1, 0),  # Left
            (1, 1),  # Diagonal up-right
            (-1, -1),  # Diagonal down-left
            (1, -1),  # Diagonal down-right
            (-1, 1),  # Diagonal up-left
        ]
        for point in points:
            for direction in directions:
                sequence = [(
                    point[0] + i * direction[0],
                    point[1] + i * direction[1]
                ) for i in range(-4, 1)]  # Génère une séquence de 5 points dans la direction actuelle
                if all(0 <= p[0] < self.grid_size and 0 <= p[1] < self.grid_size for p in
                       sequence):  # Vérifie si tous les points sont dans la grille
                    if all(p in points or p == point for p in sequence):  # Vérifie si tous les points sont présents
                        return True
        return False

    def find_possible_moves(self):
        possible_moves = []
        directions = [
            (0, 1),  # Up
            (0, -1),  # Down
            (1, 0),  # Right
            (-1, 0),  # Left
            (1, 1),  # Diagonal up-right
            (-1, -1),  # Diagonal down-left
            (1, -1),  # Diagonal down-right
            (-1, 1),  # Diagonal up-left
        ]

        # Iterate over every cell in the grid to check for potential moves
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                cell = (x, y)
                # Skip the cell if it's already a part of cross_points
                if cell in self.cross_points:
                    continue

                # Check every direction for possible sequences that include the cell
                for direction in directions:
                    is_valid_move = False
                    for shift in range(-4,
                                       1):  # Shift the starting point in each direction to check for potential moves
                        potential_sequence = [
                            (cell[0] + shift * direction[0] + i * direction[0],
                             cell[1] + shift * direction[1] + i * direction[1])
                            for i in range(5)
                        ]

                        # Check if the sequence is valid: within grid bounds and contains exactly one empty spot (the potential move)
                        if all(0 <= p[0] < self.grid_size and 0 <= p[1] < self.grid_size for p in potential_sequence):
                            cross_count = sum(p in self.cross_points for p in potential_sequence)
                            if cross_count == 4:  # There are exactly 4 crosses in the sequence
                                normalized_direction = self.normalize_direction(direction)
                                if not self.is_sequence_overlapping(potential_sequence, normalized_direction,
                                                                    self.played_sequence):
                                    is_valid_move = True
                                    break  # Break out of the shift loop as we've found a valid sequence for this direction

                    if is_valid_move:
                        possible_moves.append(cell)
                        break  # Break out of the direction loop as we've found at least one valid sequence that includes the cell

        return possible_moves

    def main_loop(self):
        # Main loop of the game
        running = True
        update_possible_moves = True  # Initialize flag to update and print possible moves

        while running:
            if update_possible_moves:
                possible_moves = self.find_possible_moves()  # Find possible moves at the current state
                print("Possible moves: ", len(possible_moves))  # Print the list of possible moves
                update_possible_moves = False  # Reset flag until the next change

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    update_possible_moves = True  # Set flag to update possible moves on the next loop
                    pos = pygame.mouse.get_pos()
                    cell = self.get_cell_from_mouse_pos(pos)
                    valid, sequence, direction = self.find_valid_sequence_with_center(cell)

                    print(self.find_all_valid_sequences_with_center(cell))

                    if cell not in self.cross_points and valid:
                        self.cross_points.append(cell)
                        self.played_cell.append(cell)
                        self.score += 1
                        self.played_sequence.append((sequence, direction))  # Include direction



                        print("Played moves: ", self.played_sequence)
                        # After each valid move, check if other lines can be created
                        if not self.can_create_line(self.cross_points):
                            print("Game over. Your score is:", self.score)
                            running = False
                    else:
                        current_time = pygame.time.get_ticks()
                        self.invalid_moves.append((cell, current_time))

            self.screen.fill(self.black)

            # Draw the grid, dots, and coordinate labels on the edges
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    rect = pygame.Rect(x * (self.cell_size + self.margin) + self.margin,
                                       y * (self.cell_size + self.margin) + self.margin, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, self.white, rect)

                    # Only draw coordinate labels on the top edge and left edge of the grid
                    if x == 0:  # Left edge, draw Y coordinates
                        coord_text_y = f'{y}'
                        text_surface_y = self.coord_font.render(coord_text_y, True, self.black)
                        # Align text to the left, inside the cell
                        text_y_x = rect.left + 3  # A small padding from the left edge
                        text_y_y = rect.top + (rect.height - text_surface_y.get_height()) / 2  # Vertically centered
                        self.screen.blit(text_surface_y, (text_y_x, text_y_y))

                    if y == 0:  # Top edge, draw X coordinates
                        coord_text_x = f'{x}'
                        text_surface_x = self.coord_font.render(coord_text_x, True, self.black)
                        # Align text to the top, inside the cell
                        text_x_x = rect.left + (rect.width - text_surface_x.get_width()) / 2  # Horizontally centered
                        text_x_y = rect.top + 3  # A small padding from the top edge
                        self.screen.blit(text_surface_x, (text_x_x, text_x_y))

            # Highlight possible moves in yellow
            possible_moves = self.find_possible_moves()  # Get the list of possible moves
            for move in possible_moves:
                self.draw_dot(*move, self.yellow)  # Use the draw_dot method to draw the dot in yellow

            for point in self.cross_points:
                self.draw_dot(*point, self.black)
            # draw lines
            for sequence, _ in self.played_sequence:
                self.draw_line_through_cells(sequence, self.green)  # Pass the sequence and a color for the line

            # Display visual feedback for invalid moves
            current_time = pygame.time.get_ticks()
            for move in self.invalid_moves[:]:
                cell, move_time = move
                if current_time - move_time <= 500:
                    rect = pygame.Rect(cell[0] * (self.cell_size + self.margin) + self.margin, cell[1] * (
                            self.cell_size + self.margin) + self.margin,
                                       self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, self.red, rect)
                else:
                    self.invalid_moves.remove(move)
            over = ""
            if len(possible_moves) == 0:
                over = "Game over"
            # Display the score outside the grid, in the new space at the bottom
            text = self.font.render(f'Soft Version (Played by a user) - Score: {self.score} {over}', True, self.white)
            text_rect = text.get_rect()
            # Center the score horizontally and position it in the extra space below the grid
            text_rect.center = (self.width // 2, self.height - 25)  # Adjust Y position based on your design
            self.screen.blit(text, text_rect)

            pygame.display.flip()

            pygame.display.flip()

        pygame.quit()

    def play_sequence(self, sequence):
        # Ajouter les cellules de la séquence dans les croix jouées, si elles ne sont pas déjà présentes
        for cell in sequence:
            if cell not in self.cross_points:
                self.cross_points.append(cell)

        # Dessiner la ligne pour la séquence sélectionnée
        self.draw_line_through_cells(sequence, self.green)  # Supposons que self.green est la couleur des lignes

        # Mettre à jour le score. On pourrait par exemple augmenter le score de 1 pour chaque cellule ajoutée
        self.score += len([cell for cell in sequence if cell not in self.played_cell])
        self.played_cell.extend(sequence)  # Ajouter la séquence aux cellules jouées pour éviter les doublons

        # Ajouter la séquence jouée et sa direction à la liste des séquences jouées, si nécessaire
        # Cela nécessite de calculer ou de connaître la direction de la séquence, que nous simplifierons ici
        # par un tuple vide, à remplacer par la logique appropriée pour votre jeu
        self.played_sequence.append((sequence, ()))  # Remplacer () par la direction réelle si utilisée


if __name__ == "__main__":
    game = GameInit()
    game.main_loop()

