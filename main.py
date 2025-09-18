import arcade
from views.intro_view import IntroView

# --- Constantes globales ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Le Caillou Spectateur"


def main():
    """Point d'entrée du jeu."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # ✅ Charger et jouer la musique une seule fois
    soundtrack = arcade.load_sound("assets/audio/stone_game_soundtrack.mp3")
    soundtrack_player = arcade.play_sound(soundtrack, volume=0.5, looping=True)
    window.soundtrack = soundtrack
    window.soundtrack_player = soundtrack_player

    intro = IntroView()
    window.show_view(intro)
    arcade.run()


if __name__ == "__main__":
    main()