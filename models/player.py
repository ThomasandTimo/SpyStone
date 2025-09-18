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
        self.jump_charge_time = 2.0
        self.jump_direction = (0, 1)
        self.jump_press_time = None
        self.log_k = 5  # constante pour la courbe logarithmique

        # --- Gestion QTE ---
        self.qte_penalty = False          # si vrai, le joueur est ralenti
        self.qte_penalty_factor = 0.1     # vitesse réduite à 10%
        
        # --- Gestion Vent ---
        self.wind_force = 0               # force du vent appliquée au joueur

    # -------------------- Déplacements --------------------
    def move_left(self):
        speed = PLAYER_SPEED * (self.qte_penalty_factor if self.qte_penalty else 1)
        self.change_x = -speed

    def move_right(self):
        speed = PLAYER_SPEED * (self.qte_penalty_factor if self.qte_penalty else 1)
        self.change_x = speed

    def stop(self):
        self.change_x = 0

    # -------------------- Saut --------------------
    def start_jump(self, mouse_x=None, mouse_y=None):
        # Bloque le saut si pénalisé par un QTE
        if self.qte_penalty:
            return

        self.jump_charging = True
        self.jump_press_time = time.time()

        # Calcul de la direction si saut dirigé par la souris
        if mouse_x is not None and mouse_y is not None:
            dx = mouse_x - self.center_x
            dy = mouse_y - self.center_y
            length = math.hypot(dx, dy)
            if length > 0:
                self.jump_direction = (dx / length, dy / length)

    def release_jump(self):
        if not self.jump_charging:
            return

        elapsed = time.time() - self.jump_press_time

        if elapsed < MIN_CHARGE_TIME:
            # Saut basique
            self.change_y = BASIC_JUMP_SPEED
        else:
            # Saut chargé logarithmique
            t = min(elapsed, self.jump_charge_time)
            log_ratio = math.log(1 + self.log_k * t) / math.log(1 + self.log_k * self.jump_charge_time)
            applied_power = BASIC_JUMP_SPEED + (log_ratio * (self.max_jump_power - BASIC_JUMP_SPEED))
            self.change_x += applied_power * self.jump_direction[0]
            self.change_y += applied_power * self.jump_direction[1]

        self.jump_charging = False
        self.jump_press_time = None

    # -------------------- Update --------------------
    def update(self):
        # Appliquer gravité
        self.change_y -= GRAVITY
        
        # Appliquer la force du vent
        self.change_x += self.wind_force

        # Déplacement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rotation en fonction du déplacement horizontal
        self.angle -= (self.change_x / self.radius) * (180 / math.pi)

        # Mise à jour de la jauge de saut si en charge
        if self.jump_charging:
            elapsed = time.time() - self.jump_press_time
            t = min(elapsed, self.jump_charge_time)
            self.jump_power = (math.log(1 + self.log_k * t) / math.log(1 + self.log_k * self.jump_charge_time)) * self.max_jump_power

    # -------------------- QTE --------------------
    def apply_qte_penalty(self, active: bool):
        """
        Active/désactive le ralentissement du joueur pendant un QTE.
        :param active: True si le joueur est ralenti, False sinon
        """
        self.qte_penalty = active

    # -------------------- Helper --------------------
    def is_jumping(self):
        return self.jump_charging
    
    def reset_position(self, x=100, y=100):
        """
        Remet le joueur à la position initiale et réinitialise la vitesse et l'état de saut.
        :param x: coordonnée X de départ
        :param y: coordonnée Y de départ
        """
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0
        self.angle = 0
        self.jump_charging = False
        self.jump_power = 0
        self.jump_press_time = None
        self.jump_direction = (0, 1)

