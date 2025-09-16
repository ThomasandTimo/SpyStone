# Everest - Spectateur (Arcade 3.3.2)

Mini-jeu narratif minimaliste: vous êtes un caillou spectateur, tandis qu'un héros tente l'ascension de l'Everest.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

## Lancer le jeu

```bash
python main.py
```

## Commandes

- Flèche Haut: proposer un conseil (sans effet réel)
- Espace: réussir le QTE (dans le temps imparti)
- R: rejouer après la fin

## Scènes

- début → camp1 → camp2 → sommet

Selon vos QTE, la fin affiche:
- "Le héros atteint le sommet !" (succès au dernier QTE)
- "Le héros abandonne !" (échec/temps écoulé au dernier QTE)
