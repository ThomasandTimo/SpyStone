import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

class GameOverView(arcade.View):
    """Écran Game Over"""

    def __init__(self, score=0):
        super().__init__()

    def on_show(self):
        """Configure la fenêtre quand la view est affichée"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        # Fond noir
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                     SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.BLACK)

        # Texte principal
        arcade.draw_text(
            "GAME OVER",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
            arcade.color.RED, 64, anchor_x="center"
        )

        # Instruction pour retourner à l'intro ou rejouer
        arcade.draw_text(
            "Appuyez sur ESPACE pour recommencer",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80,
            arcade.color.LIGHT_GRAY, 24, anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            # Exemple : revenir à l'intro ou relancer le jeu
            from views.intro_view import IntroView  # adapte si ton fichier est différent
            self.window.show_view(IntroView())
