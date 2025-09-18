
import arcade
from managers.game_manager import GameManager
from levels.level0 import Level0
from levels.level1 import Level1
from levels.level2 import Level2
from levels.level3 import Level3
import textwrap
import random

import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCROLL_MARGIN = 200
MIN_CHARGE_TIME= 0.2

class MountainView(arcade.View):
    def __init__(self):
        super().__init__()
        self.levels = [Level0(), Level1(),Level3()]
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

        # Dessine les obstacles spécifiques au Level 3
        if hasattr(self.level, 'draw_obstacles'):
            self.level.draw_obstacles(self.camera_sprites.position[0])

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
                        "← → to navigate, ENTER to select",
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
                        "← → to navigate, ENTER to select",
                        self.camera_sprites.position[0]+SCREEN_WIDTH//2, 50,
                        arcade.color.LIGHT_GRAY, 14, anchor_x="center"
                    )
            elif not dm.is_showing_choices():
                arcade.draw_text(
                    "ENTER or DOWN ARROW to continue",
                    self.camera_sprites.position[0]+SCREEN_WIDTH//2, 60,
                    arcade.color.LIGHT_GRAY, 14, anchor_x="center"
                )


        # QTE
        if self.game_manager.qte_manager.active:
            self.game_manager.qte_manager.draw(self.camera_sprites.position[0] + SCREEN_WIDTH / 2)
        
        # Effets visuels du Level 3 (vent, QTE)
        if hasattr(self.level, 'draw_wind_effects'):
            self.level.draw_wind_effects(self.camera_sprites.position[0])
        if hasattr(self.level, 'draw_qte_indicator'):
            self.level.draw_qte_indicator(self.camera_sprites.position[0])

            
    def back_to_intro(self, delta_time):
        arcade.unschedule(self.back_to_intro)
        from views.intro_view import IntroView
        self.window.show_view(IntroView())
        
    def show_game_over(self, delta_time):
        arcade.unschedule(self.show_game_over)
        # Affiche la scène d'animation de mort du caillou
        from views.death_animation_scene import DeathAnimationScene
        self.window.show_view(DeathAnimationScene())
        
    def on_update(self, delta_time):
        self.game_manager.update()
        self.scroll_to_player()

        # === GESTION DU VENT POUR LEVEL 3 ===
        if hasattr(self.level, 'get_wind_force'):
            wind_force = self.level.get_wind_force(self.game_manager.player)
            self.game_manager.player.wind_force = wind_force

        # === GESTION DES QTE DU LEVEL 3 ===
        if hasattr(self.level, 'qte_active') and self.level.qte_active:
            self.level.qte_timer += delta_time
            if self.level.qte_timer >= self.level.qte_duration:
                # QTE échoué
                self.level.qte_active = False
                self.level.gust_active = False
                self.level.wind_strength = 0.5  # Vent plus fort après échec

        # === ACTIVATION ALÉATOIRE DES ROCHERS ===
        if hasattr(self.level, 'activate_random_rock'):
            if random.random() < 0.01:  # 1% de chance par frame
                self.level.activate_random_rock()

        # Vérifie si un dialogue vient de se terminer et qu'il y a une transition en attente
        if (hasattr(self.level, 'pending_transition') and 
            self.level.pending_transition and 
            not self.game_manager.dialogue_manager.active):
            if self.level.pending_transition == 'yeti':
                self.go_to_yeti_scene()
            elif self.level.pending_transition == 'crossroads':
                self.go_to_crossroads_scene()
            elif self.level.pending_transition == 'slope':
                self._pending_resume_level = self.current_level_index + 1
                self.go_to_slope_scene()
            elif self.level.pending_transition == 'slope_completion':
                self.go_to_slope_completion_scene()
            # Nettoie la transition en attente
            self.level.pending_transition = None

        # Transition automatique de Level0 à Level1 uniquement
        if (
            isinstance(self.level, Level0)
            and self.game_manager.player.center_x > self.level.level_end_x
            and not self.game_manager.dialogue_manager.active
        ):
            # Crée une nouvelle MountainView qui commence au Level1 (index 0 de la nouvelle liste)
            new_view = MountainView()
            new_view.levels = [Level1(), Level3()]
            new_view.current_level_index = 0
            new_view.level = new_view.levels[0]
            new_view.level.setup()
            new_view._connect_level_to_manager()
            new_view.game_manager.setup(new_view.level)
            new_view.camera_sprites.move_to((0, 0))
            self.window.show_view(new_view)
            return

        # Si on est sur le dernier niveau et que le joueur dépasse la fin, on lance la slope completion scene
        if (
            isinstance(self.level, Level3)
            and self.game_manager.player.center_x > self.level.level_end_x
            and not self.game_manager.dialogue_manager.active
        ):
            self.go_to_slope_completion_scene()

        # Vérifie la chute du joueur pour le game over (mort du caillou)
        if self.game_manager.player.center_y < 0 and not self.game_manager.is_game_over:
            self.game_manager.is_game_over = True
            arcade.schedule(self.show_game_over, 1.0)

    def go_to_slope_completion_scene(self):
        from views.slope_completion_scene import SlopeCompletionScene
        slope_completion_scene = SlopeCompletionScene()
        self.window.show_view(slope_completion_scene)

        # Vérifie la chute du joueur pour le game over
        if self.game_manager.player.center_y < 0 and not self.game_manager.is_game_over:
            self.game_manager.is_game_over = True
            arcade.schedule(self.show_game_over, 1.0)

    def go_to_crossroads_scene(self):
        # Sauvegarde la position du joueur et l'état des triggers avant l'animation
        self._crossroads_player_pos = (
            self.game_manager.player.center_x,
            self.game_manager.player.center_y
        )
        # Sauvegarde l'état des triggers (clé 'triggered')
        self._crossroads_triggers_state = [
            dict(x=trig.get('x'), triggered=trig.get('triggered', False))
            for trig in getattr(self.level, 'dialogue_triggers', [])
        ]
        # Sauvegarde aussi l'état des QTE triggers (clé 'triggered')
        self._crossroads_qte_state = [
            dict(x=trig.get('x'), triggered=trig.get('triggered', False))
            for trig in getattr(self.level, 'qte_triggers', [])
        ]
        from views.crossroads_completion_scene import CrossroadsCompletionScene
        crossroads = CrossroadsCompletionScene(mountain_view=self)
        self.window.show_view(crossroads)

    def resume_after_crossroads(self):
        # Replace le joueur à la position sauvegardée avant l'animation
        self.current_level_index = 0
        self.level = self.levels[self.current_level_index]
        self.level.setup()
        self._connect_level_to_manager()
        self.game_manager.setup(self.level)
        self.camera_sprites.move_to((0, 0))
        # Utilise la position sauvegardée si dispo, sinon fallback
        pos = getattr(self, '_crossroads_player_pos', (3550, 400))
        if hasattr(self.game_manager.player, 'reset_position'):
            self.game_manager.player.reset_position(x=pos[0], y=pos[1])
        # Restaure l'état des triggers (clé 'triggered')
        triggers_state = getattr(self, '_crossroads_triggers_state', None)
        if triggers_state:
            for trig in self.level.dialogue_triggers:
                for saved in triggers_state:
                    if trig.get('x') == saved.get('x'):
                        trig['triggered'] = saved['triggered']
        # Restaure aussi l'état des QTE triggers
        qte_state = getattr(self, '_crossroads_qte_state', None)
        if qte_state:
            for trig in getattr(self.level, 'qte_triggers', []):
                for saved in qte_state:
                    if trig.get('x') == saved.get('x'):
                        trig['triggered'] = saved['triggered']
        # Nettoie les variables temporaires
        if hasattr(self, '_crossroads_player_pos'):
            del self._crossroads_player_pos
        if hasattr(self, '_crossroads_triggers_state'):
            del self._crossroads_triggers_state
        if hasattr(self, '_crossroads_qte_state'):
            del self._crossroads_qte_state

        # Vérifie si le joueur est tombé sous l'écran après restauration
        if self.game_manager.player.center_y < 0:
            self.game_manager.is_game_over = True
            arcade.schedule(self.show_game_over, 1.0)
            return

        # Transition automatique : si le joueur atteint la fin du niveau courant
        # (exemple : position x > level.end_width)
        if self.game_manager.player.center_x > self.level.level_end_x:
            # Si on termine le Level1 (index 1), on lance la YetiView
            if self.current_level_index == 1:
                self._pending_resume_level = self.current_level_index + 1  # On reprendra au Level2
                self.go_to_yeti_scene()
            elif self.current_level_index + 1 < len(self.levels):
                # SAFE ROUTE : on lance la SlopeScene avant Level3
                self.current_level_index += 1
                self._pending_resume_level = self.current_level_index
                self.go_to_slope_scene()
            else:
                # Dernier niveau atteint, retour à l'intro ou écran de fin
                arcade.schedule(self.show_game_over, 0.5)

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
        # Passe une référence à MountainView pour pouvoir reprendre après la YetiView
        yeti_view = YetiView(mountain_view=self)
        self.window.show_view(yeti_view)

    def resume_after_yeti(self):
        # Reprend la progression après la YetiView
        if hasattr(self, '_pending_resume_level'):
            self.current_level_index = self._pending_resume_level
            del self._pending_resume_level
            # Affiche la SlopeScene avant de lancer le niveau suivant
            self.go_to_slope_scene()

    def on_key_press(self, key, modifiers):
        # Quitter le jeu si ECHAP
        if key == arcade.key.ESCAPE:
            arcade.close_window()
            return
        dm = self.game_manager.dialogue_manager
        if dm.active:
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
                if key in (arcade.key.ENTER, arcade.key.DOWN):
                    dm.next_line()
        else:
            # === GESTION DES QTE DU LEVEL 3 ===
            if hasattr(self.level, 'handle_qte'):
                if self.level.handle_qte(key):
                    return  # QTE réussi, ne pas traiter comme mouvement normal
            # Contrôles classiques du joueur
            self.game_manager.handle_key_press(key)

    def on_key_release(self, key, modifiers):
        self.game_manager.handle_key_release(key)

    def go_to_slope_scene(self):
        from views.slope_scene import SlopeScene
        slope_scene = SlopeScene()
        slope_scene.mountain_view = self  # Pour rappel du callback
        self.window.show_view(slope_scene)

    def resume_after_slope(self):
        # Appelé par la SlopeScene pour lancer le niveau suivant (Level3)
        print("Reprise après SlopeScene")
        # Passe au niveau suivant
        if self.current_level_index + 1 < len(self.levels):
            self.current_level_index += 1
        self.level = self.levels[self.current_level_index]
        self.level.setup()
        self._connect_level_to_manager()
        self.game_manager.setup(self.level)
        self.camera_sprites.move_to((0, 0))
        self.game_manager.is_game_over = False
        # Affiche la MountainView à l'écran
        if self.window:
            self.window.show_view(self)
        
        
    def on_show_view(self):
        # Si on revient du YetiView et une reprise est en attente, effectue la reprise
        if hasattr(self, "pending_resume_after_yeti") and self.pending_resume_after_yeti:
            self.pending_resume_after_yeti = False
            self.resume_after_yeti()
