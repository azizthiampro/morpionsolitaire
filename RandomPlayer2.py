import random

class RandomPlayer2:
    def __init__(self):
        self.grid_size = 20
        self.reset_game()

    def reset_game(self):
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

    def find_possible_moves(self):
        possible_moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                cell = (x, y)
                if cell in self.cross_points:
                    continue
                for direction in directions:
                    is_valid_move = False
                    for shift in range(-4, 1):
                        potential_sequence = [
                            (cell[0] + shift * direction[0] + i * direction[0],
                             cell[1] + shift * direction[1] + i * direction[1])
                            for i in range(5)
                        ]
                        if self.is_valid_sequence(potential_sequence):
                            is_valid_move = True
                            break
                    if is_valid_move:
                        possible_moves.append(cell)
                        break
        return possible_moves

    def is_valid_sequence(self, sequence):
        if not all(0 <= p[0] < self.grid_size and 0 <= p[1] < self.grid_size for p in sequence):
            return False
        empty_count = sum(p not in self.cross_points for p in sequence)
        return empty_count == 1

    def choose_random_move(self, possible_moves):
        if possible_moves:
            return random.choice(possible_moves)
        else:
            return None

    def main_loop(self, num_games=10):
        initial_possible_moves = self.find_possible_moves()
        best_score = 0
        best_move = None

        for start_move in initial_possible_moves:
            scores = []
            for _ in range(num_games):
                self.reset_game()
                self.cross_points.append(start_move)
                self.score = 1  # Initialisation du score avec le premier coup joué

                while True:
                    possible_moves = self.find_possible_moves()
                    if not possible_moves:
                        break
                    move = self.choose_random_move(possible_moves)
                    if move is None:
                        break
                    self.cross_points.append(move)
                    self.score += 1  # Incrémenter le score pour chaque coup joué

                scores.append(self.score)
                if self.score > best_score:
                    best_score = self.score
                    best_move = start_move

            average_score = sum(scores) / len(scores)
            print(f"Moyenne des scores pour le coup de départ {start_move}: {average_score}")

        print(f"Meilleur score global: {best_score}, obtenu avec le coup de départ {best_move}")

if __name__ == "__main__":
    game = RandomPlayer2()
    game.main_loop()
