import arcade
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


    def setup(self):
        # --- Plateformes

        ground = Platform(2000, 40, arcade.color.GRAY, 1000, 20)
        self.platform_list.append(ground)
        self.platform_list.append(Platform(200, 20, arcade.color.BROWN, 400, 150))
        self.platform_list.append(Platform(150, 20, arcade.color.BROWN, 700, 250))
        self.platform_list.append(Platform(180, 20, arcade.color.BROWN, 1100, 300))
        self.platform_list.append(Platform(150, 20, arcade.color.BROWN, 1400, 400))
        

        # --- Trous
        self.holes = [Hole(500, 100), Hole(1300, 150)]

        # --- Obstacles tombants
        for _ in range(5):
            self.obstacle_list.append(FallingObstacle())

        # --- Bonus
        for _ in range(5):
            self.bonus_list.append(Bonus())

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
        self.qte_manager.spawn_qte(self.player.center_x)

    def reset_player(self):
        self.player.center_x = 100
        self.player.center_y = 150
        self.is_game_over = False 

    def handle_qte(self):
        if self.qte_manager.active:
            print("QTE réussi !")
            self.qte_manager.success()

    def handle_key_press(self, key):
        if key == arcade.key.RIGHT:
            self.player.move_right()
        elif key == arcade.key.LEFT:
            self.player.move_left()
        elif key == arcade.key.SPACE:  # touche pour charger le saut
            self.player.start_jump_charge()
        elif key == arcade.key.E:
            self.handle_qte()

    def handle_key_release(self, key):
        if key in (arcade.key.RIGHT, arcade.key.LEFT):
            self.player.stop()
        elif key == arcade.key.SPACE:  # relâche le saut
            self.player.release_jump()

