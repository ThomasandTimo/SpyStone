import arcade

class Platform(arcade.SpriteSolidColor):
    """Plateforme simple"""
    def __init__(self, width, height, color, center_x, center_y):
        super().__init__(width, height, color)
        self.center_x = center_x
        self.center_y = center_y
