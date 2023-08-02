from manim import *

class IterateColor(Scene):
    def construct(self):
        text = Text("Colors", font_size=96)
        # self.play(text.animate.set_color(RED))
        for letter in text:
            self.play(letter.animate.set_color(RED))
            self.wait()
