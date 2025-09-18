import arcade

class CrossroadsScene(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_texture = None
        self.explorer_texture = None
        self.stone_texture = None
        
        # Character positions
        self.explorer_x = -20  # Start off-screen left
        self.stone_x = -40     # Stone starts behind explorer
        self.explorer_y = 180   # Ground level
        self.stone_y = 160      # Ground level for stone
        
        # Target positions
        self.stone_stop_x = 60    # Stone stops early
        self.explorer_stop_x = 750  # Explorer stops at signs
        
        # Movement speeds
        self.explorer_speed = 100
        self.stone_speed = 50
        
        # Animation states
        self.stone_stopped = False
        self.explorer_stopped = False
        self.scene_complete = False
        self.fade_alpha = 0
        self.fade_in_complete = False
        self.transition_timer = 0
        
    def on_show(self):
        try:
            # Load the crossroads background with signs
            self.background_texture = arcade.load_texture("assets/emptyM.png")
            self.explorer_texture = arcade.load_texture("assets/explorer.png")
            self.stone_texture = arcade.load_texture("assets/stone.png")
        except:
            arcade.set_background_color(arcade.color.SKY_BLUE)

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
        
        # Draw moving explorer
        if self.explorer_texture:
            arcade.draw_texture_rectangle(
                center_x=self.explorer_x,
                center_y=self.explorer_y,
                width=self.explorer_texture.width,
                height=self.explorer_texture.height,
                texture=self.explorer_texture
            )
        
        # Draw moving stone
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
                "L'explorateur s'approche des panneaux...",
                self.window.width // 2, 50,
                arcade.color.WHITE, 14,
                anchor_x="center"
            )
        else:
            arcade.draw_text(
                "ESPACE - Commencer le défi",
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
            # Move stone until it reaches stop position
            if not self.stone_stopped:
                self.stone_x += self.stone_speed * delta_time
                if self.stone_x >= self.stone_stop_x:
                    self.stone_x = self.stone_stop_x
                    self.stone_stopped = True
            
            # Move explorer until it reaches signs
            if not self.explorer_stopped:
                self.explorer_x += self.explorer_speed * delta_time
                if self.explorer_x >= self.explorer_stop_x:
                    self.explorer_x = self.explorer_stop_x
                    self.explorer_stopped = True
            
            # When both have reached their positions, scene is complete
            if self.stone_stopped and self.explorer_stopped:
                self.transition_timer += delta_time
                if self.transition_timer >= 1.0:  # Wait 1 second after stopping
                    self.scene_complete = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.scene_complete:
                # Transition to obstacle course/platformer game
                self.start_obstacle_course()
            else:
                # Skip to end of scene
                self.stone_x = self.stone_stop_x
                self.explorer_x = self.explorer_stop_x
                self.stone_stopped = True
                self.explorer_stopped = True
                self.scene_complete = True

    def start_obstacle_course(self):
        # Transition to Level 1 (not Level 2)
        from .level_game_view import LevelGameView
        from levels.level1 import Level1
        
        level1_view = LevelGameView(Level1)
        level1_view.setup()
        self.window.show_view(level1_view)