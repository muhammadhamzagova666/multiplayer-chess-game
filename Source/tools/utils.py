# Programming Language: Python
# Project Type: Multiplayer Chess Game
# Key Functionalities: General purpose utilities including drawing functions and performance measurement.
# Target Users: Developers maintaining and extending the Chess application.
# Code Style: PEP8 with Google-style docstrings

"""
This module provides a set of utility functions for the Chess application. 
These utilities include graphics functions for drawing rounded rectangles using Pygame 
and a decorator for simple performance measurement of functions.
"""

import time

import pygame
import pygame.gfxdraw

def rounded_rect(surf, color, rect, radius=10, border=2, incolor=(0, 0, 0)):
    """
    Draw a rounded rectangle with an optional border on a given surface.

    This function first draws a filled rounded rectangle in the outer color,
    then draws a smaller rounded rectangle inside using a different color to create
    a border effect. This is particularly useful for stylized UI elements in the game.

    Args:
        surf (pygame.Surface): The surface to draw on.
        color (tuple): The color (R, G, B) of the border.
        rect (tuple): The (x, y, width, height) coordinates for the rectangle.
        radius (int): The radius of the rounded corners.
        border (int): The border thickness.
        incolor (tuple): The inner fill color (R, G, B).
    """
    # Only draw if the rectangle is large enough to accommodate the rounded corners and border.
    if min(rect[2], rect[3]) > 2 * (radius + border):
        # Draw the outer rounded rectangle.
        _filled_rounded_rect(surf, color, rect, radius)
        # Adjust rect size to create inner rectangle for border effect.
        inner_rect = (
            rect[0] + border, 
            rect[1] + border,
            rect[2] - 2 * border, 
            rect[3] - 2 * border
        )
        # Draw the inner rounded rectangle.
        _filled_rounded_rect(surf, incolor, inner_rect, radius)

def _filled_rounded_rect(surf, color, rect, r):
    """
    Draw a solid rounded rectangle on a given surface.

    The function creates smooth rounded corners by drawing filled circles at the corners,
    and then fills in the central rectangular area. This breakdown ensures that the drawing
    is both efficient and visually appealing.

    Args:
        surf (pygame.Surface): The surface to draw on.
        color (tuple): The color (R, G, B) to fill with.
        rect (tuple): The rectangle (x, y, width, height) representing the area.
        r (int): The radius for the rounded corners.
    """
    # Draw circles at each corner to achieve the rounded effect.
    for x, y in [
            (rect[0] + r, rect[1] + r),
            (rect[0] + rect[2] - r - 1, rect[1] + r),
            (rect[0] + r, rect[1] + rect[3] - r - 1),
            (rect[0] + rect[2] - r - 1, rect[1] + rect[3] - r - 1)
    ]:
        # Anti-aliased circle for smooth edges.
        pygame.gfxdraw.aacircle(surf, x, y, r, color)
        pygame.gfxdraw.filled_circle(surf, x, y, r, color)
    
    # Draw central rectangles to cover the remaining areas between corner circles.
    pygame.draw.rect(surf, color, (rect[0] + r, rect[1], rect[2] - 2 * r, rect[3]))
    pygame.draw.rect(surf, color, (rect[0], rect[1] + r, rect[2], rect[3] - 2 * r))

def timeit(func):
    """
    Decorator to measure and print the execution time of a function.

    This decorator is useful during testing and debugging to quickly assess 
    the performance of code segments without altering their logic.

    Args:
        func (function): The function to be measured.

    Returns:
        function: A wrapped version of the original function that prints its execution time.
    """
    def inner(*args, **kwargs):
        start = time.perf_counter()
        ret = func(*args, **kwargs)
        end = time.perf_counter()
        print("Time:", round((end - start) * 1000, 4), "ms")
        return ret
    return inner