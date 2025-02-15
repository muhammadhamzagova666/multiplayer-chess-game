# Programming Language: Python
# Project Type: Multiplayer Chess Game
# Key Functionalities: Managing user preferences, saving/loading configuration, and displaying the preferences menu.
# Target Users: Developers maintaining or extending the Chess application.
# Code Style: PEP8 with Google-style docstrings and inline comments

'''
This file is a part of the Chess application.
It manages the preferences menu, which is launched from the main menu,
and includes functions to persist and retrieve user preferences.
'''

import os.path
import pygame
from tools.loader import PREF, BACK  # Reference to [tools/loader.py](Source/tools/loader.py)
from tools.utils import rounded_rect  # Reference to [tools/utils.py](Source/tools/utils.py)

# List of valid preference keys.
KEYS = ["sounds", "flip", "slideshow", "show_moves", "allow_undo", "show_clock"]

# Default preference values.
DEFAULTPREFS = {
    "sounds": True,
    "flip": False,
    "slideshow": True,
    "show_moves": True,
    "allow_undo": True,
    "show_clock": False
}


def save(load):
    """Save user preferences to a text file.

    Opens (or creates) the preferences file and writes each key-value pair
    in the format 'key = value' for later retrieval.

    Args:
        load (dict): The current user preferences to be saved.
    """
    with open(os.path.join("res", "preferences.txt"), "w") as f:
        for key, val in load.items():
            # Write a single preference setting and move to a new line.
            f.write(key + " = " + str(val) + '\n')


def load():
    """Load user preferences from a text file.

    Reads the preferences file and converts string boolean values into actual booleans.
    If the file does not exist, it creates an empty file. Any unknown keys are filtered
    out and missing keys are assigned their default values.

    Returns:
        dict: A dictionary containing validated user preferences.
    """
    path = os.path.join("res", "preferences.txt")
    if not os.path.exists(path):
        # Create the file if it does not exist.
        open(path, "w").close()
    
    with open(path, "r") as f:
        mydict = {}
        for line in f.read().splitlines():
            # Split each line into key and value.
            lsplit = line.split("=")
            if len(lsplit) == 2:
                # Normalize and convert the value.
                val = lsplit[1].strip().lower()
                if val == "true":
                    mydict[lsplit[0].strip()] = True
                elif val == "false":
                    mydict[lsplit[0].strip()] = False

        # Remove any keys that are not defined in KEYS.
        for key in list(mydict.keys()):
            if key not in KEYS:
                mydict.pop(key)
        
        # Ensure all keys have a value by assigning defaults if necessary.
        for key in KEYS:
            if key not in mydict:
                mydict[key] = DEFAULTPREFS[key]
        return mydict


def prompt(win):
    """Display a confirmation prompt when the user attempts to quit.

    Renders a prompt dialog with YES and NO options and waits for the user
    to click one of them. Returns True if the user confirms quitting, else False.

    Args:
        win (pygame.Surface): The display surface on which to render the prompt.

    Returns:
        bool: True if the user confirms action, False otherwise.
    """
    # Draw prompt area using a rounded rectangle.
    rounded_rect(win, (255, 255, 255), (110, 160, 280, 130), 4, 4)
    
    # Display the prompt messages.
    win.blit(PREF.PROMPT[0], (130, 165))
    win.blit(PREF.PROMPT[1], (130, 190))
    
    # Display YES and NO buttons.
    win.blit(PREF.YES, (145, 240))
    win.blit(PREF.NO, (305, 240))
    pygame.draw.rect(win, (255, 255, 255), (140, 240, 60, 28), 2)
    pygame.draw.rect(win, (255, 255, 255), (300, 240, 45, 28), 2)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the vertical button area.
                if 240 < event.pos[1] < 270:
                    # Determine which button was clicked.
                    if 140 < event.pos[0] < 200:
                        return True  # User confirmed (YES)
                    elif 300 < event.pos[0] < 350:
                        return False  # User declined (NO)


