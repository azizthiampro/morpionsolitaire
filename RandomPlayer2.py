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

        self.reset_game()
        self.played_sequence = []
        self.best_moves = []

        game_data = []
        phase = 1

        #Enregistrement des meilleurs score, sequences et coups joués pour chaque phase
        global_best_score = 0
        global_best_sequences = None
        global_best_moves = None
        while True:
            print(f"\nDébut de la Phase {phase}")

            self.reset_game()
            for move in self.best_moves:
                self.cross_points.add(move)

            possible_moves = self.find_possible_moves()
            print(f"{len(possible_moves)} coups possibles à évaluer : {possible_moves}\n")
            if not possible_moves:
                break

            # Enregistrement des meilleurs score, sequences et coups joués pour chaque coup fixé
            best_score = 0
            best_move = None
            best_sequence = []

            start_time = time.time()  # Enregistrer le temps de début

            for move in possible_moves:
                self.reset_game()
                for prev_move in self.best_moves:
                    self.cross_points.add(prev_move)

                self.cross_points.add(move)

                current_score, current_sequence, moves_played, sequence, direction = self.simulate_game(move, num_games)

                if current_score > best_score:
                    print(f"Le coup {move} a battu l'ancien record de {best_score}  avec un score de {current_score}\n")
                    b_sequence = sequence
                    b_direction = direction
                    best_score = current_score
                    best_move = move
                    best_moves_played = moves_played
                    best_sequence = current_sequence

            end_time = time.time()  # Enregistrer le temps de fin
            elapsed_time = end_time - start_time  # Calculer le temps écoulé

            if best_move:
                print(f"Le meilleur coup trouvé de la phase {phase} est : {best_move} avec un score record de {best_score}")
                # print(f"liste des coups joués : {best_moves_played}\n")
                # print(f"liste des sequences joués: {best_sequence}\n")
                # print(f"Sequences trouvées: {self.played_sequence}")
                # print(f"coups trouvées: {self.best_moves}")

                if best_score > global_best_score:
                    print(f"Il bat l'ancien record de {global_best_score} des phases précédentes")

                    global_best_score = best_score
                    global_best_moves = best_moves_played
                    self.played_sequence.append((b_sequence, b_direction)) #Ajout de la sequence du best_move
                    self.best_moves.append(best_move)
                    global_best_sequences = best_sequence
                    print(f"Suite de coup ayant engendré ce score: {global_best_moves}")
                else:
                    print(f"L'ancien record de {global_best_score} des phases précédentes n'a pas été battu")
                    print(f"On conserve l'ancienne suite de coup :{global_best_moves}")

                    move1 = global_best_moves[len(self.best_moves)]
                    self.best_moves.append(move1)

                    sequence1 = global_best_sequences[len(self.played_sequence)]
                    self.played_sequence.append(sequence1)

                    try:
                        move2 = global_best_moves[len(self.best_moves)]
                        print(move1, move2)
                        self.best_moves.append(move2)
                        sequence2 = global_best_sequences[len(self.played_sequence)]
                        self.played_sequence.append(sequence2)
                        print(f"On joue les 2 prochains coups dans l'ancienne suite qui est de coups :{move1} et {move2}")
                    except:
                        print(f"On joue le prochain coup dans l'ancienne suite qui est le coup :{move1}")

                print(f"Coup trouvé en : {elapsed_time:.2f} secondes")  # Afficher le temps pris
                phase += 1

            else:
                break

        # En-têtes des colonnes (clés des dictionnaires)

        print(f"Final moves: {self.best_moves}")
        print(f"Final sequences: {self.played_sequence}")
        print(f"Score final : {len(self.best_moves)}")
        return len(self.best_moves)

    def simulate_game(self, initial_move, n_simulation):
        print(f"Début des simulations pour le coup {initial_move}")
        c = 1

        #Enregistrement du meilleur score, sequence et coups
        best_simulation_score = 0
        best_simulation_sequence = None
        best_simulation_moves = []

        for _ in range(n_simulation):

            cross_points_simulation = self.cross_points.copy() #simulation effectué avec l'état de la grille à jour
            played_sequence_simulation = self.played_sequence.copy() #simulation effectué avec les précédents coups déjà joué
            simulation_moves = self.best_moves.copy() #sequence de jeu de la simulation contenant les coups déjà joué
            score_simulation = 0 #score de la simulation actuelle

            #Pour chaque séquence déjà trouvé mettre à jour le score
            for seq in played_sequence_simulation:
                score_simulation +=1

            #Application du coup en cours d'évaluation
            valid, initial_sequence, initial_direction = self.find_valid_sequence_with_center(initial_move)
            if valid:
                played_sequence_simulation.append((initial_sequence, initial_direction))
                cross_points_simulation.add(initial_move)
                score_simulation += 1
                simulation_moves.append(initial_move)

            while True:
                possible_moves = self.find_possible_moves_simulation(cross_points_simulation, played_sequence_simulation)
                if not possible_moves:
                    break

                random_move = random.choice(possible_moves)
                valid, sequence, direction = self.find_valid_sequence_with_center_simulation(random_move,
                                                                                             cross_points_simulation,
                                                                                             played_sequence_simulation)

                if valid:
                    played_sequence_simulation.append((sequence, direction))
                    score_simulation += 1
                    cross_points_simulation.add(random_move)
                    simulation_moves.append(random_move)  # Ajouter chaque nouveau mouvement à la séquence

            print(f"Simulation {c} : {score_simulation}")
            c += 1
            if score_simulation > best_simulation_score:
                best_simulation_score = score_simulation
                best_simulation_sequence = played_sequence_simulation
                best_simulation_moves = simulation_moves

        print(f"Meilleur score des {n_simulation} simulations: {best_simulation_score}\n")
        return best_simulation_score, best_simulation_sequence, best_simulation_moves, initial_sequence, initial_direction # Retourner le score et la séquence

    def find_possible_moves_simulation(self, cross_points, played_sequence):
        random.shuffle(RandomPlayer2.DIRECTIONS)
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
    nbre_simulation = 1
    nbre_test = 10
    player = RandomPlayer2()

    # Lancement de la simulation
    fichier = "records.txt"
    for i in range(nbre_test):
        score = player.main_loop(num_games=nbre_simulation)
        with open("records.txt", "a") as F:
            text = f"{nbre_simulation}, {score} \n"
            F.write(text)