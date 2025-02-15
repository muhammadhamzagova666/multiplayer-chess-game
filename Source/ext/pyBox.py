# Programming Language: Python
# Project Type: Multiplayer Chess Game
# Key Functionalities: Provides a high-level interactive TextBox in Pygame for user text input.
# Target Users: Developers maintaining or extending the Chess application.
# Code Style: PEP8 with Google-style docstrings and inline comments

"""
This file is a part of the Chess application.
This module provides a custom TextBox class for interactive text input using Pygame,
supporting both keyboard and mouse events. The TextBox handles text rendering, cursor
movement, and basic text editing functionality.

Note:
    This module is a work-in-progress and may evolve further.
"""

import os
import pygame

class TextBox:
    """A high-level interactive text box widget implemented using Pygame.

    The TextBox supports keyboard and mouse interaction, allowing text insertion,
    deletion, and cursor movement. It maintains an internal clock for blinking
    cursor visibility.
    """

    def __init__(self, font, color, rect, text=""):
        """Initializes the TextBox widget.

        Args:
            font (str): The font path or name to be used for text rendering.
            color (tuple): The RGB color tuple for the text.
            rect (tuple): The rectangle defining the position and size (x, y, width, height).
            text (str, optional): Initial text content. Defaults to "".
        """
        # Ensure the font exists; otherwise, try to match built-in system font.
        if not os.path.isfile(font):
            font = pygame.font.match_font(font)
            
        # Set up the font with font size adjusted to the TextBox height.
        self.font = pygame.font.Font(font, rect[3] - 8)
        self.COLOR = color
        self.RECT = rect
        self.text = text

        # Cursor and selection management.
        self.cursor = 0  # Current cursor position.
        self.startpos = 0  # Starting horizontal offset for scrolling text.
        self.active = False  # Determines if the TextBox is in focus.
        self.mouseheld = False  # Tracks if mouse button is held down.
        self.shiftheld = False  # Tracks shift key status for text selection.
        self.selected = None  # Holds selected text indices as a two-element list.

        # Setup timer variables for blinking cursor effect.
        self.clock = pygame.time.Clock()
        self.time = 0
        self.visible = True  # Visibility of the blinking cursor.
        self.SWITCHTIME = 600  # Milliseconds after which the cursor toggles visibility.
        
        # Create a surface for drawing text inside the TextBox.
        self.surf = pygame.Surface(rect[2:])

    def renderText(self, indices=None):
        """Render a portion of the text using the configured font and color.

        Args:
            indices (list, optional): Start and end indices to define the text slice.
                                      Defaults to the entire text.

        Returns:
            pygame.Surface: Surface containing rendered text.
        """
        if indices is None:
            indices = [0, len(self.text)]
        # Render only the selected substring.
        return self.font.render(self.text[indices[0]:indices[1]], True, self.COLOR)
        
    def insert(self, index, text):
        """Insert text at the specified cursor index.

        Args:
            index (int): Position where the text should be inserted.
            text (str): The text string to insert.
        """
        # Insert text and preserve the existing substring.
        self.text = self.text[:index] + text + self.text[index:]
    
    def remove(self, indices):
        """Remove characters specified by indices.

        If a single index is provided (as int), assume deletion of one character.
        If a list is provided, delete the substring defined by that range.

        Args:
            indices (int or list): Index or range to remove from the text.
        """
        # Normalize indices if a single integer is provided.
        if isinstance(indices, int):
            indices = [indices, indices + 1]
        # Remove the specified substring.
        self.text = self.text[:indices[0]] + self.text[indices[1]:]
    
    def getLen(self, indices=None):
        """Calculate the rendered width of the specified text segment.

        Args:
            indices (list, optional): Start and end indices of the text segment.
                                      Defaults to the entire text.

        Returns:
            int: The width in pixels of the rendered text.
        """
        # Leverage renderText to get accurate width measurement.
        return self.renderText(indices).get_width()
           
    def push(self, event):
        """Handle incoming Pygame events for this TextBox.

        Processes mouse events for activation and keyboard events for text editing,
        cursor movement, and selection.

        Args:
            event (pygame.event.Event): The Pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouseheld = True
            x, y = event.pos
            # Check if mouse click falls within the TextBox boundaries.
            if (self.RECT[0] < x < (self.RECT[0] + self.RECT[2]) and
                self.RECT[1] < y < (self.RECT[1] + self.RECT[3])):
                self.active = True
            else:
                # Deactivate TextBox if clicked outside.
                self.active = False
                self.selected = None
            
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouseheld = False
            
        elif event.type == pygame.KEYUP:
            # Reset shift state when shift key is released.
            if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                self.shiftheld = False
            
        elif event.type == pygame.KEYDOWN and self.active:
            # Ignore certain keys that are reserved for navigation.
            if event.key in [pygame.K_TAB, pygame.K_ESCAPE, pygame.K_KP_ENTER]:
                pass
            
            elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                self.shiftheld = True
            
            elif event.key == pygame.K_BACKSPACE:
                # Handle backspace: remove character before cursor if no selection.
                if self.selected is None:
                    if self.cursor > 0:
                        self.cursor -= 1
                        self.remove(self.cursor)
                else:
                    # Remove selected text if any.
                    self.cursor = self.selected[0]
                    self.remove(self.selected)
                    self.selected = None
                    
            elif event.key == pygame.K_DELETE:
                # Handle deletion: remove character at cursor if no selection.
                if self.selected is None:
                    if self.cursor < len(self.text):
                        self.remove(self.cursor)
                else:
                    # Remove selected text and reset selection.
                    self.cursor = self.selected[0]
                    self.remove(self.selected)
                    self.selected = None
                        
            elif event.key == pygame.K_RIGHT:
                # Move cursor right, update selection if shift is held.
                if self.cursor < len(self.text):
                    if self.shiftheld:
                        if self.selected is None:
                            self.selected = [self.cursor, self.cursor + 1]
                        elif self.cursor == self.selected[1]:
                            self.selected[1] += 1
                        elif self.cursor == self.selected[0]:
                            self.selected[0] += 1
                        # Clear selection if it collapses.
                        if self.selected[0] == self.selected[1]:
                            self.selected = None
                    else:
                        self.selected = None
                    self.cursor += 1

            elif event.key == pygame.K_LEFT:
                # Move cursor left, update selection if shift is held.
                if self.cursor > 0:
                    self.cursor -= 1
                    if self.shiftheld:
                        if self.selected is None:
                            self.selected = [self.cursor, self.cursor + 1]
                        elif self.cursor == self.selected[0] - 1:
                            self.selected[0] -= 1
                        elif self.cursor == self.selected[1] - 1:
                            self.selected[1] -= 1
                        if self.selected[0] == self.selected[1]:
                            self.selected = None
                    else:
                        self.selected = None
                        
            elif event.key == pygame.K_END:
                # Move cursor to the end of the text, optionally extending selection.
                if self.cursor < len(self.text):
                    if self.shiftheld:
                        if self.selected is None:
                            self.selected = [self.cursor, len(self.text)]
                        else:
                            self.selected[1] = len(self.text)
                    else:
                        self.selected = None
                    self.cursor = len(self.text)

            elif event.key == pygame.K_HOME:
                # Move cursor to the beginning of the text, optionally extending selection.
                if self.cursor > 0:
                    if self.shiftheld:
                        if self.selected is None:
                            self.selected = [0, self.cursor]
                        else:
                            self.selected[0] = 0
                    else:
                        self.selected = None
                    self.cursor = 0
                
            elif event.key == pygame.K_RETURN:
                # Deactivate the TextBox on Enter.
                self.active = False
                
            elif len(event.unicode) == 1:
                # Insert character: if text is selected, replace selection.
                if self.selected is None:
                    self.insert(self.cursor, event.unicode)
                    self.cursor += 1
                else:
                    self.remove(self.selected)
                    self.cursor = self.selected[0]
                    self.selected = None
                    self.insert(self.cursor, event.unicode)
                    self.cursor += 1
                        
    def draw(self, win):
        """Draw the TextBox onto the provided surface.

        Handles blinking of the cursor, drawing the text, and ensuring that overflowing
        text scrolls horizontally.

        Args:
            win (pygame.Surface): The display surface where the TextBox is rendered.
        """
        # Update timer for blinking cursor.
        self.time += self.clock.get_time()
        if self.time >= self.SWITCHTIME:
            self.time %= self.SWITCHTIME
            self.visible = not self.visible
        
        # Clear the internal surface and draw a border.
        self.surf.fill((0, 0, 0))
        pygame.draw.rect(self.surf, (255, 255, 255), 
                         (3, 3, self.RECT[2] - 6, self.RECT[3] - 6))
        
        # Determine the pixel position of the cursor.
        cursorpos = self.getLen([0, self.cursor])
        
        # Create a temporary surface to render the text.
        rendered = pygame.Surface((self.getLen() + 2, self.RECT[3] - 8))
        rendered.fill((255, 255, 255))
        
        # If text is selected, draw a highlighted rectangle around the selection.
        if self.selected is not None:
            selrect = (self.getLen([0, self.selected[0]]), 2,
                       self.getLen(self.selected), self.RECT[3] - 12)
            pygame.draw.rect(rendered, (128, 220, 255), selrect)
            
        # Render the text onto the temporary surface.
        rendered.blit(self.renderText(), (0, 0))
        
        if self.active:
            # Draw an active border when the TextBox is focused.
            pygame.draw.rect(self.surf, (0, 0, 255),
                             (2, 2, self.RECT[2] - 5, self.RECT[3] - 5), 2)
            # Only draw the blinking cursor if it is visible.
            if self.visible:
                pygame.draw.line(rendered, (0, 0, 0), (cursorpos, 2),
                                 (cursorpos, self.RECT[3] - 12), 2)
        
        # Scroll text horizontally if necessary.
        if rendered.get_width() > self.RECT[2] - 8:
            if cursorpos < self.startpos + 2:
                self.startpos = cursorpos - 2
            elif cursorpos > self.startpos + self.RECT[2] - 6:
                self.startpos = cursorpos - self.RECT[2] + 6
            else:
                self.surf.blit(rendered, (4 - self.startpos, 4))
        else:
            self.surf.blit(rendered, (4, 4))
            
        # Blit the TextBox surface onto the provided window.
        win.blit(self.surf, self.RECT[:2])
        self.clock.tick()  # Update the clock to manage frame rate.

# Basic sample usage for pyBox module.
if __name__ == "__main__":
    pygame.init()
    # Create a TextBox with a default font ("calibri") for testing purposes.
    box = TextBox("calibri", (0, 0, 0), (30, 0, 150, 35))
    running = True
    win = pygame.display.set_mode((300, 200))
    win.fill((255, 255, 255))
    while running:
        for event in pygame.event.get():
            box.push(event)  # Process all events for the TextBox.
            if event.type == pygame.QUIT:
                running = False
        box.draw(win)
        pygame.display.flip()
    pygame.quit()