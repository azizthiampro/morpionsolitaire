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
        self.invalid_moves = []

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

        # Points and score
        self.cross_points = self.init_cross_points()
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def init_cross_points(self):
        # Initialize the cross points for the game start
        return [...]  # Your list of initial cross points

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
        if not self.can_create_line(self.cross_points):
            print("Fin de la partie. Votre score est :", self.score)
            return False
        return True

    def draw_game_elements(self):
        self.screen.fill(self.black)
        self.draw_grid()
        self.draw_cross_points()
        self.draw_played_lines()
        self.draw_invalid_moves()
        self.draw_score()

    def main_loop(self):
        running = True
        while running:
            running = self.handle_events()
            game_continues = self.update_game_state()
            if not game_continues:
                running = False
            self.draw_game_elements()
            pygame.display.flip()
        pygame.quit()

    # Methods for drawing grid, cross points, played lines, invalid moves, and score
    def draw_grid(self):
        pass

    def draw_cross_points(self):
        pass

    def draw_played_lines(self):
        pass

    def draw_invalid_moves(self):
        pass

    def draw_score(self):
        pass

    # Remaining methods unchanged...
