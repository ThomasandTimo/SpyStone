import arcade

class SlopeScene(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_texture = None
        self.explorer_texture = None
        self.stone_texture = None
        
        # Character positions - both start from bottom-left (0,0)
        self.explorer_x = 0     # Start from position (0,0)
        self.stone_x = 0        # Stone also starts from (0,0)
        self.explorer_y = 0     # Start from bottom
        self.stone_y = 0        # Start from bottom
        
        # Target positions
        self.stone_stop_x = 120    # Stone stops very early on slope
        self.stone_stop_y = 30     # Stone climbs just a little bit
        self.explorer_stop_x = 600  # Explorer continues much further
        self.explorer_stop_y = 200  # Explorer reaches higher but less steep (reduced from 300)
        
        # Movement speeds
        self.explorer_speed = 100
        self.stone_speed = 40
        
        # Animation states
        self.stone_stopped = False
        self.explorer_stopped = False
        self.scene_complete = False
        self.fade_alpha = 0
        self.fade_in_complete = False
        self.transition_timer = 0
        
    def on_show(self):
        # Reset viewport to ensure proper positioning
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        
        try:
            # Load the slope background
            self.background_texture = arcade.load_texture("assets/pente_scene.png")
            self.explorer_texture = arcade.load_texture("assets/explorer.png")
            self.stone_texture = arcade.load_texture("assets/stone.png")
        except:
            arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        self.clear()
        
        # Draw static background with slope
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
        
        # Draw stone (stays at bottom)
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
        
        # Show instructions based on scene state
        if not self.scene_complete:
            arcade.draw_text(
                "L'explorateur gravit la pente...",
                self.window.width // 2, 50,
                arcade.color.WHITE, 14,
                anchor_x="center"
            )
        else:
            arcade.draw_text(
                "ESPACE - Commencer le niveau 2",
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
        
        if self.fade_in_complete and not self.scene_complete:
            # Move stone until it reaches stop position (follows same slope path but stops early)
            if not self.stone_stopped:
                self.stone_x += self.stone_speed * delta_time
                # Stone follows same slope angle as explorer
                progress = self.stone_x / self.stone_stop_x
                self.stone_y = progress * self.stone_stop_y
                
                if self.stone_x >= self.stone_stop_x:
                    self.stone_x = self.stone_stop_x
                    self.stone_y = self.stone_stop_y
                    self.stone_stopped = True
            
            # Move explorer up the slope (both x and y movement)
            if not self.explorer_stopped:
                self.explorer_x += self.explorer_speed * delta_time
                # Calculate slope climb (y increases as x increases from 0,0)
                progress = self.explorer_x / self.explorer_stop_x
                self.explorer_y = progress * self.explorer_stop_y
                
                if self.explorer_x >= self.explorer_stop_x:
                    self.explorer_x = self.explorer_stop_x
                    self.explorer_y = self.explorer_stop_y
                    self.explorer_stopped = True
            
            # When both have reached their positions, scene is complete
            if self.stone_stopped and self.explorer_stopped:
                self.transition_timer += delta_time
                if self.transition_timer >= 1.0:  # Wait 1 second after stopping
                    self.scene_complete = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.scene_complete:
                # Transition to Level 2
                self.start_level_2()
            else:
                # Skip to end of scene
                self.stone_x = self.stone_stop_x
                self.stone_y = self.stone_stop_y
                self.explorer_x = self.explorer_stop_x
                self.explorer_y = self.explorer_stop_y
                self.stone_stopped = True
                self.explorer_stopped = True
                self.scene_complete = True

    def start_level_2(self):
        # Start Level 2
        from .level_game_view import LevelGameView
        from levels.level2 import Level2
        
        level2_view = LevelGameView(Level2)
        level2_view.setup()
        self.window.show_view(level2_view)