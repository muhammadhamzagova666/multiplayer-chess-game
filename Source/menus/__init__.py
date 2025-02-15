# Programming Language: Python
# Project Type: Multiplayer Chess Game
# Key Functionalities: Menu management for online connectivity, user preferences, and timer configuration.
# Target Users: Developers maintaining or extending the Chess application.
# Code Style: PEP8 with Google-style docstrings and inline comments

"""
Menus Package Initialization

This module aggregates the main functions from various menu submodules. It allows
the main application to access the following menu functionalities directly:
    - Online Menu: Handles online connectivity and chat. See [menus.online.main](Source/menus/online.py)
    - Preferences Menu: Manages user settings and configuration. See [menus.pref.main](Source/menus/pref.py)
    - Timer Menu: Configures the in-game timer for multiplayer matches. See [menus.timer.main](Source/menus/timer.py)

Importing this package provides a convenient interface to launch these menus.
"""

from menus.online import main as onlinemenu
from menus.pref import main as prefmenu
from menus.timer import main as timermenu