import math
import arcade

GRAVITY = 0.5
PLAYER_SPEED = 2

class Player(arcade.Sprite):
    """Le caillou joueur avec rotation visible et saut lance-pierre"""

    def __init__(self, radius=20):
        super().__init__()
        self.radius = radius
        stone_size = radius * 2

        # Sprite du joueur
        self.texture = arcade.make_circle_texture(stone_size, arcade.color.DIM_GRAY)
        self.width = stone_size
        self.height = stone_size

        # Position et vitesse
        self.center_x = 100
        self.center_y = 100
        self.change_x = 0
        self.change_y = 0
        self.angle = 0

        # --- Saut lance-pierre ---
        self.jump_charging = False       # Est-ce que le saut est en cours de charge
        self.jump_power = 0              # Puissance actuelle du saut
        self.max_jump_power = 20         # Puissance maximale
        self.jump_charge_rate = 0.3      # Vitesse de charge par frame
        self.jump_direction = (0, 1)     # Direction du saut (unit vector)
        self.target_x = self.center_x    # Coordonnée x de la souris
        self.target_y = self.center_y    # Coordonnée y de la souris

    # Déplacements horizontaux
    def move_left(self):
        self.change_x = -PLAYER_SPEED

    def move_right(self):
        self.change_x = PLAYER_SPEED

    def stop(self):
        self.change_x = 0

    # Démarrer la charge du saut
    def start_jump_charge(self, mouse_x=None, mouse_y=None):
        self.jump_charging = True
        self.jump_power = 0
        if mouse_x is not None and mouse_y is not None:
            dx = mouse_x - self.center_x
            dy = mouse_y - self.center_y
            length = math.hypot(dx, dy)
            if length > 0:
                self.jump_direction = (dx / length, dy / length)

    # Libérer le saut
    def release_jump(self):
        if self.jump_charging:
            # Appliquer la puissance du saut dans la direction ciblée
            self.change_x += self.jump_power * self.jump_direction[0]
            self.change_y += self.jump_power * self.jump_direction[1]
            self.jump_charging = False
            self.jump_power = 0

    def update(self):
        # --- Charger le saut si nécessaire ---
        if self.jump_charging:
            self.jump_power += self.jump_charge_rate
            if self.jump_power > self.max_jump_power:
                self.jump_power = self.max_jump_power

        # Appliquer la gravité
        self.change_y -= GRAVITY

        # Déplacement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rotation du caillou en fonction du déplacement horizontal
        self.angle -= (self.change_x / self.radius) * (180 / math.pi)
