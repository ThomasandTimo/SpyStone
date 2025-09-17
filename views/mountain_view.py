import arcade
from managers.game_manager import GameManager

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCROLL_MARGIN = 200

class MountainView(arcade.View):
    def __init__(self):
        super().__init__()
        self.game_manager = GameManager()
        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def setup(self):
        self.game_manager.setup()

    def on_draw(self):
        arcade.start_render()
        self.camera_sprites.use()

        # Dessine tous les sprites
        self.game_manager.platform_list.draw()
        self.game_manager.player.draw()
        self.game_manager.obstacle_list.draw()
        self.game_manager.bonus_list.draw()

        # Trous
        for hole in self.game_manager.holes:
            arcade.draw_rectangle_filled(
                hole.center_x, 20, hole.width, 40, arcade.color.BLUE
            )

        # UI : Score
        arcade.draw_text(
            f"Score : {self.game_manager.score}",
            self.camera_sprites.position[0] + 20,
            SCREEN_HEIGHT - 40,
            arcade.color.BLACK, 16
        )

        # UI : QTE
        if self.game_manager.qte_manager.active:
            arcade.draw_text(
                "QTE! Appuyez sur E!",
                self.camera_sprites.position[0] + SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.RED, 24, anchor_x="center"
            )

        # --- Jauge de saut ---
        player = self.game_manager.player
        if player.jump_charging:
            gauge_width = 150
            gauge_height = 20
            power_ratio = player.jump_power / player.max_jump_power
            filled_width = gauge_width * power_ratio

            # Position de la jauge en bas à droite
            x = self.camera_sprites.position[0] + SCREEN_WIDTH - gauge_width - 20
            y = 20

            # Fond gris
            arcade.draw_rectangle_filled(
                x + gauge_width / 2, y + gauge_height / 2,
                gauge_width, gauge_height,
                arcade.color.GRAY
            )
            # Partie verte correspondant à la puissance
            arcade.draw_rectangle_filled(
                x + filled_width / 2, y + gauge_height / 2,
                filled_width, gauge_height,
                arcade.color.GREEN
            )
            # Contour noir
            arcade.draw_rectangle_outline(
                x + gauge_width / 2, y + gauge_height / 2,
                gauge_width, gauge_height,
                arcade.color.BLACK, 2
            )

    def back_to_intro(self, delta_time):
        arcade.unschedule(self.back_to_intro)
        from views.intro_view import IntroView
        self.window.show_view(IntroView())

    def on_update(self, delta_time):
        self.game_manager.update()
        self.scroll_to_player()

        # Mort si tombe sous l'écran
        if self.game_manager.player.center_y < 0 and not self.game_manager.is_game_over:
            self.game_manager.is_game_over = True
            # Schedule la fonction pour 1 seconde plus tard
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
        self.game_manager.handle_key_press(key)

    def on_key_release(self, key, modifiers):
        self.game_manager.handle_key_release(key)
