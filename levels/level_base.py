import arcade
import os 
from config import ASSETS_PATH

class LevelBase:
    def __init__(self, name, background_color=arcade.color.SKY_BLUE, background_image=None, background_zoom=1.0, dialogue_box_image=os.path.join(ASSETS_PATH, "ui", "box1.png"), dialogue_character_fullbody_image=None, dialogue_character_head_image=None):
        if dialogue_character_fullbody_image is None:
            dialogue_character_fullbody_image = os.path.join(ASSETS_PATH, "characters", "hero_fullbody.png")
        if dialogue_character_head_image is None:
            dialogue_character_head_image = os.path.join(ASSETS_PATH, "characters", "hero_head.png")
        self.name = name
        self.background_color = background_color
        self.background_image = background_image
        self.background_texture = None
        self.background_zoom = background_zoom  # facteur de zoom (1.0 = taille normale)
        self.platforms = None
        self.obstacles = None
        self.dialogue_triggers = []
        self.holes = []
        self.dialogue_box_image = dialogue_box_image
        self.dialogue_box_texture = None
        self.dialogue_character_fullbody_image = dialogue_character_fullbody_image
        self.dialogue_character_fullbody_texture = None
        self.dialogue_character_head_image = dialogue_character_head_image
        self.dialogue_character_head_texture = None

    def setup(self):
        """Crée les sprites et plateformes du niveau"""
        self.platforms = arcade.SpriteList()
        self.obstacles = arcade.SpriteList()
        self.holes = []
        # Charge la texture de background si besoin
        if self.background_image:
            self.background_texture = arcade.load_texture(self.background_image)
        # Charge la texture de la boîte de dialogue si besoin
        if self.dialogue_box_image:
            self.dialogue_box_texture = arcade.load_texture(self.dialogue_box_image)
        # Charge les textures de personnage si besoin
        if self.dialogue_character_fullbody_image:
            self.dialogue_character_fullbody_texture = arcade.load_texture(self.dialogue_character_fullbody_image)
        if self.dialogue_character_head_image:
            self.dialogue_character_head_texture = arcade.load_texture(self.dialogue_character_head_image)

    def update(self, delta_time):
        """Mettre à jour logique spécifique au niveau (si besoin)"""
        pass

    def draw_background(self):
        if self.background_texture:
            # Récupère la taille de la fenêtre
            left, right, bottom, top = arcade.get_viewport()
            width = right - left
            height = top - bottom
            tex_w = self.background_texture.width * self.background_zoom
            tex_h = self.background_texture.height * self.background_zoom
            # Commence à -tex_w pour éviter le vide à gauche
            x = -tex_w
            while x < width:
                arcade.draw_lrwh_rectangle_textured(x, 0, tex_w, tex_h, self.background_texture)
                x += tex_w
        else:
            arcade.set_background_color(self.background_color)
