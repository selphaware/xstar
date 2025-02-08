from xanimation.aniscene import AnimatedScene
from xanimation.pobject import PhysicalObject
from xanimation.pscene import PhysicalScene
from xmath.gobj import generate_square_points, generate_circle_points


def create_sector():
    # 1) Create our Scene
    scene = PhysicalScene()

    # 2) Create various objects spread around the coordinate range.
    # Example: a circle at (200, 100) with radius=30, velocity=(2,0)
    circle_coords = generate_circle_points(center=(200, 100), radius=30,
                                           num_points=60)
    circle_obj = PhysicalObject(circle_coords, velocity=(2, 0),
                                rotation_speed_deg=0.0, color='red')
    scene.add_object(circle_obj, main=False)  # Make the circle the main object

    # A square at (-150, 400), side_length=50, velocity=(0,-1), rotation=10
    # deg/unit
    square_coords = generate_square_points(center=(-150, 400), side_length=50)
    square_obj = PhysicalObject(square_coords, velocity=(0, -1),
                                rotation_speed_deg=10.0, color='green')
    scene.add_object(square_obj, main=True)

    # Another circle far away, with velocity=(-1.5, 1.0), rotation=0
    another_circle_coords = generate_circle_points(center=(800, -300),
                                                   radius=15)
    another_circle_obj = PhysicalObject(another_circle_coords,
                                        velocity=(-1.5, 1.0),
                                        rotation_speed_deg=0.0,
                                        color='blue')
    scene.add_object(another_circle_obj, main=False)

    # 3) Create the animator, start the input thread, and run
    animator = AnimatedScene(scene)
    animator.start_input_thread()
    animator.run()


if __name__ == "__main__":
    create_sector()
