import os
import math
import arcade
from config import ASSETS_PATH
import time

GRAVITY = 0.5
PLAYER_SPEED = 2
BASIC_JUMP_SPEED = 12
MIN_CHARGE_TIME = 0.2  # seuil pour différencier le saut basique et chargé

class Player(arcade.Sprite):
    """Le caillou joueur avec rotation et saut hybride logarithmique"""

    def __init__(self, radius=20):
        # Charge l'image du sprite 
        super().__init__(os.path.join(ASSETS_PATH, "rock.gif"), scale=1.5)
        self.radius = radius
        # Position et vitesse
        self.center_x = 100
        self.center_y = 100
        self.change_x = 0
        self.change_y = 0
        self.angle = 0

        # Saut hybride
        self.jump_charging = False
        self.jump_power = 0
        self.max_jump_power = 20
        self.jump_charge_time = 2.0  # temps max pour atteindre max_jump_power
        self.jump_direction = (0, 1)
        self.jump_press_time = None

        self.log_k = 5  # constante pour la courbe logarithmique

    # Déplacements horizontaux
    def move_left(self):
        self.change_x = -PLAYER_SPEED

    def move_right(self):
        self.change_x = PLAYER_SPEED

    def stop(self):
        self.change_x = 0

    # Appui sur la touche saut
    def start_jump(self, mouse_x=None, mouse_y=None):
        self.jump_charging = True
        self.jump_press_time = time.time()
        if mouse_x is not None and mouse_y is not None:
            dx = mouse_x - self.center_x
            dy = mouse_y - self.center_y
            length = math.hypot(dx, dy)
            if length > 0:
                self.jump_direction = (dx / length, dy / length)

    # Relâchement de la touche saut
    def release_jump(self):
        
        if not self.jump_charging:
            return

        elapsed = time.time() - self.jump_press_time

        if elapsed < MIN_CHARGE_TIME:
            # saut basique
            self.change_y = BASIC_JUMP_SPEED
        else:
            # saut chargé logarithmique
            t = min(elapsed, self.jump_charge_time)
            log_ratio = math.log(1 + self.log_k * t) / math.log(1 + self.log_k * self.jump_charge_time)
            applied_power = BASIC_JUMP_SPEED + (log_ratio * (self.max_jump_power - BASIC_JUMP_SPEED))
            self.change_x += applied_power * self.jump_direction[0]
            self.change_y += applied_power * self.jump_direction[1]

        self.jump_charging = False
        self.jump_press_time = None


    def update(self):
        # Appliquer gravité
        self.change_y -= GRAVITY

        # Déplacement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rotation en fonction du déplacement horizontal
        self.angle -= (self.change_x / self.radius) * (180 / math.pi)

        # Mise à jour de la puissance de saut pour la jauge
        if self.jump_charging:
            elapsed = time.time() - self.jump_press_time
            t = min(elapsed, self.jump_charge_time)
            self.jump_power = (math.log(1 + self.log_k * t) / math.log(1 + self.log_k * self.jump_charge_time)) * self.max_jump_power

    def is_jumping(self):
        return self.jump_charging
