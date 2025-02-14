import pdb
import random

from xanimation.aniscene import AnimatedScene
from xanimation.pobject import PhysicalObject
from xanimation.pscene import PhysicalScene
from xmath.gobj import generate_square_points, generate_circle_points, \
    generate_isosceles_triangle_points, \
    generate_spiked_circle_points, generate_trapezium_points, \
    generate_polygon_points
from xmath.xrandom import random_int_generator


def create_sector() -> PhysicalScene:
    # 1) Create our Scene
    scene = PhysicalScene()

    # 2) Create various objects spread around the coordinate range.
    # Example: a circle at (200, 100) with radius=30, velocity=(2,0)
    circle_coords = generate_circle_points(center=(200, 100), radius=30,
                                           num_points=60)
    circle_obj = PhysicalObject(circle_coords, velocity=(2, 0),
                                _rotation_speed_deg=0.0, color='red')
    scene.add_object(circle_obj, main=False)  # Make the circle the main object

    # A square at (-150, 400), side_length=50, velocity=(0,-1), rotation=10
    # deg/unit
    square_coords = generate_square_points(center=(100, 100), side_length=50)
    square_obj = PhysicalObject(square_coords, velocity=(0, 0),
                                _rotation_speed_deg=75.0, color='green')
    scene.add_object(square_obj, main=False)

    square_coords2 = generate_square_points(center=(-2550, 400),
                                            side_length=50)
    square_obj2 = PhysicalObject(square_coords2, velocity=(100, 10),
                                 _rotation_speed_deg=275.0, color='yellow')
    scene.add_object(square_obj2, main=False)

    # Another circle far away, with velocity=(-1.5, 1.0), rotation=0
    another_circle_coords = generate_circle_points(center=(800, -300),
                                                   radius=15)
    another_circle_obj = PhysicalObject(another_circle_coords,
                                        velocity=(-1.5, 1.0),
                                        _rotation_speed_deg=0.0,
                                        color='blue')
    scene.add_object(another_circle_obj, main=False)

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
                attachments=[
                    PhysicalObject(
                        generate_circle_points(
                            center=ship_coords[0],
                            radius=1
                        ),
                        velocity=(0, 0),
                        is_main=False,
                        color="yellow"
                    )
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
                attachments=[
                    PhysicalObject(
                        generate_circle_points(
                            center=ship_coords[1],
                            radius=1
                        ),
                        velocity=(0, 0),
                        is_main=False,
                        color="yellow"
                    )
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
    rnd_xp = random_int_generator(-3000, 3000, "RXp")
    rnd_yp = random_int_generator(-3000, 3000, "RYp")
    rnd_r = random_int_generator(1, 30, "RR")
    rnd_s = random_int_generator(3, 7, "RS")

    for _ in range(1000):
        ship_coords = generate_polygon_points(
            (next(rnd_xp), next(rnd_yp)),
            next(rnd_r),
            next(rnd_s)
        )
        ship_obj = PhysicalObject(
            ship_coords,
            velocity=(next(rnd_x) / 10_000, next(rnd_y) / 10_000),
            _rotation_speed_deg=15.0,
            color=random.choice([
                "blue", "purple", "white", "grey", "green", "pink"
            ])
        )
        scene.add_object(ship_obj, main=False)

    # stars
    rnd_x = random_int_generator(-3000, 3000, "RX")
    rnd_y = random_int_generator(-3000, 3000, "RY")
    rnd_r = random_int_generator(5, 75, "RR")
    rnd_s = random_int_generator(75, 400, "RS")
    rnd_d = random_int_generator(0, 200, "RD")
    for _ in range(100):
        star_coords = generate_spiked_circle_points(
            center=(next(rnd_x), next(rnd_y)),
            radius=next(rnd_r),
            num_spikes=next(rnd_s),
            spike_height=10
        )
        star_obj = PhysicalObject(
            star_coords,
            velocity=(0, 0),
            _rotation_speed_deg=next(rnd_d),
            color=random.choice([
                "yellow", "red", "orange"
            ])
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
