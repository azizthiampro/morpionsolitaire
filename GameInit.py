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

        # Window size
        self.width = self.grid_size * (self.cell_size + self.margin) + self.margin
        self.height = self.grid_size * (self.cell_size + self.margin) + self.margin

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
        self.font = pygame.font.Font(None, 36)

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

    def main_loop(self):
        # Main loop of the game
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    cell = self.get_cell_from_mouse_pos(pos)
                    valid, sequence, direction = self.find_valid_sequence_with_center(cell)

                    if cell not in self.cross_points and valid:
                        self.cross_points.append(cell)
                        self.played_cell.append(cell)
                        self.score += 1
                        self.played_sequence.append((sequence, direction))  # Include direction
                        # Après chaque coup valide, vérifier si d'autres lignes peuvent être créées
                        if not self.can_create_line(self.cross_points):
                            print("Fin de la partie. Votre score est :", self.score)
                            running = False
                    else:
                        current_time = pygame.time.get_ticks()
                        self.invalid_moves.append((cell, current_time))

            self.screen.fill(self.black)

            # Draw the grid and dots
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    rect = pygame.Rect(x * (self.cell_size + self.margin) + self.margin, y * (
                            self.cell_size + self.margin) + self.margin, self.cell_size,
                                       self.cell_size)
                    pygame.draw.rect(self.screen, self.white, rect)
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

            # Display the score
            text = self.font.render(f'Score: {self.score}', True, self.white, self.red)
            text_rect = text.get_rect()
            text_rect.center = (self.width // 2, 20)
            self.screen.blit(text, text_rect)

            pygame.display.flip()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = GameInit()
    game.main_loop()
