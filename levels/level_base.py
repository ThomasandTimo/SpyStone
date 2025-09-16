import arcade

class LevelBase:
    def __init__(self, name, background_color=arcade.color.SKY_BLUE):
        self.name = name
        self.background_color = background_color
        self.platforms = None
        self.obstacles = None
        self.dialogue_triggers = []
        self.holes = []

    def setup(self):
        """Crée les sprites et plateformes du niveau"""
        self.platforms = arcade.SpriteList()
        self.obstacles = arcade.SpriteList()
        self.holes = []

    def update(self, delta_time):
        """Mettre à jour logique spécifique au niveau (si besoin)"""
        pass

    def draw_background(self):
        arcade.set_background_color(self.background_color)
