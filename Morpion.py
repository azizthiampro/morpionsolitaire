import pygame
import sys

class GameInit:
    def __init__(self):
        # Initialisation et configuration existantes
        self.all_valid_sequences = []  # Ajout pour stocker les séquences valides détectées
        self.sequence_ends = []

    # Méthodes existantes inchangées...

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
                        all_valid_sequences.append((sequence, normalized_direction))

        return all_valid_sequences

    def highlight_sequence_ends(self, all_valid_sequences):
        for sequence, _ in all_valid_sequences:
            # Prendre en compte uniquement les extrémités de chaque séquence
            for end in (sequence[0], sequence[-1]):
                self.draw_dot(*end, self.blue)  # Dessiner les extrémités en bleu

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    cell = self.get_cell_from_mouse_pos(pos)

                    # Réinitialiser les séquences valides et les extrémités si on commence une nouvelle recherche
                    if not self.all_valid_sequences:
                        self.all_valid_sequences = self.find_all_valid_sequences_with_center(cell)
                        if len(self.all_valid_sequences) == 1:
                            # S'il n'y a qu'une seule séquence valide, la jouer automatiquement
                            self.play_sequence(self.all_valid_sequences[0][0])
                            self.all_valid_sequences.clear()  # Réinitialiser pour la prochaine recherche
                        elif self.all_valid_sequences:
                            # Mettre en surbrillance les extrémités des séquences pour la sélection par l'utilisateur
                            self.highlight_sequence_ends()
                    else:
                        # Vérifier si le clic est sur une extrémité de séquence valide
                        if self.is_click_on_end(cell):
                            for sequence, _ in self.all_valid_sequences:
                                if cell in [sequence[0], sequence[-1]]:
                                    self.play_sequence(sequence)
                                    break  # Sortir de la boucle une fois la séquence trouvée et jouée
                            self.all_valid_sequences.clear()  # Réinitialiser après la sélection
                            self.sequence_ends.clear()  # Réinitialiser les extrémités après la sélection

            self.screen.fill(self.black)

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

            if self.all_valid_sequences:
                for sequence in self.all_valid_sequences:
                    for point in sequence[0]:  # sequence[0] est la séquence, sequence[1] serait la direction
                        self.draw_dot(*point, self.blue)

                # Mettre à jour l'affichage à chaque itération de la boucle
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

    def main_loop(self):
        # Main loop of the game
        running = True
        update_possible_moves = True  # Initialize flag to update and print possible moves

        while running:
            if update_possible_moves:
                possible_moves = self.find_possible_moves()  # Find possible moves at the current state
                print("Possible moves: ", possible_moves)  # Print the list of possible moves
                update_possible_moves = False  # Reset flag until the next change

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    update_possible_moves = True  # Set flag to update possible moves on the next loop
                    pos = pygame.mouse.get_pos()
                    cell = self.get_cell_from_mouse_pos(pos)
                    valid, sequence, direction = self.find_valid_sequence_with_center(cell)

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