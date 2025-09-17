import arcade

class Trap:
    """Un piège rectangulaire qui bloque le joueur."""

    def __init__(self, x, y, width, height, player: arcade.Sprite):
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
        self.player = player
        self.active = True  # pour pouvoir activer/désactiver le piège

    def draw(self):
        """Dessine le piège sous forme de rectangle rouge."""
        if self.active:
            arcade.draw_rectangle_filled(
                self.center_x, self.center_y,
                self.width, self.height,
                arcade.color.RED
            )

    def update(self):
        """Vérifie si le joueur est dans le piège et le bloque."""
        if not self.active:
            return

        # Collision simple AABB
        px, py = self.player.center_x, self.player.center_y
        hw, hh = self.width / 2, self.height / 2

        if (self.center_x - hw <= px <= self.center_x + hw and
            self.center_y - hh <= py <= self.center_y + hh):
            # Bloquer le joueur : annule ses mouvements
            self.player.change_x = 0
            self.player.change_y = 0

