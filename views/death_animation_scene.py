import arcade

class DeathAnimationScene(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene_frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_durations = []  # Individual duration for each frame
        self.is_playing = True
        self.fade_alpha = 0
        self.fade_in_complete = False
        self.in_loop_phase = False
        
    def on_show(self):
        # Reset viewport to ensure proper positioning
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        
        # Load all 21 death animation frames
        frame_files = []
        for i in range(1, 22):  # frames 1-21
            frame_files.append(f"death_{i:02d}.png")
        
        # Set individual durations for each frame (all 0.2 seconds for now)
        self.frame_durations = [
            0.2,  
            0.2,
            0.2, 
            0.2, 
            0.2, 
            0.2,  
            0.2, 
            0.2, 
            0.2,  
            0.2,  
            0.2, 
            0.2,  
            0.2,  
            0.5, 
            0.5,  
            0.5,  
            0.2,  
            0.6,  
            0.6,  
            0.6,  
            0.6 
        ]
        
        # Try to load all frames
        for frame_file in frame_files:
            try:
                texture = arcade.load_texture(f"assets/rock_death_sequence/{frame_file}")
                self.scene_frames.append(texture)
            except:
                print(f"Could not load {frame_file}")
                continue
        
        if not self.scene_frames:
            # Fallback if no images load
            arcade.set_background_color(arcade.color.DARK_RED)

    def on_draw(self):
        self.clear()
        
        # Draw current frame
        if self.scene_frames and self.current_frame < len(self.scene_frames):
            current_texture = self.scene_frames[self.current_frame]
            
            # Scale to fit screen while maintaining aspect ratio
            scale_x = self.window.width / current_texture.width
            scale_y = self.window.height / current_texture.height
            scale = min(scale_x, scale_y)
            
            arcade.draw_scaled_texture_rectangle(
                center_x=self.window.width // 2,
                center_y=self.window.height // 2,
                texture=current_texture,
                scale=scale
            )
        
        # Fade in effect
        if not self.fade_in_complete:
            fade_overlay = arcade.color.BLACK + (int(255 - self.fade_alpha),)
            arcade.draw_rectangle_filled(
                self.window.width // 2, self.window.height // 2,
                self.window.width, self.window.height,
                fade_overlay
            )

    def on_update(self, delta_time):
        # Fade in animation
        if not self.fade_in_complete:
            self.fade_alpha += 150 * delta_time
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.fade_in_complete = True
        
        # Frame animation with individual timing
        if self.is_playing and self.fade_in_complete:
            if self.current_frame < len(self.frame_durations):
                current_duration = self.frame_durations[self.current_frame]
                
                self.frame_timer += delta_time
                
                if self.frame_timer >= current_duration:
                    self.frame_timer = 0
                    self.current_frame += 1
                    
                    # Check if we've reached frame 19 (next to last - index 18)
                    if self.current_frame == 19:
                        self.in_loop_phase = True
                    
                    # If in loop phase, alternate between frames 19 and 20 (last two)
                    if self.in_loop_phase:
                        if self.current_frame >= 21:  # After frame 20 (index 20)
                            self.current_frame = 19  # Go back to frame 19 (index 18)
                    
                    # If not in loop phase and reached the end, start looping
                    elif self.current_frame >= len(self.scene_frames):
                        self.current_frame = 19  # Start the loop
                        self.in_loop_phase = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            from views.intro_view import IntroView
            menu_view = IntroView()
            self.window.show_view(menu_view)