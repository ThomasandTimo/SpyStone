import arcade

class FinalCinematicScene(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene_frames = []
        self.current_frame = 0
        self.frame_durations = []
        self.frame_timer = 0
        self.is_playing = True
        self.fade_alpha = 0
        self.fade_in_complete = False
        self.transition_alpha = 0
        self.loop_count = 0
        self.max_loops = 5
        
    def on_show(self):
        # Load all the final sequence frames (77 total frames)
        frame_files = []
        for i in range(1, 78):  # frames 1-77
            frame_files.append(f"final_{i:02d}.png")
        
        # Set durations - 0.1 second for each frame as requested
        self.frame_durations = [0.1] * 77  # All frames get 0.1 second timing
        
        # Try to load all frames
        for frame_file in frame_files:
            try:
                texture = arcade.load_texture(f"assets/final_sequence/{frame_file}")
                self.scene_frames.append(texture)
            except:
                print(f"Could not load {frame_file}")
                continue
        
        if not self.scene_frames:
            # Fallback if no images load
            arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        self.clear()
        
        # Always draw current frame (prevents blank moments)
        if self.scene_frames and self.current_frame < len(self.scene_frames):
            current_texture = self.scene_frames[self.current_frame]
            
            # Scale to fit screen while maintaining aspect ratio
            scale_x = self.window.width / current_texture.width
            scale_y = self.window.height / current_texture.height
            scale = min(scale_x, scale_y)
            
            # Draw current frame at full opacity
            arcade.draw_scaled_texture_rectangle(
                center_x=self.window.width // 2,
                center_y=self.window.height // 2,
                texture=current_texture,
                scale=scale
            )
            
            # Draw next frame on top during transition
            if (self.current_frame + 1 < len(self.scene_frames) and 
                self.transition_alpha > 0):
                next_texture = self.scene_frames[self.current_frame + 1]
                arcade.draw_scaled_texture_rectangle(
                    center_x=self.window.width // 2,
                    center_y=self.window.height // 2,
                    texture=next_texture,
                    scale=scale,
                    alpha=self.transition_alpha
                )
        
        # Fade in effect
        if not self.fade_in_complete:
            fade_overlay = arcade.color.BLACK + (int(255 - self.fade_alpha),)
            arcade.draw_rectangle_filled(
                self.window.width // 2, self.window.height // 2,
                self.window.width, self.window.height,
                fade_overlay
            )
        
        # Show instructions
        if self.is_playing:
            arcade.draw_text(
                    "ENTER - Skip the final cutscene",
                self.window.width // 2, 50,
                arcade.color.WHITE, 14,
                anchor_x="center"
            )
        else:
            arcade.draw_text(
                    "ENTER - Return to menu",
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
        
        # Frame animation with smooth transitions
        if self.is_playing and self.fade_in_complete:
            if self.current_frame < len(self.frame_durations):
                current_duration = self.frame_durations[self.current_frame]
                
                self.frame_timer += delta_time
                
                # Calculate transition alpha for smooth blending
                transition_start = current_duration - 0.2  # Start transition 0.2s before frame end
                if self.frame_timer >= transition_start and self.current_frame + 1 < len(self.scene_frames):
                    # Create smooth fade transition
                    transition_progress = (self.frame_timer - transition_start) / 0.2
                    self.transition_alpha = min(255, transition_progress * 255)
                else:
                    self.transition_alpha = 0
                
                # Change frame when duration is complete
                if self.frame_timer >= current_duration:
                    self.frame_timer = 0
                    self.current_frame += 1
                    self.transition_alpha = 0
                    
                    # Special handling for the first 8 frames (loop 3 times)
                    if self.current_frame == 7 and self.loop_count < self.max_loops:
                        self.loop_count += 1
                        self.current_frame = 0  # Reset to first frame
                    
                    # Check if sequence is complete
                    elif self.current_frame >= len(self.scene_frames):
                        self.is_playing = False
                        self.current_frame = len(self.scene_frames) - 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            if self.is_playing:
                # Skip to end of sequence
                self.is_playing = False
                self.current_frame = len(self.scene_frames) - 1 if self.scene_frames else 0
            else:
                # Return to main menu
                from .intro_view import IntroView
                menu_view = IntroView()
                self.window.show_view(menu_view)