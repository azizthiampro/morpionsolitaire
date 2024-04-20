import pygame
import sys
import random

class RandomPlayer:
    def __init__(self, render=True):
        self.render = render
        if self.render:
            pygame.init()

            # Les attributs suivants sont uniquement nécessaires si le rendu est activé
            self.cell_size = 40
            self.grid_size = 20
            self.margin = 1
            self.width = self.grid_size * (self.cell_size + self.margin) + self.margin
            self.height = self.grid_size * (self.cell_size + self.margin) + self.margin + 50
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("20x20 Morpion solitaire game")
            self.coord_font = pygame.font.Font(None, 20)
            self.font = pygame.font.Font(None, 32)
            # Colors
            self.black = (0, 0, 0)
            self.white = (255, 255, 255)
            self.red = (255, 0, 0)
            self.yellow = (255, 255, 0)
            self.green = (0, 255, 0)

            # Attributs communs, nécessaires indépendamment du rendu
        self.grid_size = 20
        self.reset_game()

    def draw_dot(self, x, y, color):
        if not self.render:
            return
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

    def draw_line_through_cells(self, sequence, color, width=5):
        if not self.render:
            return
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

    def reset_game(self):
        # Réinitialise les points de départ des croix et le score
        self.cross_points = [
            (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5),
            (14, 8), (13, 8), (12, 8), (11, 8), (11, 7), (11, 6), (11, 5),
            (10, 5), (9, 5), (5, 9), (5, 10), (5, 11), (14, 9), (14, 10), (14, 11), (13, 11),
            (12, 11), (11, 11), (6, 11), (7, 11), (8, 11), (8, 12), (8, 13), (8, 14), (11, 12),
            (11, 13), (11, 14), (9, 14), (10, 14)
        ]
        self.played_cell = []
        self.played_sequence = []
        self.score = 0

    def main_loop(self, num_games=10):
        global_best_score = 0  # Pour garder trace du meilleur score global
        global_best_move = None  # Pour garder trace du meilleur coup de départ global

        self.reset_game()
        initial_possible_moves = self.find_possible_moves()  # Trouve tous les coups de départ possibles

        for start_move in initial_possible_moves:
            series_best_score = 0  # Meilleur score pour la série de jeux en cours
            series_best_move = None  # Meilleur coup pour la série de jeux en cours

            for game_idx in range(num_games):
                self.reset_game()

                # Appliquer le premier coup spécifique
                self.cross_points.append(start_move)
                self.played_cell.append(start_move)
                self.score += 1

                running = True
                update_possible_moves = True  # Cette variable doit être réinitialisée pour chaque partie
                last_move_time = pygame.time.get_ticks()  # Réinitialiser le temps pour chaque partie

                while running:

                    current_time = pygame.time.get_ticks()
                    if update_possible_moves or current_time - last_move_time >= 1000:
                        possible_moves = self.find_possible_moves()

                        if possible_moves:
                            random_move = random.choice(possible_moves)
                            valid, sequence, direction = self.find_valid_sequence_with_center(random_move)
                            if valid:
                                self.cross_points.append(random_move)
                                self.played_cell.append(random_move)
                                self.score += 1
                                self.played_sequence.append((sequence, direction))
                                update_possible_moves = True
                        else:
                            running = False
                        last_move_time = current_time

                    if self.render:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return

                    if self.render:
                        self.screen.fill(self.white)  # Fill screen with white background

                        # Drawing grid, dots, sequences, and score
                        for x in range(self.grid_size):
                            for y in range(self.grid_size):
                                rect = pygame.Rect(x * (self.cell_size + self.margin) + self.margin,
                                                   y * (self.cell_size + self.margin) + self.margin,
                                                   self.cell_size, self.cell_size)
                                pygame.draw.rect(self.screen, self.black, rect, 1)  # Grid cell borders

                        for point in self.cross_points:
                            self.draw_dot(*point, self.black)

                        for sequence, _ in self.played_sequence:
                            self.draw_line_through_cells(sequence, self.red)

                        # Display score
                        over = ""
                        if len(possible_moves) == 0:
                            over = "Game over"

                        score_text = self.font.render(f'Artificial player (Soft version) -  Score: {self.score} {over}',
                                                      True, self.black)
                        self.screen.blit(score_text, (10, self.height - 40))

                        pygame.display.flip()

                if self.score > series_best_score:
                    series_best_score = self.score
                    series_best_move = start_move

            print(f"Meilleur score pour le coup de départ {start_move}: {series_best_score}")
            if series_best_score > global_best_score:
                global_best_score = series_best_score
                global_best_move = series_best_move

        # Affiche le meilleur score global et le meilleur coup de départ après toutes les séries
        print(f"Meilleur score global obtenu: {global_best_score} avec le coup de départ {global_best_move}")
        if self.render:
            pygame.quit()


if __name__ == "__main__":
    game = RandomPlayer(render=True)  # Active le rendu
    game.main_loop()