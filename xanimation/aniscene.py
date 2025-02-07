from typing import Tuple
import matplotlib.pyplot as plt

from xanimation.pscene import PhysicalScene


class AnimatedScene:
    def __init__(
            self,
            scene: PhysicalScene,
            xlim: Tuple[int, int] = (-100, 100),
            ylim: Tuple[int, int] = (-100, 100)
    ) -> None:
        self.scene: PhysicalScene = scene
        self.fig, self.ax = plt.subplots()

        self.ax.set_xlim(*xlim)
        self.ax.set_ylim(*ylim)

        for obj in self.scene.objects:
            self.ax.add_patch(obj.patch)
