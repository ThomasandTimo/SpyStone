
import arcade
from managers.game_manager import GameManager
from levels.level1 import Level1
from levels.level2 import Level2

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCROLL_MARGIN = 200

class MountainView(arcade.View):
    def __init__(self):
        super().__init__()
        self.levels = [Level1(), Level2()]
        self.current_level_index = 0
        self.level = self.levels[self.current_level_index]
        self.level.setup()
        self.game_manager = GameManager()
        self._connect_level_to_manager()
        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def _connect_level_to_manager(self):
        self.game_manager.platform_list = self.level.platforms
        self.game_manager.obstacle_list = self.level.obstacles
        self.game_manager.dialogue_triggers = self.level.dialogue_triggers
        # Synchronise les trous du niveau courant
        if hasattr(self.level, "holes"):
            self.game_manager.holes = self.level.holes
        else:
            self.game_manager.holes = []

    def setup(self):
        self.game_manager.setup(self.level)

    def on_draw(self):
        arcade.start_render()
        self.camera_sprites.use()
        # Fond du niveau
        self.level.draw_background()

        self.game_manager.platform_list.draw()
        self.game_manager.player.draw()
        self.game_manager.obstacle_list.draw()
        self.game_manager.bonus_list.draw()

        # Trous
        for hole in self.game_manager.holes:
            arcade.draw_rectangle_filled(
                hole.center_x, 20, hole.width, 40, arcade.color.BLACK
            )

        # Dialogue (texte et choix)
        dm = self.game_manager.dialogue_manager
        if dm.active:
            line = dm.get_current_line()
            arcade.draw_rectangle_filled(
                self.camera_sprites.position[0]+SCREEN_WIDTH//2, 100,
                SCREEN_WIDTH-100, 100 + 30*len(dm.choices), (0,0,0,180)
            )
            arcade.draw_text(
                line,
                self.camera_sprites.position[0]+60, 160 + 30*len(dm.choices),
                arcade.color.WHITE, 16, width=SCREEN_WIDTH-120
            )
            # Affichage des choix si présents
            if dm.choices:
                for idx, choice in enumerate(dm.choices):
                    arcade.draw_text(
                        f"{idx+1}. {choice}",
                        self.camera_sprites.position[0]+80,
                        120 + 30*(len(dm.choices)-idx-1),
                        arcade.color.LIGHT_GREEN if dm.choice_selected==idx else arcade.color.LIGHT_GRAY,
                        16
                    )
                arcade.draw_text(
                    "Appuyez sur 1, 2, 3... pour choisir",
                    self.camera_sprites.position[0]+SCREEN_WIDTH//2, 80,
                    arcade.color.LIGHT_GRAY, 14, anchor_x="center"
                )
            else:
                arcade.draw_text(
                    "ESPACE ou flèche bas pour continuer",
                    self.camera_sprites.position[0]+SCREEN_WIDTH//2, 80,
                    arcade.color.LIGHT_GRAY, 14, anchor_x="center"
                )

        # UI
        arcade.draw_text(f"Score : {self.game_manager.score}",
                         self.camera_sprites.position[0]+20, SCREEN_HEIGHT-40,
                         arcade.color.BLACK, 16)
        if self.game_manager.qte_manager.active:
            arcade.draw_text("QTE! Appuyez sur E!",
                             self.camera_sprites.position[0]+SCREEN_WIDTH/2,
                             SCREEN_HEIGHT/2,
                             arcade.color.RED, 24, anchor_x="center")
            
    def back_to_intro(self, delta_time):
        arcade.unschedule(self.back_to_intro)
        from views.intro_view import IntroView
        self.window.show_view(IntroView())

    def on_update(self, delta_time):
        self.game_manager.update()
        self.scroll_to_player()

        # Transition automatique : si le joueur atteint la fin du niveau courant
        # (exemple : position x > 950)
        if self.game_manager.player.center_x > 950:
            if self.current_level_index + 1 < len(self.levels):
                self.current_level_index += 1
                self.level = self.levels[self.current_level_index]
                self.level.setup()
                self._connect_level_to_manager()
                self.game_manager.setup(self.level)  # Reset le joueur et la physique
                # Optionnel : replacer la caméra au début
                self.camera_sprites.move_to((0, 0))
            else:
                # Dernier niveau atteint, retour à l'intro ou écran de fin
                arcade.schedule(self.back_to_intro, 0.5)

        # Mort si tombe sous l'écran
        if self.game_manager.player.center_y < 0 and not self.game_manager.is_game_over:
            self.game_manager.is_game_over = True
            arcade.schedule(self.back_to_intro, 1.0)

    def scroll_to_player(self):
        left_boundary = self.camera_sprites.position[0] + SCROLL_MARGIN
        right_boundary = self.camera_sprites.position[0] + SCREEN_WIDTH - SCROLL_MARGIN

        player_x = self.game_manager.player.center_x

        if player_x < left_boundary:
            self.camera_sprites.move_to((player_x - SCROLL_MARGIN, 0), 0.2)
        elif player_x > right_boundary:
            self.camera_sprites.move_to((player_x - SCREEN_WIDTH + SCROLL_MARGIN, 0), 0.2)

    def on_key_press(self, key, modifiers):
        dm = self.game_manager.dialogue_manager
        if dm.active:
            # Sélection choix si présents
            if dm.choices:
                if arcade.key.KEY_1 <= key <= arcade.key.KEY_9:
                    idx = key - arcade.key.KEY_1
                    if 0 <= idx < len(dm.choices):
                        dm.select_choice(idx)

            else:
                if key in (arcade.key.SPACE, arcade.key.DOWN):
                    dm.next_line()
        else:
            # Contrôles classiques du joueur
            self.game_manager.handle_key_press(key)

    def on_key_release(self, key, modifiers):
        self.game_manager.handle_key_release(key)
