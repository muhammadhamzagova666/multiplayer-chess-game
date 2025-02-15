"""
This file is a part of the Chess application.
In this file, we define key GUI-related functions to handle drawing the board,
pieces, prompts, and other interactive elements.

For a better understanding of certain assets or variables (e.g., CHESS, BACK),
refer to the [tools.loader.py](tools/loader.py) and the documentation in docs.txt.
"""

import pygame
from tools.loader import CHESS, BACK, putNum, putLargeNum
from tools import sound


def convertPieces(win):
    """Convert piece images to alpha-optimized surfaces for faster rendering.

    Iterates through each piece image in [`CHESS.PIECES`](tools/loader.py)
    and applies convert_alpha for better performance when drawing.
    """
    for i in range(2):
        for key, val in CHESS.PIECES[i].items():
            # Minimizes rendering overhead by using hardware-friendly pixel formats.
            CHESS.PIECES[i][key] = val.convert_alpha(win)


def getChoice(win, side):
    """Display a small menu for the user to select a promotion piece.

    This function shows a row of possible promotion pieces (Queen, Bishop, Rook, Knight)
    for the given side and waits for a mouse click to determine which piece is chosen.

    Args:
        win (pygame.Surface): The window surface where the menu should be drawn.
        side (int): Indicates which side (0 or 1).

    Returns:
        str: A single-character code representing the chosen piece (e.g., "q", "b", "r", "n").
    """
    win.blit(CHESS.CHOOSE, (130, 10))
    win.blit(CHESS.PIECES[side]["q"], (250, 0))
    win.blit(CHESS.PIECES[side]["b"], (300, 0))
    win.blit(CHESS.PIECES[side]["r"], (350, 0))
    win.blit(CHESS.PIECES[side]["n"], (400, 0))
    pygame.display.update((0, 0, 500, 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0 < event.pos[1] < 50:
                    if 250 < event.pos[0] < 300:
                        return "q"
                    elif 300 < event.pos[0] < 350:
                        return "b"
                    elif 350 < event.pos[0] < 400:
                        return "r"
                    elif 400 < event.pos[0] < 450:
                        return "n"


def showTimeOver(win, side):
    """Display a dialog indicating that the current player's time is over.

    A button labeled OK waits for a user click to dismiss the dialog.

    Args:
        win (pygame.Surface): The window surface on which the message is rendered.
        side (int): Indicates which side has run out of time (0 or 1).
    """
    pygame.draw.rect(win, (0, 0, 0), (100, 190, 300, 120))
    pygame.draw.rect(win, (255, 255, 255), (100, 190, 300, 120), 4)

    win.blit(CHESS.TIMEUP[0], (220, 200))
    win.blit(CHESS.TIMEUP[1], (105, 220))
    win.blit(CHESS.TIMEUP[2], (115, 240))

    win.blit(CHESS.OK, (230, 270))
    pygame.draw.rect(win, (255, 255, 255), (225, 270, 50, 30), 2)

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 225 < event.pos[0] < 275 and 270 < event.pos[1] < 300:
                    return


def putClock(win, timer):
    """Render a clock display for each side, showing minutes and seconds.

    Takes a pair of millisecond values in the form [time_side0, time_side1],
    converts them to MM:SS format, and draws them at the bottom of the screen.

    Args:
        win (pygame.Surface): The window surface onto which the clock is drawn.
        timer (list[int] or None): Time values for both sides in milliseconds. If None, nothing is drawn.
    """
    if timer is None:
        return

    m1, s1 = divmod(timer[0] // 1000, 60)
    m2, s2 = divmod(timer[1] // 1000, 60)

    # Display side 0's time.
    putLargeNum(win, format(m1, "02"), (100, 460), False)
    win.blit(CHESS.COL, (130, 460))
    putLargeNum(win, format(s1, "02"), (140, 460), False)

    # Display side 1's time.
    putLargeNum(win, format(m2, "02"), (210, 460), False)
    win.blit(CHESS.COL, (240, 460))
    putLargeNum(win, format(s2, "02"), (250, 460), False)

    # Show small king icons to indicate which side's clock is displayed.
    win.blit(CHESS.PIECES[0]["k"], (50, 450))
    win.blit(CHESS.PIECES[1]["k"], (278, 450))

    pygame.display.update()


def drawBoard(win):
    """Draw the chessboard background and squares.

    Fills the screen with a base color, then draws an 8x8 board with alternating tile colors.

    Args:
        win (pygame.Surface): The window surface where the board is drawn.
    """
    win.fill((100, 200, 200))
    pygame.draw.rect(win, (180, 100, 30), (50, 50, 400, 400))
    for y in range(1, 9):
        for x in range(1, 9):
            if (x + y) % 2 == 0:
                pygame.draw.rect(win, (220, 240, 240), (50 * x, 50 * y, 50, 50))


def drawPieces(win, board, flip):
    """Render all chess pieces onto the board.

    Checks if the board should be flipped for the second player,
    then draws the pieces in their correct positions.

    Args:
        win (pygame.Surface): The window surface onto which pieces are drawn.
        board (list): A 2D data structure representing piece positions for each side.
        flip (bool): If True, invert the board to show from the second player's perspective.
    """
    for side in range(2):
        for x, y, ptype in board[side]:
            if flip:
                x, y = 9 - x, 9 - y
            win.blit(CHESS.PIECES[side][ptype], (x * 50, y * 50))


def prompt(win, msg=None):
    """Display a prompt screen with Yes/No buttons, returning a boolean based on user choice.

    This function is used for confirming actions like quitting a match or discarding unsaved data.

    Args:
        win (pygame.Surface): The window surface where the prompt is rendered.
        msg (int or None, optional): If None, a generic message is shown. If -1 or another value,
                                     specific text or error info is displayed. Defaults to None.

    Returns:
        bool: True if Yes is clicked, False if No is clicked.
    """
    pygame.draw.rect(win, (0, 0, 0), (110, 160, 280, 130))
    pygame.draw.rect(win, (255, 255, 255), (110, 160, 280, 130), 4)

    pygame.draw.rect(win, (255, 255, 255), (120, 160, 260, 60), 2)

    win.blit(CHESS.YES, (145, 240))
    win.blit(CHESS.NO, (305, 240))
    pygame.draw.rect(win, (255, 255, 255), (140, 240, 60, 28), 2)
    pygame.draw.rect(win, (255, 255, 255), (300, 240, 50, 28), 2)

    if msg is None:
        win.blit(CHESS.MESSAGE[0], (130, 160))
        win.blit(CHESS.MESSAGE[1], (190, 190))
    elif msg == -1:
        win.blit(CHESS.MESSAGE[0], (130, 160))
        win.blit(CHESS.MESSAGE[1], (190, 190))
        win.blit(CHESS.SAVE_ERR, (115, 270))
    else:
        win.blit(CHESS.MESSAGE2[0], (123, 160))
        win.blit(CHESS.MESSAGE2[1], (145, 190))
        win.blit(CHESS.MSG, (135, 270))
        putNum(win, msg, (345, 270))

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 240 < event.pos[1] < 270:
                    if 140 < event.pos[0] < 200:
                        return True
                    elif 300 < event.pos[0] < 350:
                        return False


def start(win, load):
    """Play a short introduction animation and initialize piece images for a new game.

    Converts all piece images to optimized formats using [`convertPieces`](#convertpieces),
    plays the opening sound via [`sound.play_start`](tools/sound.py),
    and creates a quick animation by drawing pieces moving across the board.

    Args:
        win (pygame.Surface): The window where the animation is displayed.
        load (dict): User preferences or settings controlling sound and visual effects.
    """
    convertPieces(win)
    sound.play_start(load)  # Audio feedback for game start.

    clk = pygame.time.Clock()
    for i in range(101):
        # Use tick_busy_loop for more precise timing in short loops.
        clk.tick_busy_loop(140)

        # Draw the board background so the moving pieces appear on top of it.
        drawBoard(win)

        # Animate pawns moving from the center outward.
        for j in range(8):
            win.blit(CHESS.PIECES[0]["p"], (0.5 * i * (j + 1), 225 + 1.25 * i))
            win.blit(CHESS.PIECES[1]["p"], (0.5 * i * (j + 1), 225 - 1.25 * i))

        # Animate other pieces in a similar style, giving a sense of progression.
        for j, pc in enumerate(["r", "n", "b", "q", "k", "b", "n", "r"]):
            win.blit(CHESS.PIECES[0][pc], (0.5 * i * (j + 1), 225 + 1.75 * i))
            win.blit(CHESS.PIECES[1][pc], (0.5 * i * (j + 1), 225 - 1.75 * i))

        pygame.display.update()