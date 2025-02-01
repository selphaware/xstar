from typing import List, Dict, Union
from matplotlib import pyplot as plt

from xmath.structures import R2, R1, Z2_MATRIX, UNIVERSE_STRUCT


def plot_parametric(name: str,
                    values: List[R2],
                    marker_type: str = None,
                    marker_size: float = None,
                    marker_color: str = None,
                    marker_edge: str = None,
                    line_style: str = None,
                    line_width: float = None):
    # Extract x and y values for plotting
    x_values: List[R1] = []
    y_values: List[R1] = []
    for _values in values:
        x_values.append([coord[0] for coord in _values])
        y_values.append([coord[1] for coord in _values])

    # Plotting
    for i in range(len(values)):
        plt.plot(x_values[i], y_values[i],
                 marker=marker_type,
                 markersize=marker_size,
                 markerfacecolor=marker_color,
                 markeredgecolor=marker_edge,
                 linestyle=line_style,
                 linewidth=line_width,
                 label=f"{name}: {i + 1}")


def plot_parametric_universe(
        values: UNIVERSE_STRUCT,
        show_galaxy_motion_path: bool = True,
        show_planets_motion_path: bool = True,
        show_stars: bool = True

):
    plt.figure(figsize=(8, 6))

    if show_galaxy_motion_path:
        galaxy_coords = []
        for gname, galaxy in values.items():
            galaxy_coords.append(galaxy['motion_path'])
            plot_parametric(gname, [galaxy['motion_path']], line_style="--",
                            line_width=0.5)

    if show_planets_motion_path:
        system_coords = []
        for gname, galaxy in values.items():
            for sname, system in galaxy['star_systems'].items():
                system_coords.extend(system['planet_orbit_path'])
                plot_parametric(sname, system['planet_orbit_path'])

    if show_stars:
        star_coords = []
        for gname, galaxy in values.items():
            for sname, system in galaxy['star_systems'].items():
                star_coords.extend(system['origin'])
                if system['is_centre']:
                    plot_parametric(
                        sname, system['origin'], marker_type="o",
                        marker_size=11, marker_color="black",
                        marker_edge="black"
                    )
                else:
                    plot_parametric(
                        sname, system['origin'], marker_type="*",
                        marker_size=8
                    )

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Universe Parametric Curve")
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
