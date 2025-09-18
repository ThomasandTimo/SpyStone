import arcade
from .mountain_view import MountainView

class IntroSceneView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_texture = None
        self.explorer_texture = None
        self.stone_texture = None
        
        # Positions for moving characters
        self.explorer_x = -100  # Start off-screen left
        self.stone_x = -150     # Stone follows behind
        self.explorer_y = 100   # Ground level
        self.stone_y = 80       # Slightly lower than explorer
        
        # Movement speeds
        self.explorer_speed = 40  # pixels per second
        self.stone_speed = 35     # Slightly slower, creating follow effect
        
        self.fade_alpha = 0
        self.fade_in_complete = False
        
    def on_show(self):
        try:
            # Load separate images
            self.background_texture = arcade.load_texture("assets/explorer_stone_scene.jpg")
            self.explorer_texture = arcade.load_texture("assets/explorer.png")
            self.stone_texture = arcade.load_texture("assets/stone.png")
        except:
            arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        self.clear()
        
        # Draw static background
        if self.background_texture:
            arcade.draw_scaled_texture_rectangle(
                center_x=self.window.width // 2,
                center_y=self.window.height // 2,
                texture=self.background_texture,
                scale=max(self.window.width / self.background_texture.width,
                         self.window.height / self.background_texture.height)
            )
        
        # Draw moving explorer
        if self.explorer_texture:
            arcade.draw_texture_rectangle(
                center_x=self.explorer_x,
                center_y=self.explorer_y,
                width=self.explorer_texture.width,
                height=self.explorer_texture.height,
                texture=self.explorer_texture
            )
        
        # Draw moving stone (following behind)
        if self.stone_texture:
            arcade.draw_texture_rectangle(
                center_x=self.stone_x,
                center_y=self.stone_y,
                width=self.stone_texture.width,
                height=self.stone_texture.height,
                texture=self.stone_texture
            )
        
        # Fade in effect
        if not self.fade_in_complete:
            fade_overlay = arcade.color.BLACK + (int(255 - self.fade_alpha),)
            arcade.draw_rectangle_filled(
                self.window.width // 2, self.window.height // 2,
                self.window.width, self.window.height,
                fade_overlay
            )
        
        # Instruction
        arcade.draw_text(
            "SPACE - Back to menu",
            self.window.width // 2, 50,
            arcade.color.WHITE, 16,
            anchor_x="center"
        )

    def on_update(self, delta_time):
        # Fade in animation
        if not self.fade_in_complete:
            self.fade_alpha += 150 * delta_time
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.fade_in_complete = True
        
        # Move characters across screen
        if self.fade_in_complete:
            self.explorer_x += self.explorer_speed * delta_time
            self.stone_x += self.stone_speed * delta_time
            
            # Reset positions when they go off-screen (loop)
            if self.explorer_x > self.window.width + 100:
                self.explorer_x = -100
            if self.stone_x > self.window.width + 100:
                self.stone_x = -150

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            # Return to main menu
            mountain_view = MountainView()
            mountain_view.setup()
            self.window.show_view(mountain_view)