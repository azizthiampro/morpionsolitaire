import random
import time
import csv
from functools import lru_cache

class RandomPlayer2:
    DIRECTIONS = [
        (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)
    ]

    def __init__(self):
        self.grid_size = 20
        self.best_moves = []
        self.played_sequence = []
        self.reset_game()

    def reset_game(self):
        self.cross_points = {
            (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5),
            (14, 8), (13, 8), (12, 8), (11, 8), (11, 7), (11, 6), (11, 5),
            (10, 5), (9, 5), (5, 9), (5, 10), (5, 11), (14, 9), (14, 10), (14, 11), (13, 11),
            (12, 11), (11, 11), (6, 11), (7, 11), (8, 11), (8, 12), (8, 13), (8, 14), (11, 12),
            (11, 13), (11, 14), (9, 14), (10, 14)
        }

        self.score = 0

    @lru_cache(maxsize=None)
    def normalize_direction(self, direction):
        dx, dy = direction
        if dx == 0:
            return (0, 1) if dy > 0 else (0, -1)
        elif dy == 0:
            return (1, 0) if dx > 0 else (-1, 0)
        elif abs(dx) == abs(dy):
            return (1, 1) if dx > 0 and dy > 0 else (-1, -1) if dx < 0 and dy < 0 else (
                1, -1) if dx > 0 and dy < 0 else (-1, 1)
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
        return list(possible_moves)

    def main_loop(self, num_games=10):

        game_data = []
        while True:
            self.reset_game()
            for move in self.best_moves:
                self.cross_points.add(move)

            possible_moves = self.find_possible_moves()
            if not possible_moves:
                break

            best_score = 0
            best_move = None
            best_sequence = []

            start_time = time.time()  # Enregistrer le temps de début

            for move in possible_moves:
                self.reset_game()
                for prev_move in self.best_moves:
                    self.cross_points.add(prev_move)
                self.cross_points.add(move)
                for _ in range(num_games):
                    current_score, current_sequence,  sequence, direction = self.simulate_game(move)
                    print(f"{len(current_sequence)}, score : {current_score}, ancien record : {best_score}")
                    if current_score > best_score:
                        b_sequence = sequence
                        b_direction = direction
                        best_score = current_score
                        best_move = move
                        best_sequence = current_sequence

            end_time = time.time()  # Enregistrer le temps de fin
            elapsed_time = end_time - start_time  # Calculer le temps écoulé

            if best_move:


                self.played_sequence.append((b_sequence, b_direction))
                self.best_moves.append(best_move)
                print(f"Added new best move: {best_move} with score {best_score}")
                print(f"sequence founded : {self.played_sequence}")
                print(f"Best sequence for this move: {len(best_sequence)}")
                print(f"Time taken to find this move: {elapsed_time:.2f} seconds")  # Afficher le temps pris

                #Ecriture des résultats dans un fichier csv
                data = {"possibles_moves": len(possible_moves), "best_move": best_move, "score": best_score,
                        "elapsed_time": elapsed_time, "sequence": b_sequence, "direction": b_direction}

                game_data.append(data)

            else:
                break

        # En-têtes des colonnes (clés des dictionnaires)
        colonnes = game_data[0].keys()

        # Écrire les données dans le fichier CSV
        with open("records2.csv", mode='w', newline='') as fichier_csv:
            writer = csv.DictWriter(fichier_csv, fieldnames=colonnes)
            writer.writeheader()
            for ligne in game_data:
                writer.writerow(ligne)

        print(f"Final moves: {len(self.played_sequence)}")

    def simulate_game(self, initial_move):
        cross_points_simulation = self.cross_points.copy()
        played_sequence_simulation = self.played_sequence.copy()
        score_simulation = 1
        game_sequence = [initial_move]  # Initialiser avec le premier mouvement joué

        cross_points_simulation.add(initial_move)
        valid, initial_sequence, initial_direction = self.find_valid_sequence_with_center(initial_move)
        if valid:
            played_sequence_simulation.append((initial_sequence, initial_direction))

        while True:
            possible_moves = self.find_possible_moves_simulation(cross_points_simulation, played_sequence_simulation)
            if not possible_moves:
                break

            random_move = random.choice(possible_moves)
            game_sequence.append(random_move)  # Ajouter chaque nouveau mouvement à la séquence
            cross_points_simulation.add(random_move)
            score_simulation += 1

            valid, sequence, direction = self.find_valid_sequence_with_center_simulation(random_move,
                                                                                         cross_points_simulation,
                                                                                         played_sequence_simulation)
            if valid:
                played_sequence_simulation.append((sequence, direction))


        return score_simulation, played_sequence_simulation, initial_sequence, initial_direction # Retourner le score et la séquence

    def find_possible_moves_simulation(self, cross_points, played_sequence):
        possible_moves = set()
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                cell = (x, y)
                if cell in cross_points:
                    continue
                for direction in RandomPlayer2.DIRECTIONS:
                    is_valid_move = False
                    for shift in range(-4, 1):
                        potential_sequence = [
                            (cell[0] + shift * direction[0] + i * direction[0],
                             cell[1] + shift * direction[1] + i * direction[1])
                            for i in range(5) if
                            0 <= cell[0] + shift * direction[0] + i * direction[0] < self.grid_size and 0 <= cell[
                                1] + shift * direction[1] + i * direction[1] < self.grid_size
                        ]
                        if len(potential_sequence) == 5 and sum(p in cross_points for p in potential_sequence) == 4:
                            normalized_direction = self.normalize_direction(direction)
                            if not self.is_sequence_overlapping_simulation(potential_sequence, normalized_direction,
                                                                           played_sequence):
                                is_valid_move = True
                                break
                    if is_valid_move:
                        possible_moves.add(cell)
                        break
        return list(possible_moves)

    def find_valid_sequence_with_center_simulation(self, new_cell, cross_points, played_sequence):
        random.shuffle(RandomPlayer2.DIRECTIONS)
        for direction in RandomPlayer2.DIRECTIONS:
            for shift in range(-4, 1):
                sequence = [
                    (new_cell[0] + (i + shift) * direction[0], new_cell[1] + (i + shift) * direction[1])
                    for i in range(5) if
                    0 <= new_cell[0] + (i + shift) * direction[0] < self.grid_size and 0 <= new_cell[1] + (
                                i + shift) * direction[1] < self.grid_size
                ]
                if len(sequence) == 5 and all(cell in cross_points or cell == new_cell for cell in sequence):
                    normalized_direction = self.normalize_direction(direction)
                    if not self.is_sequence_overlapping_simulation(sequence, normalized_direction, played_sequence):
                        return True, sequence, normalized_direction
        return False, None, None

    def is_sequence_overlapping_simulation(self, new_sequence, new_direction, played_sequences):
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

if __name__ == "__main__":
    player = RandomPlayer2()
    # Lancement de la simulation
    player.main_loop(num_games=10)