import random

class QTEManager:
    """Gestion des QTE"""
    def __init__(self):
        self.active = False

    def spawn_qte(self, player_x):
        if not self.active and random.random() < 0.002:
            self.active = True

    def success(self):
        self.active = False
        return True
