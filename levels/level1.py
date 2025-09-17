import os
import arcade
from config import ASSETS_PATH
from levels.level_base import LevelBase

class Level1(LevelBase):
    def __init__(self):
        super().__init__("Niveau 1", background_color=arcade.color.SKY_BLUE, background_image=os.path.join(ASSETS_PATH, "backgrounds", "background_glacial_mountains1.png"))
        self.level_end_x = 4000

    def setup(self):
        super().setup()
        
        # Liste de blocs à créer : (width, height, center_x, center_y, couleur)
        blocs = [
            # Sols
            (300, 1200, -300, 100, arcade.color.DARK_BROWN),
            (800, 40, 400, 20, arcade.color.DARK_BROWN),
            
            # Gros blocs
            (300, 450, 0, 200, arcade.color.BROWN),
            (500, 450, 970, 200, arcade.color.BROWN),
            
            # Plateformes bleues
            (120, 50, 230, 100, arcade.color.BLUE),
            (120, 50, 350, 280, arcade.color.BLUE),
            (120, 50, 490, 130, arcade.color.BLUE),
            (120, 50, 610, 350, arcade.color.BLUE),
            
            # Gros blocs droits
            (400, 200, 1300, 100, arcade.color.BROWN),
            (250, 80, 1600, 0, arcade.color.BROWN),
            
            # Sols
            (2500, 80, 3080, 0, arcade.color.BROWN),
            
             # Plafond au-dessus du bloc précédent
            (1200, 400, 2000, 600, arcade.color.BROWN),
            
             # Plafond au-dessus du bloc précédent
            (1200, 400, 2000, 600, arcade.color.BROWN),
            
            # Gros blocs droits
            (60, 620, 2850, 220, arcade.color.BROWN),
            
            # Plateformes bleues
            (120, 60, 2760, 100, arcade.color.BLUE),
            
            # Plateformes bleues
            (120, 60, 2660, 430, arcade.color.BLUE),
            
        ]

        # Création des sprites
        for width, height, x, y, color in blocs:
            bloc_droit = arcade.SpriteSolidColor(width, height, color)
            bloc_droit.center_x = x
            bloc_droit.center_y = y
            self.platforms.append(bloc_droit)

        # # --- Triggers de dialogue ---
        # self.dialogue_triggers = [
        #     {"x": 0, "lines": ["Bienvenue sur le premier niveau !"], "triggered": False},
        #     {"x": 100, "lines": ["Trouves un moyen de rejoindre l'autre côté !"], "triggered": False},
        #     {"x": 1200, "lines": ["Tu arrives bientôt à la fin !"], "triggered": False}
        # ]

        # --- QTE ---
        self.qte_triggers = [
            {
                "x": 1900,
                "key": arcade.key.E,
                "triggered": False,
                "on_success": lambda: print("QTE réussie !"),
                "on_fail": lambda: print("QTE échouée...")
            }
        ]


