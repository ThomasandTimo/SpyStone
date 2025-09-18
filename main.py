import arcade
from views.intro_view import IntroView

# --- Constantes globales ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Rolling Stone"


def main():
    """Point d'entrée du jeu."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    intro = IntroView()
    window.show_view(intro)
    arcade.run()


if __name__ == "__main__":
    main()