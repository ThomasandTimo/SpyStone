import arcade

class IntroView(arcade.View):
    def __init__(self):
        super().__init__()
        self.mountain_texture = None
        
    def on_show(self):
        # Load the mountain background image
        try:
            self.mountain_texture = arcade.load_texture("assets/startmenu.png")
        except:  # noqa: E722
            # Fallback if image not found - use solid color
            arcade.set_background_color(arcade.color.SKY_BLUE)
        
        self.soundtrack = arcade.load_sound("assets/audio/main_theme.mp3")
        self.soundtrack_player = arcade.play_sound(self.soundtrack, volume=0.5, looping=True)

    def on_draw(self):
        self.clear()
        
        # Draw mountain background if available
        if self.mountain_texture:
            # Scale the mountain image to fill the screen
            arcade.draw_scaled_texture_rectangle(
                center_x=self.window.width / 2,
                center_y=self.window.height / 2,
                texture=self.mountain_texture,
                scale=max(self.window.width / self.mountain_texture.width,
                         self.window.height / self.mountain_texture.height)
            )
            
        # Credits
        arcade.draw_text(
            "A GameJam Production",
            self.window.width / 2, 50,
            arcade.color.GRAY, 14,
            anchor_x="center", anchor_y="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            # Transition to cinematic sequence first
            from .cinematic_sequence_view import CinematicSequenceView
            cinematic = CinematicSequenceView()
            self.window.show_view(cinematic)
        elif key == arcade.key.ESCAPE:
            # Quit the game
            self.window.close()