import random
from functools import lru_cache

class RandomPlayer2:
    DIRECTIONS = [
        (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)
    ]

    def __init__(self):
        self.grid_size = 20
        self.best_moves = []
        self.reset_game()

    def reset_game(self):
        self.cross_points = {(5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5),
            (14, 8), (13, 8), (12, 8), (11, 8), (11, 7), (11, 6), (11, 5),
            (10, 5), (9, 5), (5, 9), (5, 10), (5, 11), (14, 9), (14, 10), (14, 11), (13, 11),
            (12, 11), (11, 11), (6, 11), (7, 11), (8, 11), (8, 12), (8, 13), (8, 14), (11, 12),
            (11, 13), (11, 14), (9, 14), (10, 14)}

        self.played_sequence = []
        self.score = 0

    @lru_cache(maxsize=None)
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

    @lru_cache(maxsize=None)
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
        random.shuffle(RandomPlayer2.DIRECTIONS)
        for direction in RandomPlayer2.DIRECTIONS:
            for shift in range(-4, 1):
                sequence = [
                    (new_cell[0] + (i + shift) * direction[0], new_cell[1] + (i + shift) * direction[1])
                    for i in range(5) if 0 <= new_cell[0] + (i + shift) * direction[0] < self.grid_size and 0 <= new_cell[1] + (i + shift) * direction[1] < self.grid_size
                ]
                if len(sequence) == 5 and all(cell in self.cross_points or cell == new_cell for cell in sequence):
                    normalized_direction = self.normalize_direction(direction)
                    if not self.is_sequence_overlapping(sequence, normalized_direction, self.played_sequence):
                        return True, sequence, normalized_direction
        return False, None, None

    def find_possible_moves(self):
        random.shuffle(RandomPlayer2.DIRECTIONS)
        possible_moves = set()  # Changé en set pour éviter les duplications
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                cell = (x, y)
                if cell in self.cross_points:
                    continue
                for direction in RandomPlayer2.DIRECTIONS:
                    is_valid_move = False
                    for shift in range(-4, 1):
                        potential_sequence = [
                            (cell[0] + shift * direction[0] + i * direction[0], cell[1] + shift * direction[1] + i * direction[1])
                            for i in range(5) if 0 <= cell[0] + shift * direction[0] + i * direction[0] < self.grid_size and 0 <= cell[1] + shift * direction[1] + i * direction[1] < self.grid_size
                        ]
                        if len(potential_sequence) == 5 and sum(p in self.cross_points for p in potential_sequence) == 4:
                            normalized_direction = self.normalize_direction(direction)
                            if not self.is_sequence_overlapping(potential_sequence, normalized_direction, self.played_sequence):
                                is_valid_move = True
                                break
                    if is_valid_move:
                        possible_moves.add(cell)
                        break
        return list(possible_moves)  # Convert back to list if necessary

    def main_loop(self, num_games=3):
        running = True
        while running:
            self.reset_game()  # Réinitialiser le jeu à chaque nouvelle recherche de meilleur coup

            # Appliquer les coups précédemment trouvés
            for move in self.best_moves:
                self.cross_points.add(move)

            global_best_score = 0
            global_best_move = None

            initial_possible_moves = self.find_possible_moves()  # Trouve tous les coups de départ possibles
            for start_move in initial_possible_moves:
                series_best_score = 0  # Meilleur score pour la série de jeux en cours
                series_best_move = None  # Meilleur coup pour la série de jeux en cours

                for game_idx in range(num_games):
                    self.reset_game()

                    # Appliquer les coups de best_moves ainsi que le nouveau coup testé
                    for move in self.best_moves:
                        self.cross_points.add(move)
                    self.cross_points.add(start_move)  # Utilisation de add pour l'ensemble
                    self.score += 1

                    # Vérifier immédiatement si le premier coup peut faire partie d'une séquence
                    valid, sequence, direction = self.find_valid_sequence_with_center(start_move)
                    if valid:
                        self.played_sequence.append((sequence, direction))

                    running_game = True
                    while running_game:
                        possible_moves = self.find_possible_moves()
                        if possible_moves:
                            random_move = random.choice(possible_moves)
                            valid, sequence, direction = self.find_valid_sequence_with_center(random_move)
                            if valid:
                                self.cross_points.add(random_move)  # Ajoute à l'ensemble
                                self.played_sequence.append((sequence, direction))
                                self.score += 1
                        else:
                            running_game = False

                    if self.score > series_best_score:
                        series_best_score = self.score
                        series_best_move = start_move

                if series_best_score > global_best_score:
                    global_best_score = series_best_score
                    global_best_move = series_best_move

            if global_best_move:
                print(f"Meilleur score global obtenu: {global_best_score} avec le coup de départ {global_best_move}")
                self.best_moves.append(global_best_move)  # Ajouter le meilleur coup à la liste
                self.cross_points.add(global_best_move)  # Ajouter à la grille
            else:
                running = False  # Aucun coup valide trouvé, arrêter la recherche


if __name__ == "__main__":
    game = RandomPlayer2()  # Active le rendu
    game.main_loop()