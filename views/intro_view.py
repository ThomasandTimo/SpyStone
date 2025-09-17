import arcade
from .mountain_view import MountainView


class IntroView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Un héros grimpe l'Everest...\n\n"
            "Mais vous n'êtes qu'un simple caillou.",
            self.window.width / 2, self.window.height / 2,
            arcade.color.WHITE, 24,
            anchor_x="center", anchor_y="center"
        )
        arcade.draw_text(
            "Appuyez sur ESPACE pour commencer",
            self.window.width / 2, 100,
            arcade.color.LIGHT_GRAY, 16,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            mountain_view = MountainView()
            mountain_view.setup()
            self.window.show_view(mountain_view)
