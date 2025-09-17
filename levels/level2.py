import os
import arcade
from levels.level_base import LevelBase

class Level2(LevelBase):
    def __init__(self):
        super().__init__("Niveau 2", background_image=os.path.join("assets/background_glacial_mountains.png"))

    def setup(self):
        super().setup()

        # Sol découpé pour laisser un trou centré à x=850 de 120px de large
        largeur_sol = 1000
        centre_trou = 850
        largeur_trou = 120
        largeur_gauche = centre_trou - largeur_trou // 2  # 790
        largeur_droite = largeur_sol - (largeur_gauche + largeur_trou)  # 90

        sol_gauche = arcade.SpriteSolidColor(largeur_gauche, 40, arcade.color.DARK_BROWN)
        sol_gauche.center_x = largeur_gauche // 2
        sol_gauche.center_y = 20
        self.platforms.append(sol_gauche)

        sol_droit = arcade.SpriteSolidColor(largeur_droite, 40, arcade.color.DARK_BROWN)
        sol_droit.center_x = largeur_gauche + largeur_trou + largeur_droite // 2
        sol_droit.center_y = 20
        self.platforms.append(sol_droit)

        # Plateformes supplémentaires
        self.platforms.append(arcade.SpriteSolidColor(250, 30, arcade.color.DARK_BROWN))
        self.platforms[-1].center_x = 150
        self.platforms[-1].center_y = 120

        self.platforms.append(arcade.SpriteSolidColor(200, 30, arcade.color.DARK_BROWN))
        self.platforms[-1].center_x = 500
        self.platforms[-1].center_y = 220

        self.platforms.append(arcade.SpriteSolidColor(150, 30, arcade.color.DARK_BROWN))
        self.platforms[-1].center_x = 800
        self.platforms[-1].center_y = 320

        # Obstacles : 2 pour le niveau 2
        from models.obstacle import FallingObstacle
        for i in range(2):
            obstacle = FallingObstacle(platforms=self.platforms)
            obstacle.center_x = 600 + i*100
            obstacle.center_y = 350 + i*50
            self.obstacles.append(obstacle)

        # Trous (exemple)
        from models.hole import Hole
        self.holes = [
            Hole(center_x=850, width=120),
        ]

        # Triggers de dialogue
        self.dialogue_triggers = [
            {"x": 200, "lines": ["Niveau 2 : la pente se corse !"], "triggered": False},
            {"x": 850, "lines": ["Un précipice... Trouve un moyen de passer !"], "triggered": False}
        ]
        
        self.qte_triggers = [
            {
                "x": 200,
                "key": arcade.key.E,
                "triggered": False,
                "on_success": lambda: print("QTE réussie !"),
                "on_fail": lambda: print("QTE échouée...")
            }
        ]

    def update(self, delta_time):
        # Logique spécifique au niveau (optionnel)
        pass
