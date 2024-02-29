import numpy as np
import matplotlib.pyplot as plt

# Create a 20x20 grid initialized with zeros
grid = np.zeros((20, 20), dtype=int)

# Marking the points in a Greek cross
cross_points = [
    (5, 8), (6, 8), (7, 8),(8, 8),(8, 7),(8, 6),(8, 5),
    (14, 8), (13, 8), (12, 8), (11, 8), (11, 7), (11, 6), (11, 5),
     (10, 5), (9, 5), (5, 9), (5, 10), (5, 11),(14, 9),(14, 10),(14, 11),(13, 11),
(12, 11),(11, 11),(6, 11),(7, 11),
(8, 11),(8, 12), (8, 13), (8, 14),(11, 12),(11, 13), (11, 14), (9, 14),(10, 14)
]

# Setting the marked points to 1
for x, y in cross_points:
    grid[x, y] = 1

# Plotting the grid
plt.figure(figsize=(8, 8))  # Adjust the figure size to make each cell clearly visible
plt.imshow(grid, cmap='Reds', interpolation='nearest')
plt.xticks(range(20))  # Set x-axis ticks to match grid size
plt.yticks(range(20))  # Set y-axis ticks to match grid size
plt.grid(True, color='black', linewidth=2)  # Add grid lines for better visualization
plt.show()