def showScreen(win, prefs):
    """Render the complete preferences menu screen.

    Draws the header, preference options, tooltips, and buttons on the display surface.
    Provides visual cues and interactive areas for each of the user preferences.

    Args:
        win (pygame.Surface): The primary display surface.
        prefs (dict): The current user preferences to be displayed.
    """
    # Fill the background with black.
    win.fill((0, 0, 0))
    
    # Draw header and content areas using rounded rectangles.
    rounded_rect(win, (255, 255, 255), (70, 10, 350, 70), 20, 4)
    rounded_rect(win, (255, 255, 255), (10, 85, 480, 360), 12, 4)
    
    # Display back button and header title.
    win.blit(BACK, (460, 0))
    win.blit(PREF.HEAD, (110, 15))
    
    # Draw tip area at the bottom.
    rounded_rect(win, (255, 255, 255), (10, 450, 310, 40), 10, 3)
    win.blit(PREF.TIP, (20, 450))
    win.blit(PREF.TIP2, (55, 467))
    
    # Render labels for each preference option.
    win.blit(PREF.SOUNDS, (90, 90))
    win.blit(PREF.FLIP, (25, 150))
    win.blit(PREF.SLIDESHOW, (40, 210))
    win.blit(PREF.MOVE, (100, 270))
    win.blit(PREF.UNDO, (25, 330))
    win.blit(PREF.CLOCK, (25, 390))
    
    # Render the current state (True/False) for each preference key.
    for i in range(6):
        # Colon serves as a visual separator.
        win.blit(PREF.COLON, (225, 90 + (i * 60)))
        # Highlight the selection based on the Boolean value.
        if prefs[KEYS[i]]:
            rounded_rect(win, (255, 255, 255), (249, 92 + (60 * i), 80, 40), 8, 2)
        else:
            rounded_rect(win, (255, 255, 255), (359, 92 + (60 * i), 90, 40), 8, 2)
        # Render the boolean text labels.
        win.blit(PREF.TRUE, (250, 90 + (i * 60)))
        win.blit(PREF.FALSE, (360, 90 + (i * 60)))
    
    # Draw the save button area.
    rounded_rect(win, (255, 255, 255), (350, 452, 85, 40), 10, 2)
    win.blit(PREF.BSAVE, (350, 450))
    
    # Display helpful tooltips based on current mouse position.
    x, y = pygame.mouse.get_pos()
    if 100 < x < 220 and 90 < y < 130:
        pygame.draw.rect(win, (0, 0, 0), (30, 90, 195, 40))
        win.blit(PREF.SOUNDS_H[0], (45, 90))
        win.blit(PREF.SOUNDS_H[1], (80, 110))
    if 25 < x < 220 and 150 < y < 190:
        pygame.draw.rect(win, (0, 0, 0), (15, 150, 210, 50))
        win.blit(PREF.FLIP_H[0], (50, 150))
        win.blit(PREF.FLIP_H[1], (70, 170))
    if 40 < x < 220 and 210 < y < 250:
        pygame.draw.rect(win, (0, 0, 0), (15, 210, 210, 40))
        win.blit(PREF.SLIDESHOW_H[0], (40, 210))
        win.blit(PREF.SLIDESHOW_H[1], (30, 230))
    if 100 < x < 220 and 270 < y < 310:
        pygame.draw.rect(win, (0, 0, 0), (15, 270, 210, 40))
        win.blit(PREF.MOVE_H[0], (35, 270))
        win.blit(PREF.MOVE_H[1], (25, 290))
    if 25 < x < 220 and 330 < y < 370:
        pygame.draw.rect(win, (0, 0, 0), (15, 330, 210, 40))
        win.blit(PREF.UNDO_H[0], (60, 330))
        win.blit(PREF.UNDO_H[1], (85, 350))
    if 25 < x < 220 and 390 < y < 430:
        pygame.draw.rect(win, (0, 0, 0), (15, 390, 210, 40))
        win.blit(PREF.CLOCK_H[0], (50, 390))
        win.blit(PREF.CLOCK_H[1], (40, 410))


def main(win):
    """Run the main preferences menu loop.

    Loads user preferences, displays the preferences screen,
    handles user interactions, and saves changes when confirmed.

    Args:
        win (pygame.Surface): The display window surface.

    Returns:
        int: Returns an integer as an exit code. Returning 0 indicates quitting,
        while 1 indicates returning to the main menu.
    """
    prefs = load()
    clock = pygame.time.Clock()
    while True:
        clock.tick(24)  # Maintain a steady 24 FPS for smooth UI updates.
        showScreen(win, prefs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT and prompt(win):
                return 0  # Exit the application.
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Detect if the user clicks the BACK button.
                if 460 < x < 500 and 0 < y < 50 and prompt(win):
                    return 1  # Return to the main menu.
                
                # Save the preferences when save button is clicked.
                if 350 < x < 425 and 450 < y < 490:
                    save(prefs)
                    return 1
                
                # Process toggle events for each preference option.
                for i in range(6):
                    if 90 + i * 60 < y < 130 + i * 60:
                        if 250 < x < 330:
                            prefs[KEYS[i]] = True
                        if 360 < x < 430:
                            prefs[KEYS[i]] = False
        pygame.display.update()