import arcade

class ExplorerDeathScene(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene_frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_durations = []
        self.is_playing = True
        self.fade_alpha = 0
        self.fade_in_complete = False
        
    def on_show(self):
        # Reset viewport to ensure proper positioning
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        
        # Load all 19 explorer death animation frames
        frame_files = []
        for i in range(1, 20):  # frames 1-19
            frame_files.append(f"explorer_death_{i:02d}.png")
        
        # Set individual durations for each frame (all 0.2 seconds for now)
        self.frame_durations = [
            0.2,  # explorer_death_01
            0.2,  # explorer_death_02
            0.2,  # explorer_death_03
            0.2,  # explorer_death_04
            0.2,  # explorer_death_05
            0.2,  # explorer_death_06
            0.2,  # explorer_death_07
            0.2,  # explorer_death_08
            0.2,  # explorer_death_09
            0.2,  # explorer_death_10
            0.2,  # explorer_death_11
            0.2,  # explorer_death_12
            0.2,  # explorer_death_13
            0.2,  # explorer_death_14
            0.2,  # explorer_death_15
            0.2,  # explorer_death_16
            0.2,  # explorer_death_17
            0.2,  # explorer_death_18
            0.2   # explorer_death_19
        ]
        
        # Try to load all frames
        for frame_file in frame_files:
            try:
                texture = arcade.load_texture(f"assets/explorer_death_sequence/{frame_file}")
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
                    
                    # Check if sequence is complete
                    if self.current_frame >= len(self.scene_frames):
                        self.is_playing = False
                        self.current_frame = len(self.scene_frames) - 1
                        
                        # After sequence completes, wait 2 seconds then return to menu
                        arcade.schedule(self.return_to_menu, 2.0)

    def return_to_menu(self, delta_time):
        arcade.unschedule(self.return_to_menu)
        from .intro_view import IntroView
        menu_view = IntroView()
        self.window.show_view(menu_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.is_playing:
                # Skip to end of sequence
                self.is_playing = False
                self.current_frame = len(self.scene_frames) - 1 if self.scene_frames else 0
                arcade.schedule(self.return_to_menu, 1.0)
            else:
                # Return to menu immediately
                arcade.unschedule(self.return_to_menu)
                from .intro_view import IntroView
                menu_view = IntroView()
                self.window.show_view(menu_view)