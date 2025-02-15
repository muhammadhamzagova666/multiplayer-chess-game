# Programming Language: Python
# Project Type: Multiplayer Chess Game
# Key Functionalities: Managing the timer configuration menu for multiplayer chess.
# Target Users: Developers maintaining or extending the Chess application.
# Code Style: PEP8 with Google-style docstrings and inline comments

"""
Module for managing the timer menu used to configure the chess timer.

This module provides functions to display interactive timer options,
handle mouse events for user input, and return the chosen timer settings.
"""

import pygame

from tools.loader import TIMER, BACK, putLargeNum
from tools.utils import rounded_rect

def start(win, load):
    """Display the initial prompt and capture the user's decision regarding timer activation.

    Uses a rounded rectangle to highlight the prompt and draws YES/NO buttons.

    Args:
        win (pygame.Surface): The primary display surface.
        load (dict): Dictionary containing user preferences.

    Returns:
        tuple or None: Returns a tuple indicating the user's choice for timer settings
        or None if the user cancels. A return of (-1, (0, 0)) signals that the clock should
        be displayed if enabled in preferences.
    """
    # Draw a rounded rectangle for the prompt area.
    rounded_rect(win, (255, 255, 255), (120, 180, 260, 100), 10, 4)
    win.blit(TIMER.PROMPT, (150, 190))
    win.blit(TIMER.YES, (145, 240))
    win.blit(TIMER.NO, (305, 240))
    # Draw button outlines to clearly indicate clickable areas.
    pygame.draw.rect(win, (255, 255, 255), (140, 240, 60, 28), 2)
    pygame.draw.rect(win, (255, 255, 255), (300, 240, 45, 28), 2)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the click is within the vertical bounds for button responses.
                if 240 < event.pos[1] < 270:
                    # Return None if YES is clicked.
                    if 140 < event.pos[0] < 200:
                        return None
                    # Allow clock display if NO is clicked and the 'show_clock' preference is enabled.
                    elif 300 < event.pos[0] < 350:
                        if load["show_clock"]:
                            return -1, (0, 0)
                        else:
                            return None, None

def showScreen(win, sel, sel2):
    """Render the timer settings screen with selectable options.

    Displays header, text, and interactive timer option boxes while highlighting the
    currently selected options.

    Args:
        win (pygame.Surface): The display surface.
        sel (int): Index corresponding to the first row selection (timer duration).
        sel2 (int): Index corresponding to the second row selection (alternate timer duration).
    """
    # Clear screen and set background to black.
    win.fill((0, 0, 0))
    
    # Draw header section with a rounded rectangle.
    rounded_rect(win, (255, 255, 255), (70, 5, 340, 60), 15, 4)
    win.blit(TIMER.HEAD, (100, 7))
    win.blit(BACK, (460, 0))

    # Draw the main content area.
    rounded_rect(win, (255, 255, 255), (10, 70, 480, 420), 12, 4)
    
    # Render each line of instruction text with proper vertical spacing.
    for cnt, i in enumerate(TIMER.TEXT):
        y = 75 + cnt * 18
        win.blit(i, (20, y))
        
    # Draw timer option boxes for the first row.
    for i in range(6):
        pygame.draw.rect(win, (255, 255, 255), (110 + 40*i, 200, 28, 23), 3)
        
    # Draw timer option boxes for the second row.
    for i in range(5):
        pygame.draw.rect(win, (255, 255, 255), (110 + 40*i, 290, 28, 23), 3)
        
    # Highlight the current selections.
    pygame.draw.rect(win, (50, 100, 150), (110 + 40*sel, 200, 28, 23), 3) 
    pygame.draw.rect(win, (50, 100, 150), (110 + 40*sel2, 290, 28, 23), 3)
        
    # Draw the confirmation button.
    pygame.draw.rect(win, (255, 255, 255), (300, 416, 50, 23), 3)    
    pygame.display.update()

def main(win, load):
    """Main timer configuration function invoked from the main menu.

    Initializes the timer menu, captures the user's selections, and returns the chosen
    timer values along with any required display option key.

    Args:
        win (pygame.Surface): Display window surface.
        load (dict): User configuration and preference dictionary.

    Returns:
        tuple: A tuple containing the selection index for the timer settings and a tuple
        of timer durations in milliseconds.
    """
    # Start with the initial prompt screen.
    ret = start(win, load)
    if ret is not None:
        return ret

    sel = sel2 = 0
    clock = pygame.time.Clock()

    # Main event loop for managing timer option selection.
    while True:
        clock.tick(24)  # Limit the loop to 24 FPS for smooth interaction.
        showScreen(win, sel, sel2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0  # Exit if the Pygame QUIT event is triggered.
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check if the user clicked the BACK button.
                if 460 < x < 500 and 0 < y < 50:
                    return 1
                
                # When the confirmation button is clicked, return the selected timer values.
                if 300 < x < 350 and 416 < y < 439:
                    # Mapping selections to corresponding durations (in milliseconds).
                    if sel == 0:
                        temp = (30 * 60 * 1000,) * 2
                    elif sel == 1:
                        temp = (15 * 60 * 1000,) * 2
                    elif sel == 2:
                        temp = (10 * 60 * 1000,) * 2
                    elif sel == 3:
                        temp = (5 * 60 * 1000,) * 2
                    elif sel == 4:
                        temp = (3 * 60 * 1000,) * 2
                    elif sel == 5:
                        temp = (1 * 60 * 1000,) * 2
                    return sel2, temp
                
                # Update the first-row selection based on mouse x-coordinate.
                for i in range(6):
                    if 110 + 40*i < x < 138 + 40*i and 200 < y < 223:
                        sel = i
                        break
                        
                # Update the second-row selection based on mouse x-coordinate.
                for i in range(5):
                    if 110 + 40*i < x < 138 + 40*i and 290 < y < 313:
                        sel2 = i
                        break