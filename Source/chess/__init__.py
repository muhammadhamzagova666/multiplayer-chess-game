'''
This file is a part of the Chess application.
It provides shorthand imports for the multiplayer and online modules, allowing other
parts of the application to easily import and invoke their main functions.

Modules referenced here:
    - [chess.multiplayer.main](Source/chess/multiplayer.py): Handles local multiplayer gameplay.
    - [chess.online.main](Source/chess/online.py): Manages online gameplay and networking.
'''

# Import the main functions from the multiplayer and online modules for easier access.
from chess.multiplayer import main as multiplayer
from chess.online import main as online