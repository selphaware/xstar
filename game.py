import pdb
import random

import numpy as np

from xanimation.aniscene import AnimatedScene
from xanimation.pobject import PhysicalObject
from xanimation.pscene import PhysicalScene
from xmath.fplot.ani3 import velocity
from xmath.gobj import generate_square_points, generate_circle_points, \
    generate_isosceles_triangle_points, \
    generate_spiked_circle_points, generate_trapezium_points, \
    generate_polygon_points
from xmath.xrandom import random_int_generator


def create_sector() -> PhysicalScene:
    # 1) Create our Scene
    scene = PhysicalScene()

    # main SHIP
    ship_coords = generate_isosceles_triangle_points(
        center=(50, 50),
        base=8,
        height=10
    )
    ship_obj = PhysicalObject(
        ship_coords,
        velocity=(0, 0),
        _rotation_speed_deg=0.0,
        attachments=[  # gun
            # GUN 1
            PhysicalObject(
                generate_square_points(
                    center=ship_coords[0],
                    side_length=3
                ),
                velocity=(0, 0),
                attachments=[  # torpedoes
                    PhysicalObject(
                        generate_circle_points(
                            center=ship_coords[0],
                            radius=1
                        ),
                        velocity=(0, 0),
                        is_main=False,
                        color="yellow"
                    )
                    for _ in range(100)
                ],
                is_main=False,
                color="red",
            ),

            # GUN 2
            PhysicalObject(
                generate_square_points(
                    center=ship_coords[1],
                    side_length=3
                ),
                velocity=(0, 0),
                attachments=[  # torpedoes
                    PhysicalObject(
                        generate_circle_points(
                            center=ship_coords[1],
                            radius=1
                        ),
                        velocity=(0, 0),
                        is_main=False,
                        color="yellow"
                    )
                    for _ in range(100)
                ],
                is_main=False,
                color="red",
            )
        ],
        is_main=True,
        color='cyan'
    )
    scene.add_object(ship_obj, main=True)

    # other random ships
    rnd_x = random_int_generator(-5_000_000, 5_000_000, "RX")
    rnd_y = random_int_generator(-5_000_000, 5_000_000, "RY")
    rnd_xp = random_int_generator(-300, 300, "RXp")
    rnd_yp = random_int_generator(-300, 300, "RYp")
    rnd_r = random_int_generator(1, 30, "RR")
    rnd_s = random_int_generator(3, 7, "RS")
    rnd_d = random_int_generator(0, 200, "RD")

    for _ in range(25):
        ship_coords = generate_polygon_points(
            (next(rnd_xp), next(rnd_yp)),
            next(rnd_r),
            next(rnd_s)
        )
        ship_obj = PhysicalObject(
            ship_coords,
            velocity=(next(rnd_x) / 10_000, next(rnd_y) / 10_000),
            _rotation_speed_deg=next(rnd_d),
            color=random.choice([
                "blue", "purple", "white", "grey", "green", "pink"
            ])
        )
        scene.add_object(ship_obj, main=False)

    # big stars
    rnum = 700_000
    rnd_x = random_int_generator(-rnum, rnum, "RX")
    rnd_y = random_int_generator(-rnum, rnum, "RY")
    rnd_r = random_int_generator(100, 1000, "RR")
    rnd_s = random_int_generator(400, 600, "RS")
    rnd_d = random_int_generator(5, 450, "RD")
    for _ in range(1000):
        _radius = next(rnd_r)
        star_coords = generate_circle_points(
            center=(next(rnd_x), next(rnd_y)),
            radius=_radius
        )
        star_obj = PhysicalObject(
            star_coords,
            velocity=(0, 0),
            _rotation_speed_deg=0,  # next(rnd_d),
            color=random.choice([
                "yellow", "red", "orange", "purple", "pink", "cyan"
            ])
        )
        scene.add_object(star_obj, main=False)

    pcts = [5, 10, 15, 25]
    colors = ["yellow", "red", "orange", "purple", "pink", "cyan"]
    for _ in range(5):
        _radius = next(rnd_r)
        star_coords = generate_circle_points(
            center=(next(rnd_x), next(rnd_y)),
            radius=_radius
        )
        star_obj = PhysicalObject(
            star_coords,
            velocity=(0, 0),
            _rotation_speed_deg=(deg_turn := next(rnd_d)),
            attachments=[
                PhysicalObject(
                    generate_circle_points(
                        center=(
                            np.random.uniform(
                                min(star_coords[:, 0]),
                                max(star_coords[:, 0]),
                                1
                            ),
                            np.random.uniform(
                                min(star_coords[:, 1]),
                                max(star_coords[:, 1]),
                                1
                            )
                        ),
                        radius=10
                    ),
                    velocity=(0., 0.),
                    is_main=False,
                    color=random.choice(colors)
                )
                for _ipct in pcts
            ],
            is_main=True,
            color=random.choice(colors)
        )
        scene.add_object(star_obj, main=False)

    return scene


def animate_scene(scene: PhysicalScene) -> None:
    # 3) Create the animator, start the input thread, and run
    animator = AnimatedScene(scene, center_grid=True,
                             full_screen=True, debug=True)
    animator.start_input_thread()
    animator.run()


def run_game():
    scene = create_sector()
    animate_scene(scene)


if __name__ == "__main__":
    run_game()
