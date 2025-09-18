import os
import arcade
from levels.level_base import LevelBase

class Level3(LevelBase):
    def __init__(self):
        super().__init__("Niveau 2", background_image=os.path.join("assets/background_glacial_mountains.png"))

    def setup(self):
        super().setup()

        # Pente ascendante : on crée une série de "segments" pour simuler la pente
        pente_length = 1000  # largeur totale du niveau
        segment_width = 20   # largeur d'un segment de pente
        start_y = 20         # point de départ en bas
        end_y = 400          # point final en haut (2/3 de la hauteur)
        num_segments = pente_length // segment_width

        for i in range(num_segments):
            x = segment_width / 2 + i * segment_width
            # interpolation linéaire pour avoir une pente régulière
            y = start_y + (end_y - start_y) * (i / num_segments)
            segment = arcade.SpriteSolidColor(segment_width, 10, arcade.color.DARK_BROWN)
            segment.center_x = x
            segment.center_y = y
            self.platforms.append(segment)

        # Triggers de dialogue
        self.dialogue_triggers = [
            {"x": 100, "lines": ["Niveau 2 : La pente commence !"], "triggered": False},
            {"x": 900, "lines": ["Vous atteignez presque le sommet !"], "triggered": False}
        ]

        # QTE simple
        self.qte_triggers = [
            {
                "x": 300,
                "key": arcade.key.E,
                "triggered": False,
                "on_success": lambda: print("QTE réussie !"),
                "on_fail": lambda: print("QTE échouée...")
            }
        ]

    def update(self, delta_time):
        pass
