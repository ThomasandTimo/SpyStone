import arcade
import random

class Bonus(arcade.SpriteSolidColor):
    """Bonus à collecter"""
    def __init__(self, width=20, height=20, color=arcade.color.GOLD):
        super().__init__(width, height, color)
        self.center_x = random.randint(200, 1800)
        self.center_y = random.randint(150, 400)
