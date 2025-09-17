import arcade

class Hole:
    """Un trou dans la plateforme"""
    def __init__(self, center_x, width):
        self.center_x = center_x
        self.width = width

    def check_fall(self, player):
        """Vérifie si le joueur tombe dans le trou"""
        left = self.center_x - self.width / 2
        right = self.center_x + self.width / 2
        debug = f"player_x={player.center_x}, player_y={player.center_y}, left={left}, right={right}"
        if left < player.center_x < right and player.center_y <= 40:
            print(f"[DEBUG] Chute détectée: {debug}")
            return True
        return False
