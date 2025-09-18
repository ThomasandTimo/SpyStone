import arcade

from views.crossroads_completion_scene import CrossroadsCompletionScene

class CinematicSequenceView(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene_frames = []
        self.current_frame = 0
        self.frame_durations = []  # Different duration for each frame
        self.frame_timer = 0
        self.is_playing = True
        self.fade_alpha = 0
        self.fade_in_complete = False
        self.transition_alpha = 0  # For smooth frame transitions
        
    def on_show(self):
        # Load all the sequence frames
        frame_files = [
            "scene_01.png", "scene_02.png", "scene_03.png", "scene_04.png",
            "scene_05.png", "scene_06.png", "scene_07.png", "scene_08.png", 
            "scene_09.png", "scene_10.png", "scene_11.png", "scene_12.png",
            "scene_13.png", "scene_14.png", "scene_15.png", "scene_16.png",
            "scene_17.png"
        ]
        
        # Set different durations for each frame (in seconds)
        self.frame_durations = [
            0.1,  # scene_01 - establishing shot
            0.1,  # scene_02 - quick transition
            0.1,  # scene_03 - medium pause
            0.1,  # scene_04 - quick
            0.1,  # scene_05 - explorer appears, longer pause
            0.1,  # scene_06 - medium
            0.1,  # scene_07 - medium
            0.1,  # scene_08 - stone appears, longer pause
            0.1,  # scene_09 - medium
            0.1,  # scene_10 - medium
            0.1,  # scene_11 - medium
            0.1,  # scene_12 - medium
            1.7,  # scene_13 - medium
            0.1,  # scene_14 - final mountain view
            0.1,  # scene_15 - close up, longer pause
            2.0,  # scene_16 - stone detail
            2.0   # scene_17 - final frame, longest pause
        ]
        
                # Try to load all frames
        for frame_file in frame_files:
            try:
                texture = arcade.load_texture(f"assets/sequence/{frame_file}")
                self.scene_frames.append(texture)
            except:
                print(f"Could not load {frame_file}")
                continue
        
        if not self.scene_frames:
            # Fallback if no images load
            arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        self.clear()
        
        # Always draw current frame (never let screen go empty)
        if self.scene_frames and self.current_frame < len(self.scene_frames):
            current_texture = self.scene_frames[self.current_frame]
            
            # Scale to fit screen while maintaining aspect ratio
            scale_x = self.window.width / current_texture.width
            scale_y = self.window.height / current_texture.height
            scale = min(scale_x, scale_y)
            
            # Always draw current frame at full opacity first (ensures no blank screen)
            arcade.draw_scaled_texture_rectangle(
                center_x=self.window.width // 2,
                center_y=self.window.height // 2,
                texture=current_texture,
                scale=scale
            )
            
            # Only draw transition overlay if we're transitioning
            if (self.current_frame + 1 < len(self.scene_frames) and 
                self.transition_alpha > 0):
                next_texture = self.scene_frames[self.current_frame + 1]
                # Draw next frame on top with transition alpha
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
                "SPACE - Skip the cutscene",
                self.window.width // 2, 50,
                arcade.color.WHITE, 14,
                anchor_x="center"
            )
        else:
            arcade.draw_text(
                "SPACE - Continue",
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
        
        # Frame animation with variable timing and smooth transitions
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
                    
                    # Check if sequence is complete
                    if self.current_frame >= len(self.scene_frames):
                        self.is_playing = False
                        self.current_frame = len(self.scene_frames) - 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.is_playing:
                # Skip to end of sequence
                self.is_playing = False
                self.current_frame = len(self.scene_frames) - 1 if self.scene_frames else 0
            else:
                # Continue to scrolling scene
                from .crossroads_scene import CrossroadsScene
                scrolling_view = CrossroadsScene()
                self.window.show_view(scrolling_view)