import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pierre qui roule ronde"

class RollingStone(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Taille souhaitée pour la pierre
        self.stone_radius = 40
        stone_size = self.stone_radius * 2

        # Sprite avec image de pierre
        self.stone = arcade.Sprite("assets/stone.png")
        # Assure une forme parfaitement ronde
        self.stone.width = stone_size
        self.stone.height = stone_size

        self.stone.center_x = SCREEN_WIDTH // 2
        self.stone.center_y = SCREEN_HEIGHT // 2
        self.stone.change_x = 0
        self.stone.angle = 0

    def on_draw(self):
        arcade.start_render()
        self.stone.draw()

    def on_update(self, delta_time):
        # Déplacement horizontal
        self.stone.center_x += self.stone.change_x

        # Rotation inverse pour rouler dans l'autre sens
        self.stone.angle -= (self.stone.change_x / self.stone_radius) * (180 / 3.1416)

        # Bordures
        if self.stone.left < 0:
            self.stone.left = 0
            self.stone.change_x = 0
        elif self.stone.right > SCREEN_WIDTH:
            self.stone.right = SCREEN_WIDTH
            self.stone.change_x = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.stone.change_x = 5
        elif key == arcade.key.LEFT:
            self.stone.change_x = -5

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.RIGHT, arcade.key.LEFT]:
            self.stone.change_x = 0

def main():
    window = RollingStone()
    arcade.run()

if __name__ == "__main__":
    main()
