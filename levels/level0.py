import os
import arcade
from config import ASSETS_PATH
from levels.level_base import LevelBase

class Level0(LevelBase):
    def __init__(self):
        super().__init__("Niveau 1", background_color=arcade.color.SKY_BLUE, background_image=os.path.join(ASSETS_PATH, "backgrounds", "background_glacial_mountains1.png"))
        self.level_end_x = 1500
    def setup(self):
        super().setup()
        
        # --- Sol ---
        sol = arcade.SpriteSolidColor(2300, 40, arcade.color.DARK_BROWN)
        sol.center_x = 800
        sol.center_y = 20
        self.platforms.append(sol)
        
        # --- Sol ---
        sol = arcade.SpriteSolidColor(200, 200, arcade.color.DARK_BROWN)
        sol.center_x = 600
        sol.center_y = 20
        self.platforms.append(sol)
        
        # --- Sol ---
        sol = arcade.SpriteSolidColor(80, 650, arcade.color.DARK_BROWN)
        sol.center_x = 1000
        sol.center_y = 20
        self.platforms.append(sol)


        # # --- Obstacles ---
        # from models.obstacle import FallingObstacle
        # obstacle = FallingObstacle(platforms=self.platforms)
        # obstacle.center_x = 500
        # obstacle.center_y = 300
        # self.obstacles.append(obstacle)

        # --- Triggers de dialogue ---
        self.dialogue_triggers = [
            {
                "x": 0,  # Ignoré pour le tutoriel
                "lines": [
                    "Bienvenue, petit caillou !",
                    "Utilise ← et → pour avancer."
                ],
                "triggered": False
            },
            {
                "x": 350,
                "lines": [
                    "Bravo ! Tu avances !",
                    "Appuie sur SPACE pour sauter."
                ],
                "triggered": False
            },
            {
                "x": 580,
                "lines": [
                    "Excellent ! Saut réussi !",
                ],
                "triggered": False
            },
             {
                "x": 850,
                "lines": [
                    "Oh non ! un obstacle plus grand !",
                    "Maintient SPACE pour aller plus haut !"
                ],
                "triggered": False
            },
            {
                "x": 1300,
                "lines": [
                    "Félicitations !",
                    "Tu as terminé ce tutoriel !",
                    "Avance pour accéder au premier niveau !"
                ],
                "triggered": False
            }
        ]


