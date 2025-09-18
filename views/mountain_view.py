
import arcade
from managers.game_manager import GameManager
from levels.level1 import Level1
from levels.level2 import Level2
from levels.level3 import Level3
import textwrap

import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCROLL_MARGIN = 200
MIN_CHARGE_TIME= 0.2

class MountainView(arcade.View):
    def __init__(self):
        super().__init__()
        self.levels = [Level3(), Level2(),Level1()]
        self.current_level_index = 0
        self.level = self.levels[self.current_level_index]
        self.level.setup()
        self.game_manager = GameManager()
        self._connect_level_to_manager()
        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        # S'assure que la physique est correctement initialisée dès le départ
        self.game_manager.setup(self.level)

    def wrap_text(self, text, max_width, font_size=18):
        """Enveloppe le texte en respectant les limites des mots"""
        # Estimation approximative de la largeur des caractères
        char_width = font_size * 0.6
        max_chars = int(max_width / char_width)
        
        # Utilise textwrap pour diviser le texte
        wrapped_lines = textwrap.wrap(text, width=max_chars)
        return wrapped_lines

    def _connect_level_to_manager(self):
        self.game_manager.platform_list = self.level.platforms
        self.game_manager.obstacle_list = self.level.obstacles
        self.game_manager.dialogue_triggers = self.level.dialogue_triggers
        # Branche des callbacks de transition spécifiques au niveau
        if hasattr(self.level, "__dict__"):
            self.level.on_next_level = self.go_to_next_level
            self.level.on_yeti_scene = self.go_to_yeti_scene
            # Expose managers au niveau pour lancer des dialogues
            self.level.game_manager = self.game_manager
            self.level.dialogue_manager = self.game_manager.dialogue_manager
        # Synchronise les trous du niveau courant
        if hasattr(self.level, "holes"):
            self.game_manager.holes = self.level.holes
        else:
            self.game_manager.holes = []

    def setup(self):
        self.game_manager.setup(self.level)

    def on_draw(self):
        arcade.start_render()
        self.camera_sprites.use()
        # Fond du niveau
        self.level.draw_background()

        # Dessine tous les sprites
        self.game_manager.platform_list.draw()
        self.game_manager.obstacle_list.draw()
        self.game_manager.bonus_list.draw()

        # Dessine le joueur (caillou)
        if self.game_manager.player:
            self.game_manager.player.draw()

        # Trous
        for hole in self.game_manager.holes:
            arcade.draw_rectangle_filled(
                hole.center_x, 20, hole.width, 40, arcade.color.BLUE
            )


        # --- Jauge de saut ---
        player = self.game_manager.player
        if player.jump_charging and (time.time() - player.jump_press_time) >= MIN_CHARGE_TIME:
            gauge_width = 150
            gauge_height = 20
            power_ratio = player.jump_power / player.max_jump_power
            filled_width = gauge_width * power_ratio

            # Position de la jauge en bas à droite, 10 px du bas et du bord
            x = self.camera_sprites.position[0] + SCREEN_WIDTH - gauge_width - 20
            y = 10

            # Fond de la jauge (gris)
            arcade.draw_rectangle_filled(
                x + gauge_width / 2, y + gauge_height / 2,
                gauge_width, gauge_height,
                arcade.color.GRAY
            )

            # Partie remplie (vert) correspondant à la puissance du saut
            arcade.draw_rectangle_filled(
                x + filled_width / 2, y + gauge_height / 2,
                filled_width, gauge_height,
                arcade.color.GREEN
            )

            # Bordure de la jauge
            arcade.draw_rectangle_outline(
                x + gauge_width / 2, y + gauge_height / 2,
                gauge_width, gauge_height,
                arcade.color.BLACK, 2
            )

        # Dialogue (texte et choix)
        dm = self.game_manager.dialogue_manager
        if dm.active:
            line = dm.get_current_line()
            # Affiche le sprite de dialogue si défini dans le niveau
            dialogue_box_texture = getattr(self.level, 'dialogue_box_texture', None)
            dialogue_box_width = SCREEN_WIDTH-200
            
            # Calcule la hauteur en fonction du nombre de lignes de texte
            max_width = SCREEN_WIDTH - 420
            wrapped_lines = self.wrap_text(line, max_width, 18)
            text_lines = len(wrapped_lines)
            dialogue_box_height = 140 + (text_lines - 1) * 22 + (30 if dm.choices else 0)
            
            dialogue_box_x = self.camera_sprites.position[0]+SCREEN_WIDTH//2
            dialogue_box_y = 100

            # Affiche la boîte de dialogue d'abord
            if dialogue_box_texture:
                arcade.draw_lrwh_rectangle_textured(
                    dialogue_box_x - dialogue_box_width//2,
                    dialogue_box_y - dialogue_box_height//2,
                    dialogue_box_width,
                    dialogue_box_height,
                    dialogue_box_texture
                )
            else:
                # Boîte claire pour un contraste fort avec du texte sombre
                arcade.draw_rectangle_filled(
                    dialogue_box_x, dialogue_box_y,
                    dialogue_box_width, dialogue_box_height, (245,245,245,230)
                )

            # Puis le personnage par-dessus (fullbody ou tête)
            char_fullbody_texture = getattr(self.level, 'dialogue_character_fullbody_texture', None)
            char_head_texture = getattr(self.level, 'dialogue_character_head_texture', None)

            if char_fullbody_texture:
                char_x = self.camera_sprites.position[0] + 120
                char_y = dialogue_box_y + dialogue_box_height//2 - 40
                char_w = 100
                char_h = 200
                arcade.draw_lrwh_rectangle_textured(
                    char_x - char_w//2, char_y - char_h//2,
                    char_w, char_h, char_fullbody_texture
                )
            elif char_head_texture:
                char_w = 90
                char_h = 90
                char_x = self.camera_sprites.position[0] + 170
                char_y = dialogue_box_y + dialogue_box_height//2 - 60
                arcade.draw_lrwh_rectangle_textured(
                    char_x - char_w//2, char_y - char_h//2,
                    char_w, char_h, char_head_texture
                )

            # Texte du dialogue (un peu décalé à droite du personnage)
            text_x = self.camera_sprites.position[0]+250
            text_y = dialogue_box_y + dialogue_box_height//2 - 40  # Centré verticalement
            
            # Word wrap pour éviter que le texte déborde
            max_width = SCREEN_WIDTH - 420
            wrapped_lines = self.wrap_text(line, max_width, 18)
            
            # Dessine chaque ligne de texte
            line_height = 22
            for i, wrapped_line in enumerate(wrapped_lines):
                arcade.draw_text(
                    wrapped_line,
                    text_x, text_y - (i * line_height),
                    arcade.color.DARK_BLUE, 18
                )
            # Affichage des choix si présents
            if dm.choices and dm.is_showing_choices():
                if len(dm.choices) == 2:
                    # Deux choix côte à côte
                    choice_y = 80
                    spacing = 260
                    center_x = self.camera_sprites.position[0]+SCREEN_WIDTH//2
                    for idx, choice in enumerate(dm.choices):
                        choice_x = center_x + (idx - 0.5) * spacing
                        selected = (dm.cursor_position == idx)
                        color = arcade.color.DARK_BLUE if selected else arcade.color.DARK_SLATE_GRAY
                        size = 20 if selected else 18
                        arcade.draw_text(choice, choice_x, choice_y, color, size, anchor_x="center")
                        if selected:
                            width_est = max(40, len(choice) * 9)
                            arcade.draw_line(choice_x - width_est//2, choice_y - 6, choice_x + width_est//2, choice_y - 6, arcade.color.DARK_BLUE, 2)
                    arcade.draw_text(
                        "← → pour naviguer, ENTRÉE pour choisir",
                        center_x, 50,
                        arcade.color.DARK_SLATE_GRAY, 14, anchor_x="center"
                    )
                else:
                    # Liste verticale fallback
                    for idx, choice in enumerate(dm.choices):
                        selected = (dm.cursor_position == idx)
                        arcade.draw_text(
                            f"{idx+1}. {choice}",
                            self.camera_sprites.position[0]+80,
                            120 + 30*(len(dm.choices)-idx-1),
                            arcade.color.YELLOW if selected else arcade.color.LIGHT_GRAY,
                            16
                        )
                    arcade.draw_text(
                        "← → pour naviguer, ENTRÉE pour choisir",
                        self.camera_sprites.position[0]+SCREEN_WIDTH//2, 50,
                        arcade.color.LIGHT_GRAY, 14, anchor_x="center"
                    )
            elif not dm.is_showing_choices():
                arcade.draw_text(
                    "ESPACE ou flèche bas pour continuer",
                    self.camera_sprites.position[0]+SCREEN_WIDTH//2, 60,
                    arcade.color.LIGHT_GRAY, 14, anchor_x="center"
                )


        # QTE
        if self.game_manager.qte_manager.active:
            self.game_manager.qte_manager.draw(self.camera_sprites.position[0] + SCREEN_WIDTH / 2)

            
    def back_to_intro(self, delta_time):
        arcade.unschedule(self.back_to_intro)
        from views.intro_view import IntroView
        self.window.show_view(IntroView())
        
    def show_game_over(self, delta_time):
        arcade.unschedule(self.show_game_over)
        
        # Réinitialiser la caméra à (0, 0) AVANT de changer de vue
        self.camera_sprites.move_to((0, 0))
        self.game_manager.player.reset_position()
        
        # Attendre un frame pour que la caméra soit mise à jour
        arcade.schedule(self._transition_to_game_over, 0.01)

    def _transition_to_game_over(self, delta_time):
        arcade.unschedule(self._transition_to_game_over)
        from views.game_over_view import GameOverView
        self.window.show_view(GameOverView())
        
    def on_update(self, delta_time):
        self.game_manager.update()
        self.scroll_to_player()

        # Vérifie si un dialogue vient de se terminer et qu'il y a une transition en attente
        if (hasattr(self.level, 'pending_transition') and 
            self.level.pending_transition and 
            not self.game_manager.dialogue_manager.active):
            
            if self.level.pending_transition == 'safe':
                self.go_to_next_level()
            elif self.level.pending_transition == 'yeti':
                self.go_to_yeti_scene()
            
            # Nettoie la transition en attente
            self.level.pending_transition = None

        # Transition automatique : si le joueur atteint la fin du niveau courant
        # (exemple : position x > 950)
        if self.game_manager.player.center_x > 950:
            self.go_to_next_level()

        # Mort si tombe sous l'écran
        if self.game_manager.player.center_y < 0 and not self.game_manager.is_game_over:
            self.game_manager.is_game_over = True
            arcade.schedule(self.show_game_over, 1.0)

    def scroll_to_player(self):
        left_boundary = self.camera_sprites.position[0] + SCROLL_MARGIN
        right_boundary = self.camera_sprites.position[0] + SCREEN_WIDTH - SCROLL_MARGIN

        player_x = self.game_manager.player.center_x

        if player_x < left_boundary:
            self.camera_sprites.move_to((player_x - SCROLL_MARGIN, 0), 0.2)
        elif player_x > right_boundary:
            self.camera_sprites.move_to((player_x - SCREEN_WIDTH + SCROLL_MARGIN, 0), 0.2)

    def go_to_next_level(self):
        if self.current_level_index + 1 < len(self.levels):
            self.current_level_index += 1
            self.level = self.levels[self.current_level_index]
            self.level.setup()
            self._connect_level_to_manager()
            self.game_manager.setup(self.level)  # Reset le joueur et la physique
            self.camera_sprites.move_to((0, 0))
        else:
            arcade.schedule(self.show_game_over, 0.5)

    def go_to_yeti_scene(self):
        from views.yeti_view import YetiView
        self.window.show_view(YetiView())

    def on_key_press(self, key, modifiers):
        dm = self.game_manager.dialogue_manager
        # Si dialogue bloquant, on bloque les contrôles joueur
        if dm.is_blocking():
            # Navigation et validation des choix au clavier
            if dm.is_showing_choices():
                if key == arcade.key.LEFT:
                    dm.move_cursor_left()
                elif key == arcade.key.RIGHT:
                    dm.move_cursor_right()
                elif key in (arcade.key.ENTER, arcade.key.RETURN):
                    dm.confirm_choice()
            else:
                # Avance le dialogue
                if key in (arcade.key.SPACE, arcade.key.DOWN):
                    dm.next_line()
        else:
            # Contrôles classiques du joueur (toujours actifs si non bloquant)
            self.game_manager.handle_key_press(key)

    def on_key_release(self, key, modifiers):
        self.game_manager.handle_key_release(key)
