import random


class RandomPlayer:
    def __init__(self, game_init):
        self.game_init = game_init  # Instance de GameInit

    def play_random_move(self):
        possible_moves = self.game_init.find_possible_moves()
        if possible_moves:
            return random.choice(possible_moves)  # Choisi un mouvement aléatoire parmi les coups possibles
        return None  # Retourne None si aucun coup possible

    def play(self):
        while True:
            move = self.play_random_move()
            if move is None:
                print("Aucun coup possible. Fin du jeu.")
                break
            self.game_init.cross_points.append(move)  # Ajoute le coup choisi aux points joués
            self.game_init.played_cell.append(move)  # Optionnel: pour garder une trace de l'historique des coups joués
            print(f"Coup joué : {move}")
            # Ajouter une logique pour dessiner le coup sur la grille, si nécessaire
            # Vérifier la condition de fin de jeu, si applicable
