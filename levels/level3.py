import os
import arcade
import random
import time
from levels.level_base import LevelBase

class Level3(LevelBase):
    def __init__(self):
        super().__init__("Niveau 3 - La Montagne Venteuse", background_image=os.path.join("assets/background_glacial_mountains_large.png"))
        self.level_end_x = 1600
        
    def setup(self):
        super().setup()

        # === SOL DE DÉBUT ===
        # Plateforme de départ solide
        start_platform = arcade.SpriteSolidColor(200, 40, arcade.color.BLACK)
        start_platform.center_x = 100
        start_platform.center_y = 20
        self.platforms.append(start_platform)

        # === MUR DE GAUCHE ===
        # Grand mur vertical à gauche (comme dans le croquis)
        left_wall = arcade.SpriteSolidColor(100, 300, arcade.color.BLACK)
        left_wall.center_x = 0
        left_wall.center_y = 170
        self.platforms.append(left_wall)

        # === TRIGGERS QTE DE VENT ===
        self.wind_qte_triggers = [
            {"x": 400, "triggered": False},
            {"x": 900, "triggered": False}
        ]
        # === PENTE AVEC ZONES DE REPOS ===
        pente_length = 1400  # largeur totale du niveau (rallongée)
        segment_width = 20  # largeur d'un segment de pente
        start_y = 20  # point de départ en bas
        end_y = 400  # point final en haut (2/3 de la hauteur)
        num_segments = pente_length // segment_width

        # Définir les positions des zones de plat/renfoncement (en nombre de segments)
        plats = [int(num_segments * 0.25), int(num_segments * 0.5), int(num_segments * 0.75)]  # pas de nouveaux renfoncements
        plat_length = 5  # nombre de segments pour chaque plat
        renfoncement_depth = 25  # profondeur du renfoncement

        plat_wall_height = 60  # hauteur des murs verticaux
        for i in range(num_segments):
            x = 200 + segment_width / 2 + i * segment_width
            # Par défaut, interpolation linéaire
            progress = i / (num_segments - 1)
            y = start_y + (end_y - start_y) * progress

            # Vérifie si on est dans une zone de plat
            in_plat = False
            for plat_start in plats:
                if plat_start <= i < plat_start + plat_length:
                    # Renfoncement : le plat est un peu plus bas
                    y = start_y + (end_y - start_y) * (plat_start / (num_segments - 1)) - renfoncement_depth
                    in_plat = True
                    # Ajoute les murs verticaux au début et à la fin du plat
                    if i == plat_start:
                        # Mur gauche
                        wall_left = arcade.SpriteSolidColor(10, plat_wall_height, arcade.color.BLACK)
                        wall_left.center_x = x - segment_width / 2
                        wall_left.center_y = y + plat_wall_height / 2
                        self.platforms.append(wall_left)
                    if i == plat_start + plat_length - 1:
                        # Mur droit
                        wall_right = arcade.SpriteSolidColor(10, plat_wall_height, arcade.color.BLACK)
                        wall_right.center_x = x + segment_width / 2
                        wall_right.center_y = y + plat_wall_height / 2
                        self.platforms.append(wall_right)
                    break

            segment = arcade.SpriteSolidColor(segment_width, 15, arcade.color.BLACK)
            segment.center_x = x
            segment.center_y = y
            self.platforms.append(segment)

            # Remplissage sous la pente : rectangle du bas de l'écran jusqu'à la plateforme
            fill_height = y - 0  # du bas (y=0) jusqu'à la plateforme
            if fill_height > 0:
                fill = arcade.SpriteSolidColor(segment_width, int(fill_height), arcade.color.BLACK)
                fill.center_x = x
                fill.center_y = fill_height / 2
                self.platforms.append(fill)

        # # === PLATEFORME CENTRALE ÉLEVÉE ===
        # # Grande plateforme centrale avec pièges en dessous
        # central_platform = arcade.SpriteSolidColor(200, 30, arcade.color.BLACK)
        # central_platform.center_x = 500
        # central_platform.center_y = 550
        # self.platforms.append(central_platform)

        # # === PIÈGES SOUS LA PLATEFORME CENTRALE ===
        # # Spikes pointant vers le bas
        # spike_positions = [450, 500, 550]
        # for x in spike_positions:
        #     spike = arcade.SpriteSolidColor(20, 30, arcade.color.RED)
        #     spike.center_x = x
        #     spike.center_y = 500
        #     self.platforms.append(spike)


        # === SOL DE FIN ===
        # Plateforme de fin avec trou (bas)
        end_platform_left = arcade.SpriteSolidColor(100, 40, arcade.color.BLACK)
        end_platform_left.center_x = 750
        end_platform_left.center_y = 20
        self.platforms.append(end_platform_left)

        end_platform_right = arcade.SpriteSolidColor(100, 40, arcade.color.BLACK)
        end_platform_right.center_x = 950
        end_platform_right.center_y = 20
        self.platforms.append(end_platform_right)

        # === PLATEFORME DE FIN EN HAUT ===
        # Ajoute une grande plateforme en haut de la pente, à la fin du niveau
        final_platform_width = 600
        final_platform_height = 40
        final_platform_x = 500 + pente_length  # tout à droite du niveau
        final_platform_y = end_y +10 # un peu au-dessus du sommet de la pente
        final_platform = arcade.SpriteSolidColor(final_platform_width, final_platform_height, arcade.color.GOLD)
        final_platform.center_x = final_platform_x
        final_platform.center_y = final_platform_y
        self.platforms.append(final_platform)


        # === SYSTÈME DE VENT ===
        self.wind_active = False
        self.wind_strength = 0
        self.wind_direction = -1  # Toujours vers la gauche
        self.last_wind_change = 0
        self.wind_duration = 3.0  # Durée du vent en secondes

        # === QTE DE VENT ===
        self.qte_active = False
        self.qte_timer = 0
        self.qte_duration = 2.0
        self.qte_required_key = arcade.key.E
        self.last_qte_time = 0
        self.qte_cooldown = 1.0  # Cooldown entre les QTE

        # === OBSTACLES QUI TOMBENT ===
        self.obstacles = arcade.SpriteList()
        self.rock_spawn_interval = 2.0  # secondes
        for i in range(3):
            from models.obstacle import FallingObstacle
            obstacle = FallingObstacle(platforms=self.platforms)
            obstacle.center_x = 400 + i*150
            obstacle.center_y = 400 + i*50
            self.obstacles.append(obstacle)
        arcade.schedule(self.spawn_falling_obstacle_cyclic, self.rock_spawn_interval)

        # === OBSTACLES ===
        from models.obstacle import FallingObstacle
        for i in range(3):
            obstacle = FallingObstacle(platforms=self.platforms)
            obstacle.center_x = 400 + i*150
            obstacle.center_y = 400 + i*50
            self.obstacles.append(obstacle)

        # === TRIGGERS DE DIALOGUE ===
        self.dialogue_triggers = [
            {"x": 100, "lines": ["Niveau 3 : La montagne venteuse !", "Attention aux rafales !"], "triggered": False},
            {"x": 300, "lines": ["Le vent se lève...", "Appuyez sur E quand vous voyez l'indicateur !"], "triggered": False},
            {"x": 600, "lines": ["Un abri ! Reposez-vous un instant."], "triggered": False},
            {"x": 900, "lines": ["Presque arrivé !", "Dernière ligne droite !"], "triggered": False}
        ]
        
        arcade.schedule(self.force_wind_test, 3.0)

        # === QTE TRIGGERS ===
        # self.qte_triggers = [
        #     {
        #         "x": 250,
        #         "key": arcade.key.E,
        #         "triggered": False,
        #         "on_success": lambda: self.wind_success(),
        #         "on_fail": lambda: self.wind_fail()
        #     },
        #     {
        #         "x": 450,
        #         "key": arcade.key.E,
        #         "triggered": False,
        #         "on_success": lambda: self.wind_success(),
        #         "on_fail": lambda: self.wind_fail()
        #     },
        #     {
        #         "x": 700,
        #         "key": arcade.key.E,
        #         "triggered": False,
        #         "on_success": lambda: self.wind_success(),
        #         "on_fail": lambda: self.wind_fail()
        #     }
        # ]
        

    def wind_success(self):
        """QTE de vent réussi"""
        self.wind_active = False
        self.wind_strength = 0
        print("Rafale maîtrisée !")

    def wind_fail(self):
        """QTE de vent échoué"""
        self.wind_strength = 2.0  # Vent plus fort
        print("Rafale incontrôlable !")

    def get_wind_force(self, player):
        """Retourne la force du vent appliquée au joueur (vent constant très faible + rafales)"""
        base_wind = 0.025  # Vent constant très faible
        direction = self.wind_direction
        if self.wind_active:
            # Rafale : vent fort
            return (base_wind + self.wind_strength) * direction
        else:
            # Vent constant
            return base_wind * direction

    def activate_wind(self, strength = None):
        """Active une rafale de vent"""
        if time.time() - self.last_wind_change < 1.5: 
            return
        
        self.wind_active = True
        if strength is not None:
            self.wind_strength = strength
        else:
            self.wind_strength = random.uniform(0.2, 1.0) 
        self.wind_direction = -1 
        self.last_wind_change = time.time()
        
        print(f"Vent activé! Force: {self.wind_strength}, Direction: {self.wind_direction}")
        
        # Déclenche un QTE après 0.5 seconde
        arcade.schedule(self.trigger_wind_qte, 0.5)

    def trigger_wind_qte(self, delta_time):
        """Déclenche un QTE de vent"""
        arcade.unschedule(self.trigger_wind_qte)
        if time.time() - self.last_qte_time < self.qte_cooldown:
            return
        
        self.qte_active = True
        self.qte_timer = 0
        self.last_qte_time = time.time()


    def spawn_falling_obstacle(self):
        """Fait tomber un obstacle (ajoute à la SpriteList obstacles)"""
        from models.obstacle import FallingObstacle
        obstacle = FallingObstacle(platforms=self.platforms)
        obstacle.center_x = random.randint(200, 800)
        obstacle.center_y = 600
        self.obstacles.append(obstacle)

    def spawn_falling_obstacle_cyclic(self, delta_time):
        """Fait tomber un obstacle à intervalle régulier (cyclique)"""
        self.spawn_falling_obstacle()

    def update(self, delta_time):
        """Mise à jour du niveau"""
        current_time = time.time()

        # === GESTION DU VENT ===
        # Vent constant toujours actif (direction inchangée sauf lors d'une rafale)
        # Rafale occasionnelle
        if not self.wind_active and random.random() < 0.02:  # 2% de chance par frame
            self.activate_wind()

        if self.wind_active and current_time - self.last_wind_change > self.wind_duration:
            self.wind_active = False
            self.wind_strength = 0

        # === GESTION DES QTE ===
        if self.qte_active:
            self.qte_timer += delta_time
            if self.qte_timer >= self.qte_duration:
                # QTE échoué
                self.qte_active = False
                self.wind_fail()

        # === SPAWN DE ROCHERS ===
        if random.random() < 0.005:  # 0.5% de chance par frame
            self.spawn_falling_rock()

        # === MISE À JOUR DES OBSTACLES ===
        self.obstacles.update()
        for obstacle in self.obstacles[:]:
            if obstacle.center_y < -50:
                obstacle.remove_from_sprite_lists()

        # === CHECK FIN DE NIVEAU ===
        if hasattr(self, 'game_manager') and hasattr(self.game_manager, 'player'):
            self.check_end_trigger(self.game_manager.player)

    def draw_wind_effects(self, camera_x):
        """Dessine les effets visuels du vent"""
        if not self.wind_active:
            return
        
        # Lignes de vent plus visibles
        wind_lines = 15
        for i in range(wind_lines):
            start_x = camera_x + 50 + i * 40
            start_y = 150 + random.randint(-30, 30)
            end_x = start_x + self.wind_direction * 80
            end_y = start_y + random.randint(-15, 15)
            
            # Couleur selon la force du vent
            if self.wind_strength > 1.5:
                color = arcade.color.RED
                width = 3
            elif self.wind_strength > 1.0:
                color = arcade.color.YELLOW
                width = 2
            else:
                color = arcade.color.WHITE
                width = 2
            
            arcade.draw_line(
                start_x, start_y, end_x, end_y,
                color, width
            )
        
        # Indicateur de direction du vent
        indicator_x = camera_x + 50
        indicator_y = 100
        arcade.draw_text(
            f"VENT: {self.wind_direction * self.wind_strength:.1f}",
            indicator_x, indicator_y,
            arcade.color.RED, 16
        )

    def draw_qte_indicator(self, camera_x):
        """Dessine l'indicateur de QTE"""
        if not self.qte_active:
            return
        
        # Cercle pulsant
        pulse = (time.time() * 5) % 1.0
        size = 50 + pulse * 20
        
        from views.mountain_view import SCREEN_WIDTH, SCREEN_HEIGHT
        arcade.draw_circle_outline(
            camera_x + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            size, arcade.color.RED, 4
        )
        
        # Texte d'instruction
        key_name = "E" if self.qte_required_key == arcade.key.E else "?"
        arcade.draw_text(
            f"APPUYEZ SUR {key_name} !",
            camera_x + SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80,
            arcade.color.RED, 24, anchor_x="center"
        )

    def draw_obstacles(self, camera_x):
        """Dessine les obstacles spécifiques au niveau"""
        
        # Dessine les obstacles qui tombent
        self.obstacles.draw()

    def handle_qte(self, key):
        """Gère les QTE de vent"""
        if not self.qte_active:
            return False
        
        if key == self.qte_required_key:
            self.qte_active = False
            self.wind_success()
            return True
        return False
    
    def force_wind_test(self, delta_time):
        """Force l'activation du vent pour les tests"""
        arcade.unschedule(self.force_wind_test)
        if not self.wind_active:
            self.activate_wind()
