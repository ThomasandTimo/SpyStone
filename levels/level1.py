import arcade
from levels.level_base import LevelBase

class Level1(LevelBase):
    def __init__(self):
        super().__init__("Niveau 1", background_color=arcade.color.SKY_BLUE)

    def setup(self):
        super().setup()

        # Sol découpé pour laisser un trou au centre
        sol_gauche = arcade.SpriteSolidColor(450, 40, arcade.color.DARK_BROWN)
        sol_gauche.center_x = 225
        sol_gauche.center_y = 20
        self.platforms.append(sol_gauche)

        sol_droit = arcade.SpriteSolidColor(450, 40, arcade.color.DARK_BROWN)
        sol_droit.center_x = 775
        sol_droit.center_y = 20
        self.platforms.append(sol_droit)

        # Plateformes supplémentaires
        self.platforms.append(arcade.SpriteSolidColor(300, 30, arcade.color.BROWN))
        self.platforms[-1].center_x = 200
        self.platforms[-1].center_y = 120

        self.platforms.append(arcade.SpriteSolidColor(200, 30, arcade.color.BROWN))
        self.platforms[-1].center_x = 600
        self.platforms[-1].center_y = 220

        # Obstacles : 1 seul pour le niveau 1
        from models.obstacle import FallingObstacle
        obstacle = FallingObstacle(platforms=self.platforms)
        obstacle.center_x = 400
        obstacle.center_y = 300
        self.obstacles.append(obstacle)

        # Trous (exemple)
        from models.hole import Hole
        self.holes = [
            Hole(center_x=500, width=100),
        ]

        # Triggers de dialogue
        self.dialogue_triggers = [
            {"x": 250, "lines": ["Bienvenue sur le premier niveau !"], "triggered": False},
            {"x": 650, "lines": ["Attention, un obstacle approche !"], "triggered": False}
        ]
        
        self.qte_triggers = [
            {
                "x": 600,
                "key": arcade.key.E,
                "triggered": False,
                "on_success": lambda: print("QTE réussie !"),
                "on_fail": lambda: print("QTE échouée...")
            }
        ]

