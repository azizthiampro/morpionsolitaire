import matplotlib.pyplot as plt

def plot_grid_with_crosses(points):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    for point in points:
        ax.plot(point[0], point[1], 'k+', markersize=10, mew=2)

    plt.show()

# Fonction pour générer les points en forme de croix grecque
def generate_crosses(size):
    crosses = []
    # Points sur les côtés de la croix
    for i in range(size):
        crosses.append((i, size//2))  # Horizontal
        crosses.append((size//2, i))  # Vertical
    # Point au centre de la croix
    crosses.append((size//2, size//2))
    return crosses

# Taille de la grille
grid_size = 20

# Générer les points en forme de croix grecque
cross_points = generate_crosses(grid_size)

# Afficher la grille avec les croix
plot_grid_with_crosses(cross_points)
