import pygame
import sys

class GameInit:
    def __init__(self):
        pygame.init()

        # Grid settings and other initializations
        self.grid_size = 20
        self.cell_size = 40
        self.margin = 1
        # Initialize other attributes...
        self.grid_size = 20
        self.cell_size = 40  # Increased cell size for better visibility of the crosses
        self.margin = 1
        self.played_cell = []
        self.played_sequence = []
        self.invalid_moves = []

        # Window size adjusted to accommodate numbers on the sides
        self.width = self.grid_size * (self.cell_size + self.margin) + self.margin + 40  # Extra space for numbers
        self.height = self.grid_size * (self.cell_size + self.margin) + self.margin + 40  # Extra space for numbers

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("20x20 Morpion Solitaire Game")

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.green = (0, 255, 0)

        # Points and score
        self.cross_points = self.init_cross_points()
        self.score = 0
        self.font = pygame.font.Font(None, 36)

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
        self.font = pygame.font.Font(None, 36)

    # Other methods...

    def draw_grid(self):
        # Drawing the grid cells
        for x in range(1, self.grid_size ):
            for y in range(self.grid_size):
                rect = pygame.Rect(x * (self.cell_size + self.margin) + self.margin + 40,  # Adjusted for number spacing
                                   y * (self.cell_size + self.margin) + self.margin + 40,  # Adjusted for number spacing
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.white, rect)

        # Drawing numbers for each column and row
        for i in range(1, self.grid_size ):
            # Numbers for columns
            self.draw_text(str(i), 20 + (i) * (self.cell_size + self.margin), 10)
            # Numbers for rows
            self.draw_text(str(i), 10, 20 + (i) * (self.cell_size + self.margin))

    def draw_text(self, text, x, y):
        """Draws text on the screen at the specified x, y coordinates."""
        text_surface = self.font.render(text, True, self.white)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def init_cross_points(self):
        # Initialize the cross points for the game start
        return [
            (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5),
            (14, 8), (13, 8), (12, 8), (11, 8), (11, 7), (11, 6), (11, 5),
            (10, 5), (9, 5), (5, 9), (5, 10), (5, 11), (14, 9), (14, 10), (14, 11), (13, 11),
            (12, 11), (11, 11), (6, 11), (7, 11), (8, 11), (8, 12), (8, 13), (8, 14), (11, 12),
            (11, 13), (11, 14), (9, 14), (10, 14)
        ]

    def draw_cross_points(self):
        for point in self.cross_points:
            self.draw_dot(*point, self.black)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(pygame.mouse.get_pos())
        return True

    def handle_mouse_click(self, pos):
        cell = self.get_cell_from_mouse_pos(pos)
        valid, sequence, direction = self.find_valid_sequence_with_center(cell)
        if cell not in self.cross_points and valid:
            self.cross_points.append(cell)
            self.played_cell.append(cell)
            self.score += 1
            self.played_sequence.append((sequence, direction))
        else:
            self.invalid_moves.append((cell, pygame.time.get_ticks()))

    def update_game_state(self):
        possible_moves = self.find_possible_moves()
        if not possible_moves:
            print("No more valid moves. Game Over.")
            print("Final Score:", self.score)
            return False  # This signals the game should end
        return True  # Game continues

    def draw_game_elements(self):
        self.screen.fill(self.black)
        self.draw_grid()
        self.draw_cross_points()
        self.draw_played_lines()
        self.draw_invalid_moves()
        self.draw_score()

    def draw_invalid_moves(self):
        current_time = pygame.time.get_ticks()
        valid_moves = []  # Prepare a new list for moves that are still valid (not expired)
        for move in self.invalid_moves:
            cell, move_time = move
            if current_time - move_time <= 500:  # Invalid move indicator visible for 500 ms
                # Adjust drawing position if necessary
                rect = pygame.Rect((cell[0] + 1) * (self.cell_size + self.margin) + self.margin,
                                   (cell[1] + 1) * (self.cell_size + self.margin) + self.margin,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.red, rect)
                valid_moves.append(move)  # This move is still within its display time
        self.invalid_moves = valid_moves  # Replace the old list with the updated one

    def draw_score(self):
        text = self.font.render(f'Score: {self.score}', True, self.white, self.black)
        text_rect = text.get_rect()
        text_rect.center = (self.width // 2, 20)
        self.screen.blit(text, text_rect)

    def draw_played_lines(self):
        for sequence, _ in self.played_sequence:
            self.draw_line_through_cells(sequence, self.green)  # Pass the sequence and a color for the line

    def main_loop(self):
        running = True
        while running:
            running = self.handle_events()
            game_continues = self.update_game_state()
            if not game_continues:
                # Here, consider adding a delay or wait for a user action to properly close the game.
                running = False
            self.draw_game_elements()
            pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds before closing
        pygame.quit()

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
        grid_x = (x - 40) // (self.cell_size + self.margin) + 1
        grid_y = (y - 40) // (self.cell_size + self.margin) + 1
        return grid_x, grid_y

    def normalize_direction(self, direction):
        """Normalise la direction pour ignorer le sens."""
        dx, dy = direction
        return (abs(dx), abs(dy))

    def is_sequence_overlapping(self, new_sequence, new_direction, played_sequences):
        """Vérifie si la nouvelle séquence chevauche des séquences existantes dans la même direction absolue."""
        normalized_new_direction = self.normalize_direction(new_direction)
        for seq, dir in played_sequences:
            if self.normalize_direction(dir) == normalized_new_direction and set(seq) & set(new_sequence):
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

        for point in self.cross_points:
            for direction in directions:
                for i in range(-4, 1):  # Shift the starting point in each direction to check for potential moves
                    potential_move = (point[0] + i * direction[0], point[1] + i * direction[1])
                    if 0 <= potential_move[0] < self.grid_size and 0 <= potential_move[1] < self.grid_size:
                        sequence = [(
                            potential_move[0] + j * direction[0],
                            potential_move[1] + j * direction[1]
                        ) for j in range(5)]
                        if all(0 <= cell[0] < self.grid_size and 0 <= cell[1] < self.grid_size for cell in sequence):
                            if sum(1 for cell in sequence if
                                   cell in self.cross_points) == 4 and potential_move not in self.cross_points:
                                if not self.is_sequence_overlapping(sequence, direction, self.played_sequence):
                                    possible_moves.append(potential_move)

        return possible_moves

if __name__ == "__main__":
    game = GameInit()
    game.main_loop()
