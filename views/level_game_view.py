import arcade
from models.player import Player

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCROLL_MARGIN = 200

class LevelGameView(arcade.View):
    def __init__(self, level_class):
        super().__init__()
        self.level = level_class()
        self.player = Player()
        self.physics_engine = None
        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.is_game_over = False
        
    def setup(self):
        # Setup the level
        self.level.setup()
        
        # Setup player
        self.player.center_x = 100
        self.player.center_y = 100
        
        # Create physics engine with level platforms
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, 
            self.level.platforms, 
            gravity_constant=0.5
        )

    def on_draw(self):
        self.clear()
        self.camera_sprites.use()
        
        # Draw level background
        self.level.draw_background()
        
        # Draw level elements
        self.level.platforms.draw()
        self.level.obstacles.draw()
        
        # Draw player
        self.player.draw()
        
        # Draw holes (from level.py)
        for hole in self.level.holes:
            arcade.draw_rectangle_filled(
                hole.center_x, 20, hole.width, 40, arcade.color.BLACK
            )
        
        # UI - Show level name
        arcade.draw_text(
            f"{self.level.name}",
            self.camera_sprites.position[0] + 20, 
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE, 
            16
        )
        
        # Show win condition
        if self.player.center_x > 900:  # Near end of level
            arcade.draw_text(
                "ESPACE - Terminer le niveau",
                self.camera_sprites.position[0] + SCREEN_WIDTH//2,
                SCREEN_HEIGHT//2,
                arcade.color.YELLOW, 
                20,
                anchor_x="center"
            )

    def on_update(self, delta_time):
        if not self.is_game_over:
            # Update physics
            self.physics_engine.update()
            self.player.update()
            
            # Update level
            self.level.update(delta_time)
            self.level.obstacles.update()
            
            # Check collision with obstacles
            for obstacle in self.level.obstacles:
                if arcade.check_for_collision(self.player, obstacle):
                    self.reset_player()
            
            # Check holes
            for hole in self.level.holes:
                if hole.check_fall(self.player):
                    self.trigger_death_animation()
            
            # Check if player fell off screen
            if self.player.center_y < 0:
                self.trigger_death_animation()
            
            # Update camera
            self.scroll_to_player()
            
            # Check dialogue triggers
            for trigger in self.level.dialogue_triggers:
                if (not trigger["triggered"] and 
                    abs(self.player.center_x - trigger["x"]) < 50):
                    trigger["triggered"] = True
                    print(f"Dialogue: {trigger['lines'][0]}")  # Simple dialogue for now

    def scroll_to_player(self):
        left_boundary = self.camera_sprites.position[0] + SCROLL_MARGIN
        right_boundary = self.camera_sprites.position[0] + SCREEN_WIDTH - SCROLL_MARGIN

        player_x = self.player.center_x

        if player_x < left_boundary:
            self.camera_sprites.move_to((player_x - SCROLL_MARGIN, 0), 0.2)
        elif player_x > right_boundary:
            self.camera_sprites.move_to((player_x - SCREEN_WIDTH + SCROLL_MARGIN, 0), 0.2)

    def reset_player(self):
        self.player.center_x = 100
        self.player.center_y = 100
        self.player.change_x = 0
        self.player.change_y = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.player.move_right()
        elif key == arcade.key.LEFT:
            self.player.move_left()
        elif key == arcade.key.UP:
            # Use the physics engine's can_jump method directly
            if self.physics_engine.can_jump():
                self.player.change_y = 12  # Jump speed
        elif key == arcade.key.SPACE:
            # Check if player is near the end of level (win condition)
            if self.player.center_x > 900:
                self.complete_level()
            else:
                # Use SPACE for jumping when not near end
                if self.physics_engine.can_jump():
                    self.player.change_y = 12  # Jump speed

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.RIGHT, arcade.key.LEFT):
            self.player.stop()
    
    def trigger_death_animation(self):
        # Transition to death animation scene
        from .death_animation_scene import DeathAnimationScene
        death_scene = DeathAnimationScene()
        self.window.show_view(death_scene)
    
    def complete_level(self):
        # Check which level was completed
        if isinstance(self.level, type(self.level)) and hasattr(self.level, 'name'):
            if "Niveau 1" in self.level.name:
                # Return to crossroads completion scene
                from .crossroads_completion_scene import CrossroadsCompletionScene
                completion_scene = CrossroadsCompletionScene()
                self.window.show_view(completion_scene)
            elif "Niveau 2" in self.level.name:
                # Go to slope completion scene
                from .slope_completion_scene import SlopeCompletionScene
                slope_completion = SlopeCompletionScene()
                self.window.show_view(slope_completion)
        else:
            # Default to crossroads completion for Level 1
            from .crossroads_completion_scene import CrossroadsCompletionScene
            completion_scene = CrossroadsCompletionScene()
            self.window.show_view(completion_scene)