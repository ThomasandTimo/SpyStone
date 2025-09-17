# core/qte_manager.py
import arcade
import time

class QTEManager:
    def __init__(self):
        self.active = False
        self.required_key = None
        self.start_time = None
        self.duration = 2.0  # durée max en secondes
        self.success_callback = None
        self.fail_callback = None

    def start_qte(self, required_key, success_callback=None, fail_callback=None):
        self.active = True
        self.required_key = required_key
        self.start_time = time.time()
        self.success_callback = success_callback
        self.fail_callback = fail_callback

    def update(self):
        if self.active and (time.time() - self.start_time > self.duration):
            # Échec par timeout
            self.active = False
            if self.fail_callback:
                self.fail_callback()

    def handle_key_press(self, key):
        if self.active:
            if key == self.required_key:
                self.active = False
                if self.success_callback:
                    self.success_callback()
            else:
                # Mauvaise touche = échec
                self.active = False
                if self.fail_callback:
                    self.fail_callback()

    def draw(self, camera_x):
        if self.active:
            arcade.draw_text(
                f"Appuie sur {arcade.key.name(self.required_key)} !",
                camera_x + 200, 400,
                arcade.color.YELLOW, 20
            )
            # Barre de temps restante
            elapsed = time.time() - self.start_time
            remaining_ratio = max(0, 1 - elapsed / self.duration)
            arcade.draw_rectangle_filled(
                camera_x + 250, 370,
                200 * remaining_ratio, 20,
                arcade.color.RED
            )
