import arcade
import os
import random
import time
from config import ASSETS_PATH

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class YetiView(arcade.View):
    def __init__(self, mountain_view=None):
        super().__init__()
        self.yeti_texture = arcade.load_texture(os.path.join(ASSETS_PATH, "yeti.png"))
        self.state = "intro"  # intro -> scream -> result
        self.scream_time = None
        self.result = None
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.mountain_view = mountain_view  # Pour reprendre la progression après

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        # Affiche le fond yeti centré sans déformation
        img_w, img_h = self.yeti_texture.width, self.yeti_texture.height
        x = (SCREEN_WIDTH - img_w) // 2
        y = (SCREEN_HEIGHT - img_h) // 2
        arcade.draw_lrwh_rectangle_textured(x, y, img_w, img_h, self.yeti_texture)

        # Dialogue stylé façon MountainView
        dialogue_box_width = SCREEN_WIDTH-200
        dialogue_box_height = 140
        dialogue_box_x = SCREEN_WIDTH//2
        dialogue_box_y = 100
        arcade.draw_rectangle_filled(
            dialogue_box_x, dialogue_box_y,
            dialogue_box_width, dialogue_box_height, (245,245,245,230)
        )

        text_x = 250
        text_y = dialogue_box_y + dialogue_box_height//2 - 40
        if self.state == "intro":
            arcade.draw_text(
                "The Hero: Aaaah! The Yeti!",
                text_x, text_y,
                arcade.color.DARK_BLUE, 22
            )
            arcade.draw_text(
                "Appuie sur ENTRÉE pour crier !",
                SCREEN_WIDTH//2, 60,
                arcade.color.DARK_SLATE_GRAY, 16, anchor_x="center"
            )
        elif self.state == "scream":
            arcade.draw_text(
                "The Hero: AAAAAAAAAAAAAAAAH!",
                text_x, text_y,
                arcade.color.RED, 26
            )
        elif self.state == "result":
            if self.result == "dead":
                arcade.draw_text(
                    "The Yeti devours the Hero...",
                    text_x, text_y,
                    arcade.color.DARK_RED, 22
                )
                arcade.draw_text(
                    "GAME OVER",
                    SCREEN_WIDTH//2, 60,
                    arcade.color.RED, 24, anchor_x="center"
                )
            elif self.result == "alive":
                arcade.draw_text(
                    "Pfiou... The Hero escapes!",
                    text_x, text_y,
                    arcade.color.DARK_GREEN, 22
                )
                arcade.draw_text(
                    "Appuie sur ENTRÉE pour continuer",
                    SCREEN_WIDTH//2, 60,
                    arcade.color.DARK_SLATE_GRAY, 16, anchor_x="center"
                )

    def on_key_press(self, key, modifiers):
        if self.state == "intro" and key in (arcade.key.ENTER, arcade.key.RETURN):
            self.state = "scream"
            self.scream_time = time.time()
            self.window.dispatch_event("on_draw")
        elif self.state == "result" and self.result == "alive" and key in (arcade.key.ENTER, arcade.key.RETURN):
            # Reprend la progression dans MountainView si fourni
            if self.mountain_view:
                self.window.show_view(self.mountain_view)
                # Appelle resume_after_yeti APRÈS le show_view, dans on_show_view de MountainView
                if hasattr(self.mountain_view, "pending_resume_after_yeti"):
                    self.mountain_view.pending_resume_after_yeti = True
                else:
                    self.mountain_view.resume_after_yeti()
            else:
                from views.mountain_view import MountainView
                mv = MountainView()
                self.window.show_view(mv)

    def on_update(self, delta_time):
        if self.state == "scream" and self.scream_time is not None:
            if time.time() - self.scream_time > 1.5:
                # Random: 50% chance de mourir ou survivre
                self.result = "dead" if random.random() < 0.5 else "alive"
                self.state = "result"
                if self.result == "dead":
                    # Game over après 2s
                    arcade.schedule(self._go_to_game_over, 2.0)

    def _go_to_game_over(self, delta_time):
        arcade.unschedule(self._go_to_game_over)
        from views.explorer_death_scene import ExplorerDeathScene
        self.window.show_view(ExplorerDeathScene())


