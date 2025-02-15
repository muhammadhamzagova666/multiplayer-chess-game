# Programming Language: Python
# Project Type: Multiplayer Chess Game
# Key Functionalities: Managing the online menu, handling user input for online connectivity, and text input through a custom TextBox.
# Target Users: Developers maintaining or extending the Chess application.
# Code Style: PEP8 with Google-style docstrings and inline comments

'''
This file is a part of the Chess application.
It manages the online menu, which is launched when the user clicks
the online button on the main menu.
'''

import pygame
from ext.pyBox import TextBox  # Provides an interactive text input box. [ext/pyBox.py](Source/ext/pyBox.py)
from tools.loader import ONLINEMENU, BACK, FONT  # Reference to graphical resources [tools/loader.py](Source/tools/loader.py)
from tools.utils import rounded_rect  # Utility to draw rounded rectangles [tools/utils.py](Source/tools/utils.py)

def showScreen(win, sel):
    """Render the online menu screen with interactive elements.

    Draws the header, background text, connect button, and selection highlight
    for different online options.

    Args:
        win (pygame.Surface): The display surface.
        sel (int): Index representing the current selection highlight.
    """
    # Set background to black.
    win.fill((0, 0, 0))
    
    # Draw header and main content area with rounded edges.
    rounded_rect(win, (255, 255, 255), (120, 10, 260, 70), 20, 4)
    rounded_rect(win, (255, 255, 255), (20, 90, 460, 400), 14, 4)

    # Render header title and back button.
    win.blit(ONLINEMENU.HEAD, (175, 15))
    win.blit(BACK, (460, 0))
    
    # Render informational text lines sourced from the loader.
    for cnt, line in enumerate(ONLINEMENU.TEXT):
        win.blit(line, (40, 100 + cnt * 18))
    
    # Draw connect button with a rounded rectangle.
    rounded_rect(win, (255, 255, 255), (300, 350, 110, 30), 10, 3)
    win.blit(ONLINEMENU.CONNECT, (300, 350))
    
    # Draw selection highlight rectangle based on user's current option.
    pygame.draw.rect(win, (255, 255, 255), (130 + sel * 160, 460, 40, 20), 3)


def main(win):
    """Main function for the online menu.

    Initializes the online menu, handles text input via a TextBox, and processes
    mouse events to determine if the user navigates back or confirms an online connection.

    Args:
        win (pygame.Surface): The display window surface.

    Returns:
        tuple or int: Returns a tuple (text, selection_flag) if the connect button is pressed,
                      1 when the user clicks the back button, or 0 on quit.
    """
    clock = pygame.time.Clock()
    sel = 0  # Initial selection index.
    
    # Create an interactive text box for entering connection information.
    box = TextBox(FONT, (0, 0, 0), (65, 350, 200, 35))
    
    while True:
        clock.tick(24)  # Limit the loop to 24 FPS for a consistent UI frame rate.
        showScreen(win, sel)
        
        # Draw the text box border for clarity.
        pygame.draw.rect(win, (255, 255, 255), (63, 348, 204, 39))
        box.draw(win)
        
        for event in pygame.event.get():
            box.push(event)  # Forward event to the TextBox for text input handling.
            
            if event.type == pygame.QUIT:
                return 0  # Exit the online menu when quit signal is received.
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check if back button is clicked (located in top-right corner).
                if 460 < x < 500 and 0 < y < 50:
                    return 1
                
                # Update selection based on click coordinates in the option area.
                if 460 < y < 480:
                    if 130 < x < 170:
                        sel = 0
                    if 290 < x < 320:
                        sel = 1
                
                # If connect button area is clicked, return the entered text and selection flag.
                if 300 < x < 410 and 350 < y < 380:
                    return box.text, bool(sel)
                    
        pygame.display.update()