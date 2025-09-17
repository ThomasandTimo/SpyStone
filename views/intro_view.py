import arcade

class IntroView(arcade.View):
    def __init__(self):
        super().__init__()
        self.mountain_texture = None
        
    def on_show(self):
        # Load the mountain background image
        try:
            self.mountain_texture = arcade.load_texture("assets/background_glacial_mountains.png")
        except:
            # Fallback if image not found - use solid color
            arcade.set_background_color(arcade.color.SKY_BLUE)

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
        
        # Semi-transparent overlay for better text readability
        arcade.draw_rectangle_filled(
            center_x=self.window.width / 2,
            center_y=self.window.height / 2,
            width=self.window.width,
            height=self.window.height,
            color=(*arcade.color.BLACK, 100)  # Semi-transparent black
        )
        
        # Game Title
        arcade.draw_text(
            "LE CAILLOU SPECTATEUR",
            self.window.width / 2, self.window.height - 100,
            arcade.color.WHITE, 48,
            anchor_x="center", anchor_y="center",
            font_name="Arial"
        )
        
        # Subtitle/Description - Split into separate lines
        arcade.draw_text(
            "Un héros grimpe l'Everest...",
            self.window.width / 2, self.window.height / 2 + 80,
            arcade.color.WHITE, 20,
            anchor_x="center", anchor_y="center"
        )
        
        arcade.draw_text(
            "Mais vous n'êtes qu'un simple caillou.",
            self.window.width / 2, self.window.height / 2 + 20,
            arcade.color.WHITE, 20,
            anchor_x="center", anchor_y="center"
        )
        
        # Menu Options
        arcade.draw_text(
            "ESPACE - Commencer l'aventure",
            self.window.width / 2, self.window.height / 2 - 50,
            arcade.color.LIGHT_GRAY, 18,
            anchor_x="center", anchor_y="center"
        )
        
        arcade.draw_text(
            "ESC - Quitter",
            self.window.width / 2, self.window.height / 2 - 100,
            arcade.color.LIGHT_GRAY, 18,
            anchor_x="center", anchor_y="center"
        )
        
        # Credits
        arcade.draw_text(
            "Une production GameJam",
            self.window.width / 2, 50,
            arcade.color.GRAY, 14,
            anchor_x="center", anchor_y="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            # Use the same import style as your original code
            from .intro_scene_view import IntroSceneView
            # Start the game
            intro_scene = IntroSceneView()
            self.window.show_view(intro_scene)
        elif key == arcade.key.ESCAPE:
            # Quit the game
            self.window.close()