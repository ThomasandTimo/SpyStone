import arcade
import os 
from config import ASSETS_PATH

class LevelBase:
    def __init__(self, name, background_color=arcade.color.SKY_BLUE, background_image="assets/background_glacial_mountains.png", background_zoom=1.0, dialogue_box_image=os.path.join(ASSETS_PATH, "ui", "box1.png"), dialogue_character_fullbody_image=None, dialogue_character_head_image=None):
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
        """Dessine le fond en texture couvrant tout l’écran"""
        if self.background_texture:
            # Obtenir les dimensions de la vue
            left, right, bottom, top = arcade.get_viewport()
            width = right - left
            height = top - bottom

            # Calcul de l’échelle pour remplir l’écran proportionnellement
            scale_x = width / self.background_texture.width
            scale_y = height / self.background_texture.height
            scale = max(scale_x, scale_y) * self.background_zoom  # Remplit sans bande noire

            # Centre de l’écran
            center_x = left + width / 2
            center_y = bottom + height / 2

            arcade.draw_scaled_texture_rectangle(
                center_x=center_x,
                center_y=center_y,
                texture=self.background_texture,
                scale=scale
            )
        else:
            arcade.set_background_color(self.background_color)
