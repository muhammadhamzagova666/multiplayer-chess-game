# Programming Language: Python# Programming Language: Python
# Project Type: Multiplayer Chess Game
# Key Functionalities: Menu management, game launching, sound handling, display and event loop management
# Target Users: Developers maintaining or extending the Chess application
# Code Style: PEP8, with Google-style docstrings and inline comments

"""
Main module for the Chess application.

This module initializes Pygame, sets up the game window and menu,
and handles the main event loop. It loads user preferences, manages background
animations, and routes user inputs to the multiplayer or online game modules.

Usage:
    Run this file to launch the Chess application.
"""

import sys  
import pygame

import chess
import menus
from tools.loader import MAIN
from tools import sound

# Flush stdout to ensure external programs calling this application
# receive any pending output immediately.
sys.stdout.flush()

# Initialize Pygame and the clock for frame rate control.
pygame.init()
clock = pygame.time.Clock()

# Set up the display window. Use Pygame's SCALED mode if using Pygame 2 or above.
if pygame.version.vernum[0] >= 2:
    win = pygame.display.set_mode((500, 500), pygame.SCALED)
else:
    win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Chess")
pygame.display.set_icon(MAIN.ICON)

# Define rectangle coordinates for the "Multiplayer" and "Online" buttons.
mult = (280, 200, 200, 40)  # Multiplayer button: (x, y, width, height)
onln = (360, 260, 120, 40)  # Online button

def showMain(prefs):
    """
    Render the main menu screen.

    This function updates the background animation if enabled in user preferences,
    displays the heading and version information, and renders the interactive menu buttons.

    Args:
        prefs (dict): Dictionary containing user preferences and settings.
    """
    global cnt, img

    # Display the current background image based on the animation frame.
    win.blit(MAIN.BG[img], (0, 0))

    if prefs["slideshow"]:
        # Increment frame counter to control slideshow timing and opacity
        cnt += 1
        if cnt >= 150:
            # Start fading effect after 5 seconds (150 frames) at approximately 30 fps.
            s = pygame.Surface((500, 500))
            s.set_alpha((cnt - 150) * 4)  # Gradually increase opacity for fade-out.
            s.fill((0, 0, 0))
            win.blit(s, (0, 0))

        if cnt == 210:
            # Reset counter after 7 seconds and update the background image index.
            cnt = 0
            img = 0 if img == 3 else img + 1
    else:
        # If slideshow is disabled, ensure default variables are set.
        cnt = -150
        img = 0

    # Render header and version texts along with decorative lines.
    win.blit(MAIN.HEADING, (80, 20))
    pygame.draw.line(win, (255, 255, 255), (80, 100), (130, 100), 4)
    pygame.draw.line(win, (255, 255, 255), (165, 100), (340, 100), 4)
    win.blit(MAIN.VERSION, (345, 95))

    # Render the "Multiplayer" and "Online" button texts at the specified positions.
    win.blit(MAIN.MULTI, mult[:2])
    win.blit(MAIN.ONLINE, onln[:2])

# Initialize global variables for background animation.
cnt = 0   # Frame counter used for slideshow timing.
img = 0   # Index tracking the current background image.
run = True  # Control variable for the main loop.

# Load player settings from the preferences module.
prefs = menus.pref.load()
print(prefs)   # Print preferences for debugging purposes.

# Start background music based on user preferences.
music = sound.Music()
music.play(prefs)

while run:
    # Maintain the loop at approximately 30 frames per second.
    clock.tick(30)
    showMain(prefs)

    # Get current mouse position for hover effects.
    x, y = pygame.mouse.get_pos()

    # Highlight the Multiplayer button if the cursor is over it.
    if mult[0] < x < sum(mult[::2]) and mult[1] < y < sum(mult[1::2]):
        win.blit(MAIN.MULTI_H, mult[:2])

    # Highlight the Online button if the cursor is over it.
    if onln[0] < x < sum(onln[::2]) and onln[1] < y < sum(onln[1::2]):
        win.blit(MAIN.ONLINE_H, onln[:2])

    # Process all events captured by Pygame.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Terminate the application if the window is closed.
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse click events by determining the clicked button region.
            x, y = event.pos

            if mult[0] < x < sum(mult[::2]) and mult[1] < y < sum(mult[1::2]):
                # When Multiplayer button is clicked, provide immediate feedback and launch the multiplayer menu.
                sound.play_click(prefs)
                ret = menus.timermenu(win, prefs)
                # Handle the return value from the timer menu.
                if ret == 0:
                    run = False
                elif ret != 1:
                    run = chess.multiplayer(win, ret[0], ret[1], prefs)

            elif onln[0] < x < sum(onln[::2]) and onln[1] < y < sum(onln[1::2]):
                # When Online button is clicked, provide immediate feedback and launch the online menu.
                sound.play_click(prefs)
                ret = menus.onlinemenu(win)
                # Process the online menu outcome.
                if ret == 0:
                    run = False
                elif ret != 1:
                    run = chess.online(win, ret[0], prefs, ret[1])

    # Refresh the display after all updates.
    pygame.display.flip()

# Clean up resources after exiting the main loop.
music.stop()
pygame.quit()