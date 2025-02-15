# Programming Language: Python
# Project Type: Multiplayer Chess Game
# Key Functionalities: Sound management including playing click, move, start, drag, and background sounds.
# Target Users: Developers maintaining or extending the Chess application
# Code Style: PEP8 with Google-style docstrings

"""
This module handles all sound-related functionalities for the Chess application.

It initializes the Pygame mixer and loads various sound effects used throughout the game.
Functions and classes in this module check the availability of sound support before attempting
to play any audio, ensuring graceful fallback if sound initialization fails.
"""

import os.path
import time

try:
    import pygame.mixer
    pygame.mixer.init()
    # SUCCESS flag indicates whether the mixer was successfully initialized
    SUCCESS = pygame.mixer.get_init() is not None

except (ImportError, RuntimeError):
    SUCCESS = False

if SUCCESS:
    # Load sound effects with appropriate file paths
    click = pygame.mixer.Sound(os.path.join("res", "sounds", "click.ogg"))
    move = pygame.mixer.Sound(os.path.join("res", "sounds", "move.ogg"))
    start = pygame.mixer.Sound(os.path.join("res", "sounds", "start.ogg"))
    drag = pygame.mixer.Sound(os.path.join("res", "sounds", "drag.ogg"))
    background = pygame.mixer.Sound(os.path.join("res", "sounds", "background.ogg"))

class Music:
    """Class to manage background music playback.

    Attributes:
        playing (bool): Indicates whether background music is currently playing.
    """
    def __init__(self):
        """Initialize the Music object with music stopped."""
        self.playing = False

    def play(self, load):
        """Start playing the background music on a continuous loop if sound is enabled.

        Args:
            load (dict): Dictionary containing user preferences. Expects a 'sounds' key.
        """
        if SUCCESS and load.get("sounds"):
            background.play(-1)  # -1 flag loops the sound indefinitely
            self.playing = True

    def stop(self):
        """Stop the background music and update the playing state."""
        if SUCCESS:
            background.stop()
        self.playing = False

    def is_playing(self):
        """Check whether the background music is currently playing.

        Returns:
            bool: True if music is playing, False otherwise.
        """
        return self.playing

def play_click(load):
    """Play the click sound effect if sound is enabled.

    Args:
        load (dict): Dictionary containing user preferences.
    """
    if SUCCESS and load.get("sounds"):
        click.play()
        time.sleep(0.1)  # Short delay to ensure the sound effect is audible

def play_start(load):
    """Play the start sound effect if sound is enabled.

    Args:
        load (dict): Dictionary containing user preferences.
    """
    if SUCCESS and load.get("sounds"):
        start.play()

def play_move(load):
    """Play the move sound effect if sound is enabled.

    Args:
        load (dict): Dictionary containing user preferences.
    """
    if SUCCESS and load.get("sounds"):
        move.play()
        time.sleep(0.1)  # Delay for better synchronization with move animations

def play_drag(load):
    """Play the drag sound effect if sound is enabled.

    Args:
        load (dict): Dictionary containing user preferences.
    """
    if SUCCESS and load.get("sounds"):
        drag.play()

# The following cleanup call quits the mixer if initialization was successful.
# Note: Calling pygame.mixer.quit() here will unload sound resources immediately.
# Ensure this is intended for your application's lifecycle, as it might affect subsequent sound playback.
if SUCCESS:
    pygame.mixer.quit()