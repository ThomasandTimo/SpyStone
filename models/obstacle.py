import arcade
import random

class FallingObstacle(arcade.SpriteSolidColor):
    """Obstacle qui tombe du haut de l'écran"""
    def __init__(self, width=20, height=20, color=arcade.color.RED):
        super().__init__(width, height, color)
        self.center_x = random.randint(200, 1000)
        self.center_y = random.randint(600, 1200)
        self.speed = random.uniform(2, 5)

    def update(self):
        self.center_y -= self.speed
        # Repositionner en haut si sorti de l'écran
        if self.center_y < 0:
            self.center_y = random.randint(600, 1200)
            self.center_x = random.randint(200, 1000)
