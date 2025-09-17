class DialogueManager:
    """
    Gère l'affichage des dialogues et les choix possibles.
    """
    def __init__(self):
        self.active = False
        self.dialogues = []       # Liste des lignes de dialogues
        self.current_index = 0
        self.choices = []         # Liste des choix possibles
        self.choice_selected = None
        self.on_choice = None     # Callback appelé lors d'un choix
        # Nouveau: navigation par curseur pour les choix
        self.cursor_position = 0
        self._showing_choices = False
        self.game_manager = None  # Référence au game manager pour les callbacks

    def start_dialogue(self, dialogues, choices=None, on_choice=None):
        """Lancer un nouveau dialogue. on_choice(index, value) sera appelé si choix."""
        self.dialogues = dialogues
        self.current_index = 0
        self.choices = choices or []
        self.active = True
        self.choice_selected = None
        self.on_choice = on_choice
        self.cursor_position = 0
        self._showing_choices = False

    def next_line(self):
        """Passe à la ligne suivante ou termine le dialogue"""
        if not self.active:
            return
        # Si des choix existent et qu'on est sur la dernière ligne, on passe à l'écran de choix
        if self.choices and self.current_index >= len(self.dialogues) - 1:
            self._showing_choices = True
            return

        self.current_index += 1
        if self.current_index >= len(self.dialogues):
            # Fin du texte: si pas de choix, on termine; sinon on affiche les choix
            if self.choices:
                self._showing_choices = True
            else:
                self.active = False

    def select_choice(self, index):
        """Choix du joueur, si applicable. Appelle le callback si défini."""
        if 0 <= index < len(self.choices):
            self.choice_selected = index
            self.active = False
            self._showing_choices = False
            value = self.choices[index]
            if self.on_choice:
                # Passe la référence au game manager au callback
                if hasattr(self.on_choice, '__self__') and hasattr(self.on_choice.__self__, 'path_choice_callback'):
                    # C'est une méthode d'un niveau, on l'appelle directement
                    self.on_choice(index, value)
                else:
                    # C'est une fonction lambda ou autre, on l'appelle normalement
                    self.on_choice(index, value)
                self.on_choice = None
            return value
        return None

    # --- Navigation par curseur ---
    def move_cursor_left(self):
        if self._showing_choices and self.choices:
            self.cursor_position = (self.cursor_position - 1) % len(self.choices)

    def move_cursor_right(self):
        if self._showing_choices and self.choices:
            self.cursor_position = (self.cursor_position + 1) % len(self.choices)

    def confirm_choice(self):
        if self._showing_choices and 0 <= self.cursor_position < len(self.choices):
            return self.select_choice(self.cursor_position)
        return None

    def get_current_line(self):
        """Récupère la ligne en cours"""
        if self.active and self.current_index < len(self.dialogues):
            return self.dialogues[self.current_index]
        return ""

    def is_finished(self):
        """Retourne True si le dialogue est terminé"""
        return not self.active

    def is_showing_choices(self):
        return self._showing_choices