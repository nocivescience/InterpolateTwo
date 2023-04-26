from manim import *

class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        square = Square()
        circle.pointwise_become_partial(
            square,
            interpolate(-0.7, 1, 1),
            interpolate(0, 1.7, 1)
        )
        self.play(self.wait(1))
