# core/qte_manager.py
import arcade
import time

class QTEManager:
    def __init__(self, player):
        self.active = False
        self.required_key = None
        self.start_time = None
        self.duration = 2.0  # durée max en secondes
        self.success_callback = None
        self.fail_callback = None
        self.player = player

    def start_qte(self, required_key, success_callback=None, fail_callback=None):
        self.active = True
        self.required_key = required_key
        self.start_time = time.time()
        self.success_callback = success_callback
        self.fail_callback = fail_callback
        self.player.apply_qte_penalty(True)


    def update(self):
        if self.active and (time.time() - self.start_time > self.duration):
            # Échec par timeout
            self.active = False
            if self.fail_callback:
                self.fail_callback()

    def handle_key_press(self, key):
        if not self.active:
            return

        # Touches autorisées à passer sans provoquer l'échec
        allowed_keys = [arcade.key.LEFT, arcade.key.RIGHT, arcade.key.SPACE]

        if key in allowed_keys:
            # Ces touches ne font rien au QTE
            return

        if key == self.required_key:
            # Bonne touche => succès
            self.active = False
            if self.success_callback:
                self.player.apply_qte_penalty(False)
                self.success_callback()
        else:
            # Mauvaise touche => échec
            self.active = False
            if self.fail_callback:
                self.player.apply_qte_penalty(True)  # optionnel, ralentir joueur
                self.fail_callback()


    def draw(self, camera_x):
        if self.active:
            screen_center_x = camera_x + 10  # Centré horizontalement

            # Texte 1 : en haut
            arcade.draw_text(
                "You are stuck !!!",
                screen_center_x, 470,  # Position Y haute
                arcade.color.BLUE, 25,
                anchor_x="center"
            )

            # Texte 2 : en dessous
            arcade.draw_text(
                "Press E!",
                screen_center_x, 430,
                arcade.color.BLUE, 25,
                anchor_x="center",
            )

            # Barre de progression : centrée et en dessous du texte
            elapsed = time.time() - self.start_time
            remaining_ratio = max(0, 1 - elapsed / self.duration)
            bar_width = 200
            bar_height = 20
            filled_width = bar_width * remaining_ratio

            # Fond de la barre (gris clair)
            arcade.draw_rectangle_filled(
                screen_center_x, 390,  # Y plus bas
                bar_width, bar_height,
                arcade.color.LIGHT_GRAY
            )

            # Barre rouge (temps restant)
            arcade.draw_rectangle_filled(
                screen_center_x - (bar_width - filled_width) / 2, 390,
                filled_width, bar_height,
                arcade.color.RED
            )

            # Bordure noire
            arcade.draw_rectangle_outline(
                screen_center_x, 390,
                bar_width, bar_height,
                arcade.color.BLACK, 2
            )

