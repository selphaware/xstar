from typing import List
from matplotlib import pyplot as plt

from xmath.structures import R2, R1, Z2_MATRIX


def plot_parametric(values: List[R2]):
    # Extract x and y values for plotting
    x_values: List[R1] = []
    y_values: List[R1] = []
    for _values in values:
        x_values.append([coord[0] for coord in _values])
        y_values.append([coord[1] for coord in _values])

    # Plotting
    plt.figure(figsize=(8, 6))
    for i in range(len(values)):
        plt.plot(x_values[i], y_values[i], label=f"Curve {i + 1}")

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Parametric Curve")
    plt.legend()
    plt.grid(True)

    # Ensure x and y axis grid units are equal
    plt.gca().set_aspect('equal', adjustable='datalim')

    # Optional: Adjust the limits to ensure the aspect ratio is enforced
    plt.tight_layout()

    plt.show()


def plot_num_grid(grid: Z2_MATRIX):
    # Plot the grid
    plt.figure(figsize=(8, 8))
    plt.imshow(grid, cmap='tab20c_r', origin='lower')
    # plt.colorbar(label="Shaded (1) / Unshaded (0)")
    plt.title("Int Grid Visualization")
    plt.xlabel("Column Index")
    plt.ylabel("Row Index")

    # Set x-axis ticks to match the number of columns
    plt.xticks(range(len(grid[0])))

    # Set y-axis ticks to match the number of rows
    plt.yticks(range(len(grid)))

    plt.grid(visible=False)
    plt.show()
