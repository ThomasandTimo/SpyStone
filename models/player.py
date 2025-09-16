import arcade

GRAVITY = 0.5
PLAYER_SPEED = 2
PLAYER_JUMP_SPEED = 12

class Player(arcade.SpriteCircle):
    """Le caillou joueur"""
    def __init__(self, radius=20, color=arcade.color.DARK_BROWN):
        super().__init__(radius, color)
        self.change_x = 0
        self.change_y = 0

    def move_left(self):
        self.change_x = -PLAYER_SPEED

    def move_right(self):
        self.change_x = PLAYER_SPEED

    def stop(self):
        self.change_x = 0

    def jump(self, physics_engine):
        if physics_engine.can_jump():
            self.change_y = PLAYER_JUMP_SPEED
