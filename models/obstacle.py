import arcade
import random
import os
from config import ASSETS_PATH

class FallingObstacle(arcade.Sprite):
    """Obstacle qui tombe du haut de l'écran"""
    def __init__(self, image_path=None, width=20, height=20, color=arcade.color.RED, platforms=None):
        if image_path is None:
            image_path = os.path.join(ASSETS_PATH, "snowball.png")
        super().__init__(image_path, scale=width/64)  # suppose une image 64x64px par défaut
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
                    self.remove_from_sprite_lists()
                    self._landed = True
                    return
        # Repositionner en haut si sorti de l'écran
        if self.center_y < 0:
            self.center_y = random.randint(600, 1200)
            self.center_x = random.randint(200, 1000)
            self._landed = False
