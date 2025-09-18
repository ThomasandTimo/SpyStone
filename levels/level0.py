import os
import arcade
from config import ASSETS_PATH
from levels.level_base import LevelBase

class Level0(LevelBase):
    def __init__(self):
        super().__init__("Niveau 0", background_image=os.path.join("assets/background_glacial_mountains_large.png"))
        self.level_end_x = 1500
    def setup(self):
        super().setup()
        
        # --- Sol ---
        sol = arcade.SpriteSolidColor(2300, 40, arcade.color.BLACK)
        sol.center_x = 800
        sol.center_y = 20
        self.platforms.append(sol)
        
          # --- Plateforme carrée (largeur: 200, hauteur: 200) ---
        sol = arcade.Sprite(os.path.join(ASSETS_PATH, "floor.png"))
        sol.scale_x = 200 / sol.texture.width
        sol.scale_y = 200 / sol.texture.height
        sol.center_x = 600
        sol.center_y = 20
        self.platforms.append(sol)
        
        # --- Mur vertical (largeur: 80, hauteur: 650) ---
        sol = arcade.SpriteSolidColor(80, 650, arcade.color.BLACK)
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
            "x": 0,  # Ignored for the tutorial
            "lines": [
                "Welcome, little stone!",
                "Use ← and → to move forward."
            ],
            "triggered": False
        },
        {
            "x": 350,
            "lines": [
                "Well done! You're moving forward!",
                "Press SPACE to jump."
            ],
            "triggered": False
        },
        {
            "x": 580,
            "lines": [
                "Excellent! Jump successful!"
            ],
            "triggered": False
        },
        {
            "x": 850,
            "lines": [
                "Oh no! A bigger obstacle!",
                "Hold SPACE to jump higher!"
            ],
            "triggered": False
        },
        {
            "x": 1300,
            "lines": [
                "Congratulations!",
                "You have completed this tutorial!",
                "Move forward to access the first level!"
            ],
            "triggered": False
        },
        {
            "x": 1450,
            "lines": [
                "Start of the real game!"
            ],
            "triggered": False,
            "on_trigger": (lambda: self.on_next_level() if hasattr(self, 'on_next_level') and self.on_next_level else None)
        }
    ]


