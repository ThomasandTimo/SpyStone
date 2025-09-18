import arcade

class CrossroadsCompletionScene(arcade.View):
    def __init__(self, mountain_view=None):
        super().__init__()
        self.background_texture = None
        self.explorer_texture = None
        self.stone_texture = None
        self.mountain_view = mountain_view
        # Final positions - both characters at the signs
        self.explorer_x = 750   # Explorer at signs
        self.stone_x = 720      # Stone next to explorer
        self.explorer_y = 180   # Ground level
        self.stone_y = 160      # Ground level for stone
        # Animation
        self.fade_alpha = 0
        self.fade_in_complete = False
        
    def on_show(self):
        try:
            # Same background as crossroads scene
            self.background_texture = arcade.load_texture("assets/emptyM.png")
            self.explorer_texture = arcade.load_texture("assets/explorer.png")
            self.stone_texture = arcade.load_texture("assets/stone.png")
        except:
            arcade.set_background_color(arcade.color.SKY_BLUE)
        
        # Reset any camera/viewport positioning that might carry over from game
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        
        # Draw static background with mountain and signs
        if self.background_texture:
            arcade.draw_scaled_texture_rectangle(
                center_x=self.window.width // 2,
                center_y=self.window.height // 2,
                texture=self.background_texture,
                scale=max(self.window.width / self.background_texture.width,
                         self.window.height / self.background_texture.height)
            )
        
        # Draw explorer (still at signs)
        if self.explorer_texture:
            arcade.draw_texture_rectangle(
                center_x=self.explorer_x,
                center_y=self.explorer_y,
                width=self.explorer_texture.width,
                height=self.explorer_texture.height,
                texture=self.explorer_texture
            )
        
        # Draw stone (now next to explorer)
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
        
        arcade.draw_text(
              "ENTER - Continue the adventure",
            self.window.width // 2, 80,
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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            # Retourne à MountainView juste avant le choix
            if self.mountain_view:
                self.window.show_view(self.mountain_view)
                self.mountain_view.resume_after_crossroads()
            else:
                from .mountain_view import MountainView
                mountain_view = MountainView()
                mountain_view.setup()
                self.window.show_view(mountain_view)