import os
import arcade
from levels.level_base import LevelBase
from config import ASSETS_PATH

class Level1(LevelBase):
    def __init__(self):
        super().__init__("Niveau 1", background_image=os.path.join("assets/background_glacial_mountains_large.png"))
        self.level_end_x = 4000

    def setup(self):
        super().setup()
        
        # Liste de blocs à créer : (width, height, center_x, center_y, couleur)
        blocs = [
            # Sols
            (300, 1200, -300, 100, arcade.color.BLACK),
            (800, 40, 400, 20, arcade.color.BLACK),
            
            # Gros blocs
            (300, 450, 0, 200, arcade.color.BLACK),
            (500, 450, 970, 200, arcade.color.BLACK),
            
            # Gros blocs droits
            (400, 200, 1300, 100, arcade.color.BLACK),
            (250, 80, 1600, 0, arcade.color.BLACK),
            
            # Sols
            (2500, 80, 3080, 0, arcade.color.BLACK),
            
             # Plafond au-dessus du bloc précédent
            (1200, 400, 2000, 600, arcade.color.BLACK),
            
            # Plafond au-dessus du bloc précédent
            (1200, 400, 2000, 600, arcade.color.BLACK),
            
            # Gros blocs droits
            (60, 620, 2850, 220, arcade.color.BLACK)
        ]
        
        # Création des sprites pour les blocs normaux
        for width, height, x, y, color in blocs:
            bloc_droit = arcade.SpriteSolidColor(width, height, color)
            bloc_droit.center_x = x
            bloc_droit.center_y = y
            self.platforms.append(bloc_droit)
        
        # --- Plateformes bleues en sprites ---
        # Plateforme 1 (120x50)
        platform1 = arcade.Sprite(os.path.join(ASSETS_PATH, "platform.png"))
        platform1.scale_x = 120 / platform1.texture.width
        platform1.scale_y = 50 / platform1.texture.height
        platform1.center_x = 230
        platform1.center_y = 100
        self.platforms.append(platform1)
        
        # Plateforme 2 (120x50)
        platform2 = arcade.Sprite(os.path.join(ASSETS_PATH, "platform.png"))
        platform2.scale_x = 120 / platform2.texture.width
        platform2.scale_y = 50 / platform2.texture.height
        platform2.center_x = 350
        platform2.center_y = 280
        self.platforms.append(platform2)
        
        # Plateforme 3 (120x50)
        platform3 = arcade.Sprite(os.path.join(ASSETS_PATH, "platform.png"))
        platform3.scale_x = 120 / platform3.texture.width
        platform3.scale_y = 50 / platform3.texture.height
        platform3.center_x = 490
        platform3.center_y = 130
        self.platforms.append(platform3)
        
        # Plateforme 4 (120x50)
        platform4 = arcade.Sprite(os.path.join(ASSETS_PATH, "platform.png"))
        platform4.scale_x = 120 / platform4.texture.width
        platform4.scale_y = 50 / platform4.texture.height
        platform4.center_x = 610
        platform4.center_y = 350
        self.platforms.append(platform4)
        
        # Plateforme 5 (120x60)
        platform5 = arcade.Sprite(os.path.join(ASSETS_PATH, "platform.png"))
        platform5.scale_x = 120 / platform5.texture.width
        platform5.scale_y = 60 / platform5.texture.height
        platform5.center_x = 2760
        platform5.center_y = 100
        self.platforms.append(platform5)
        
        # Plateforme 6 (120x60)
        platform6 = arcade.Sprite(os.path.join(ASSETS_PATH, "platform.png"))
        platform6.scale_x = 120 / platform6.texture.width
        platform6.scale_y = 60 / platform6.texture.height
        platform6.center_x = 2660
        platform6.center_y = 430
        self.platforms.append(platform6)

        # Création des sprites pour les blocs
        for width, height, x, y, color in blocs:
            if color == arcade.color.RED:
                sprite = arcade.Sprite(os.path.join(ASSETS_PATH, "characters/hero_fullbody.png"))
                sprite.scale_x = width / sprite.texture.width
                sprite.scale_y = height / sprite.texture.height
            elif color == arcade.color.GREEN:
                sprite = arcade.Sprite(os.path.join(ASSETS_PATH, "characters/hero_fullbody.png"))
                sprite.scale_x = width / sprite.texture.width
                sprite.scale_y = height / sprite.texture.height
            elif color == arcade.color.BLUE:
                sprite = arcade.Sprite(os.path.join(ASSETS_PATH, "characters/hero_fullbody.png"))
                sprite.scale_x = width / sprite.texture.width
                sprite.scale_y = height / sprite.texture.height
            else:
                sprite = arcade.SpriteSolidColor(width, height, color)

            # Positionnement exact
            sprite.center_x = x
            sprite.center_y = y
            self.platforms.append(sprite)
        
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

        # Création des sprites
        for width, height, x, y, color in blocs:
            bloc_droit = arcade.SpriteSolidColor(width, height, color)
            bloc_droit.center_x = x
            bloc_droit.center_y = y
            self.platforms.append(bloc_droit)
        
        # Triggers de dialogue et de transition
        self.dialogue_triggers = [
            {
                "x": 0,
                "lines": ["This path wasn’t easy!"],
                "triggered": False
            },
           {
                "x": 120,
                "lines": ["These platforms were very helpful,", "allowing me to continue on my path."],
                "triggered": False
            },
            {"x": 3300, "lines": [], "triggered": False, "on_trigger": self.crossroads_transition},
            {
                "x": 3600,
                "lines": ["Two paths lie ahead...", "Which one holds the truth?"],
                "choices": ["Path 1 (Yeti)", "Path 2 (Safe)"],
                "on_choice": self.path_choice_callback,
                "triggered": False
            },
            {"x": 3700, "lines": [], "triggered": False, "on_trigger": self.slope_transition},
        ]   


    def slope_transition(self):
        self.pending_transition = 'slope'

    def crossroads_transition(self):
        # Indique à MountainView de lancer la crossroads scene
        self.pending_transition = 'crossroads'

    def path_choice_callback(self, idx, value):
        """Callback pour le choix de chemin"""
        import random
        hero_choice = random.randint(0, 1)
        
        player_line = ""
        if idx == hero_choice:
            player_line = "This way feels right. Let's go."
        else:
            player_line = "I trust my own judgment. I'll take the other path."

        if hero_choice == 1:
            lines = [player_line, "The Hero nods and heads down the safe path."]
            self.pending_transition = 'safe'
        else:
            lines = [player_line, "The Hero grins mischievously and runs toward the Yeti's lair!"]
            self.pending_transition = 'yeti'

        # Démarre le dialogue combiné; la transition sera déclenchée par MountainView quand le dialogue se termine
        if hasattr(self, 'dialogue_manager'):
            self.dialogue_manager.start_dialogue(lines)