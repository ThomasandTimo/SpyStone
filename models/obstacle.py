import arcade
import random

class FallingObstacle(arcade.SpriteSolidColor):
    """Obstacle qui tombe du haut de l'écran"""
    def __init__(self, width=20, height=20, color=arcade.color.RED, platforms=None):
        super().__init__(width, height, color)
        self.center_x = random.randint(200, 1000)
        self.center_y = random.randint(600, 1200)
        self.speed = random.uniform(2, 5)
        self.platforms = platforms  # SpriteList ou liste de plateformes

    def update(self):
        # Si déjà posé sur une plateforme, ne plus bouger
        if hasattr(self, '_landed') and self._landed:
            return
        self.center_y -= self.speed
        # Collision avec plateformes
        if self.platforms:
            for platform in self.platforms:
                if arcade.check_for_collision(self, platform):
                    self.center_y = platform.top + self.height / 2
                    self._landed = True
                    return
        # Repositionner en haut si sorti de l'écran
        if self.center_y < 0:
            self.center_y = random.randint(600, 1200)
            self.center_x = random.randint(200, 1000)
            self._landed = False
