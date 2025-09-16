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

    def start_dialogue(self, dialogues, choices=None, on_choice=None):
        """Lancer un nouveau dialogue. on_choice(index, value) sera appelé si choix."""
        self.dialogues = dialogues
        self.current_index = 0
        self.choices = choices or []
        self.active = True
        self.choice_selected = None
        self.on_choice = on_choice

    def next_line(self):
        """Passe à la ligne suivante ou termine le dialogue"""
        if not self.active:
            return
        self.current_index += 1
        if self.current_index >= len(self.dialogues):
            self.active = False

    def select_choice(self, index):
        """Choix du joueur, si applicable. Appelle le callback si défini."""
        if 0 <= index < len(self.choices):
            self.choice_selected = index
            self.active = False
            value = self.choices[index]
            if self.on_choice:
                self.on_choice(index, value)
                self.on_choice = None
            return value
        return None

    def get_current_line(self):
        """Récupère la ligne en cours"""
        if self.active and self.current_index < len(self.dialogues):
            return self.dialogues[self.current_index]
        return ""

    def is_finished(self):
        """Retourne True si le dialogue est terminé"""
        return not self.active