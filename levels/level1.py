import os
import arcade
from levels.level_base import LevelBase

class Level1(LevelBase):
    def __init__(self):
        super().__init__("Niveau 1", background_image=os.path.join("assets/background_glacial_mountains_large.png"))
        self.level_end_x = 4000

    def setup(self):
        super().setup()
        
        # Liste de blocs à créer : (width, height, center_x, center_y, couleur)
        blocs = [
            # Sols
            (300, 1200, -300, 100, arcade.color.DARK_SLATE_GRAY),
            (800, 40, 400, 20, arcade.color.DARK_SLATE_GRAY),
            
            # Gros blocs
            (300, 450, 0, 200, arcade.color.DARK_SLATE_GRAY),
            (500, 450, 970, 200, arcade.color.DARK_SLATE_GRAY),
            
            # Plateformes bleues
            (120, 50, 230, 100, arcade.color.ICEBERG),
            (120, 50, 350, 280, arcade.color.ICEBERG),
            (120, 50, 490, 130, arcade.color.ICEBERG),
            (120, 50, 610, 350, arcade.color.ICEBERG),
            
            # Gros blocs droits
            (400, 200, 1300, 100, arcade.color.DARK_SLATE_GRAY),
            (250, 80, 1600, 0, arcade.color.DARK_SLATE_GRAY),
            
            # Sols
            (2500, 80, 3080, 0, arcade.color.DARK_SLATE_GRAY),
            
             # Plafond au-dessus du bloc précédent
            (1200, 400, 2000, 600, arcade.color.DARK_SLATE_GRAY),
            
             # Plafond au-dessus du bloc précédent
            (1200, 400, 2000, 600, arcade.color.DARK_SLATE_GRAY),
            
            # Gros blocs droits
            (60, 620, 2850, 220, arcade.color.DARK_SLATE_GRAY),
            
            # Plateformes bleues
            (120, 60, 2760, 100, arcade.color.ICEBERG),
            
            # Plateformes bleues
            (120, 60, 2660, 430, arcade.color.ICEBERG),
            
        ]
        
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
        
         # Triggers de dialogue
        self.dialogue_triggers = [
            {"x": 0, "lines": ["Bienvenue sur le premier niveau !"], "triggered": False},
            {"x": 200, "lines": ["Trouves un moyen de rejoindre l'autre côté !"], "triggered": False},
            {"x": 3600, "lines": ["Deux directions s'offrent à vous...", "Laquelle cache la vérité ?"],
             "choices": ["Chemin 1 (Yéti)", "Chemin 2 (Sûr)"],
             "on_choice": self.path_choice_callback,
             "triggered": False},
        ]

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

    


