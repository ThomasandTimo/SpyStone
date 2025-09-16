import arcade
from managers.dialogue_manager import DialogueManager
from models.player import Player
from models.platform import Platform
from models.obstacle import FallingObstacle
from models.hole import Hole
from models.bonus import Bonus
from managers.qte_manager import QTEManager

class GameManager:
    """Gestion centrale du jeu"""
    def __init__(self):
        self.player = Player()
        self.platform_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.bonus_list = arcade.SpriteList()
        self.holes = []
        self.qte_manager = QTEManager()
        self.score = 0
        self.physics_engine = None
        self.is_game_over = False
        self.dialogue_manager = DialogueManager()
        self.dialogue_triggers = [
            {"x": 500, "lines": ["Le héros commence son ascension.", "Vous observez attentivement."], "triggered": False},
            {"x": 1200, "lines": ["Un oiseau vous bloque la route. Que fais-tu ?"],
             "choices": ["Lui parler gentiment", "Lancer un caillou", "Contourner discrètement"],
             "on_choice": self.oiseau_callback,
             "triggered": False}
        ]
        self.level = None

    def oiseau_callback(self, idx, value):
        # Exemple de callback pour le choix de l'oiseau
        if idx == 0:
            self.dialogue_manager.start_dialogue(["L'oiseau te répond poliment."])
        elif idx == 1:
            self.dialogue_manager.start_dialogue(["L'oiseau s'envole, vexé !"])
        elif idx == 2:
            self.dialogue_manager.start_dialogue(["Tu passes discrètement, l'oiseau ne te voit pas."])


    def setup(self, level=None):
        # Synchronise le niveau courant
        if level is not None:
            self.level = level

        # --- Trous (délégués au niveau si défini)
        if self.level and hasattr(self.level, "holes"):
            self.holes = self.level.holes
        else:
            self.holes = []

        # --- Moteur physique
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.platform_list, gravity_constant=0.5
        )
        self.player.center_x = 100
        self.player.center_y = 60

    def update(self):
        # --- Met à jour physique
        self.physics_engine.update()
        self.player.update()

        # Si dialogue actif, on stoppe obstacles, bonus, QTE
        if self.dialogue_manager.active:
            self.check_dialogue_triggers()
            return

        self.obstacle_list.update()
        self.bonus_list.update()

        # --- Collision bonus
        for bonus in self.bonus_list[:]:
            if arcade.check_for_collision(self.player, bonus):
                bonus.remove_from_sprite_lists()
                self.score += 1

        # --- Collision obstacles
        for o in self.obstacle_list:
            if arcade.check_for_collision(self.player, o):
                self.reset_player()

        # --- Trous
        for hole in self.holes:
            if hole.check_fall(self.player):
                self.reset_player()

        # --- QTE simple
        if self.level and hasattr(self.level, "qte_triggers"):
            for trigger in self.level.qte_triggers:
                if (self.player.center_x >= trigger["x"] and not trigger["triggered"]):
                    print(f"[DEBUG] QTE déclenché à x={trigger['x']}")
                    self.qte_manager.start_qte(
                        required_key=trigger["key"],
                        success_callback=trigger.get("on_success"),
                        fail_callback=trigger.get("on_fail")
                    )
                    trigger["triggered"] = True
        self.qte_manager.update()
        self.check_dialogue_triggers()


    def reset_player(self):
        self.player.center_x = 100
        self.player.center_y = 150
        self.is_game_over = False 

    def handle_qte(self):
        if self.qte_manager.active:
            print("QTE réussi !")
            self.qte_manager.success()

    def handle_key_press(self, key):
        if self.qte_manager.active:
            self.qte_manager.handle_key_press(key)
            
        if self.dialogue_manager.active:
            return
        if key == arcade.key.RIGHT:
            self.player.move_right()
        elif key == arcade.key.LEFT:
            self.player.move_left()
        elif key == arcade.key.UP:
            self.player.jump(self.physics_engine)
        elif key == arcade.key.E:
            self.handle_qte()

    def handle_key_release(self, key):
        # Bloque les contrôles de déplacement si un dialogue est actif
        if self.dialogue_manager.active:
            return
        if key in (arcade.key.RIGHT, arcade.key.LEFT):
            self.player.stop()
            
    def check_dialogue_triggers(self):
        # On ne déclenche pas de dialogue si le joueur saute
        for trigger in self.dialogue_triggers:
            if (
                self.player.center_x >= trigger["x"]
                and not self.dialogue_manager.active
                and not trigger["triggered"]
                and not self.player.is_jumping()
            ):
                self.player.stop()
                self.dialogue_manager.start_dialogue(
                    trigger["lines"],
                    choices=trigger.get("choices"),
                    on_choice=trigger.get("on_choice")
                )
                trigger["triggered"] = True

