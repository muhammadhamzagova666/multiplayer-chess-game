"""
This file is a part of the Chess application. It provides a unified import interface
(called "Chess Standard Chess Library") by collecting the functionalities from the
core, GUI, and utils modules in [Source/chess/lib](Source/chess/lib). It also defines
helper functions that depend on multiple modules for convenience.

Usage:
    >>> from chess.lib import *

For more details on variables used here, refer to docs.txt.
"""

# Import essential gameplay and logic functions from the core library.
from chess.lib.core import (
    getType,          # [getType](Source/chess/lib/core.py)
    isOccupied,       # [isOccupied](Source/chess/lib/core.py)
    isChecked,        # [isChecked](Source/chess/lib/core.py)
    isEnd,            # [isEnd](Source/chess/lib/core.py)
    isValidMove,      # [isValidMove](Source/chess/lib/core.py)
    availableMoves,   # [availableMoves](Source/chess/lib/core.py)
    makeMove,         # [makeMove](Source/chess/lib/core.py)
)

# Import GUI-related items from the gui module.
from chess.lib.gui import (
    pygame,           # [pygame](Source/chess/lib/gui.py)
    CHESS,            # [CHESS](Source/chess/lib/gui.py)
    BACK,             # [BACK](Source/chess/lib/gui.py)
    sound,            # [sound](Source/chess/lib/gui.py)
    getChoice,        # [getChoice](Source/chess/lib/gui.py)
    showTimeOver,     # [showTimeOver](Source/chess/lib/gui.py)
    putClock,         # [putClock](Source/chess/lib/gui.py)
    drawBoard,        # [drawBoard](Source/chess/lib/gui.py)
    drawPieces,       # [drawPieces](Source/chess/lib/gui.py)
    prompt,           # [prompt](Source/chess/lib/gui.py)
    start,            # [start](Source/chess/lib/gui.py)
)

# Import utility functions from the utils module.
from chess.lib.utils import (
    encode,           # [encode](Source/chess/lib/utils.py)
    decode,           # [decode](Source/chess/lib/utils.py)
    initBoardVars,    # [initBoardVars](Source/chess/lib/utils.py)
    undo,             # [undo](Source/chess/lib/utils.py)
    getSFpath,        # [getSFpath](Source/chess/lib/utils.py)
    rmSFpath,         # [rmSFpath](Source/chess/lib/utils.py)
    getTime,          # [getTime](Source/chess/lib/utils.py)
    updateTimer,      # [updateTimer](Source/chess/lib/utils.py)
    saveGame,         # [saveGame](Source/chess/lib/utils.py)
)


def convertMoves(moves):
    """Convert a list of algebraic move strings into the internal board representation.

    Automatically initializes the board using [`initBoardVars`](Source/chess/lib/utils.py),
    decodes each move via [`decode`](Source/chess/lib/utils.py), and applies the move
    using [`makeMove`](Source/chess/lib/core.py).

    Args:
        moves (list[str]): A list of move strings in long algebraic notation (e.g., "e2e4").

    Returns:
        tuple: (side, board, flags) representing the current side to move, updated board,
               and castling/en passant flags after applying all moves.
    """
    side, board, flags = initBoardVars()

    for fro, to, promote in map(decode, moves):
        side, board, flags = makeMove(side, board, fro, to, flags, promote)

    return side, board, flags


def getPromote(win, side, board, fro, to, single=False):
    """Determine which piece type a pawn should promote to.

    Checks if a pawn has reached the last rank and then decides whether to offer a GUI
    choice via [`getChoice`](Source/chess/lib/gui.py) or automatically choose 'q' depending
    on the 'single' player flag.

    Args:
        win (pygame.Surface): The main game window surface.
        side (int): The side making the move (0 or 1).
        board (list): Board state.
        fro (list[int]): Origin [x, y] of the pawn.
        to (list[int]): Destination [x, y] of the pawn.
        single (bool, optional): If True, automatically choose "q"; otherwise display a GUI. Defaults to False.

    Returns:
        str or None: The chosen promotion piece symbol, or None if no promotion is applicable.
    """
    if getType(side, board, fro) == "p":
        # Check if the pawn has reached the promotion rank
        if (side == 0 and to[1] == 1) or (side == 1 and to[1] == 8):
            if single:
                return "q"
            else:
                return getChoice(win, side)
    # No promotion required
    return None


def showClock(win, side, mode, timer, start_time, timedelta):
    """Update and display the clock for a specific side, handling time increments or decrements.

    If the game mode is -1, the clock is effectively paused, and elapsed time is added to
    the side's timer. Otherwise, the elapsed time is subtracted. It calls
    [`showTimeOver`](Source/chess/lib/gui.py) if time runs out, and uses
    [`putClock`](Source/chess/lib/gui.py) for rendering.

    Args:
        win (pygame.Surface): Game window surface for drawing the clock.
        side (int): The current side whose clock is updated.
        mode (int): Clock mode; -1 indicates paused, any other value means time is ticking.
        timer (list[int] or None): [time_side0, time_side1] in milliseconds, or None if no clock is used.
        start_time (int): A reference timestamp in milliseconds.
        timedelta (int): Amount of time offset to account for (e.g., any latency adjustments).

    Returns:
        list[int] or None: Updated timer array if still valid, or None if time ended or no timer given.
    """
    if timer is None:
        pygame.display.update()
        return None

    ret = list(timer)
    elapsed = getTime() - (start_time + timedelta)
    if mode == -1:
        # Paused time is added; can be used for manually adjusting or incrementing
        ret[side] += elapsed
        if ret[side] >= 3600000:
            ret[side] = 3599000  # Hard cap at just under one hour
    else:
        # Subtract elapsed time in normal mode
        ret[side] -= elapsed
        if ret[side] < 0:
            showTimeOver(win, side)
            return None

    putClock(win, ret)
    return ret


def showAvailMoves(win, side, board, pos, flags, flip):
    """Visualize legal moves by drawing green squares for the selected piece.

    This function iterates over all possible moves from
    [`availableMoves`](Source/chess/lib/core.py) and draws small markers on each valid square.

    Args:
        win (pygame.Surface): The game window surface.
        side (int): Side to move (0 or 1).
        board (list): Current board structure.
        pos (list[int]): [x, y] origin of the selected piece.
        flags (list): Castling/en passant flags.
        flip (bool): If True, the board display is inverted for the opponent's perspective.
    """
    piece = pos + [getType(side, board, pos)]
    for i in availableMoves(side, board, piece, flags):
        x = 470 - i[0] * 50 if flip else i[0] * 50 + 20
        y = 470 - i[1] * 50 if flip else i[1] * 50 + 20
        pygame.draw.rect(win, (0, 255, 0), (x, y, 10, 10))


def animate(win, side, board, fro, to, load, player=None):
    """Create a smooth animation of moving a piece from origin to destination.

    This plays a drag sound before moving, smoothly transitions the piece, and finally
    plays a move sound. It relies on [`drawBoard`](Source/chess/lib/gui.py) and
    [`drawPieces`](Source/chess/lib/gui.py) to refresh the board at each frame.

    Args:
        win (pygame.Surface): The game window surface.
        side (int): Side making the move (0 or 1).
        board (list): Board configuration.
        fro (list[int]): Origin [x, y].
        to (list[int]): Destination [x, y].
        load (dict): User or system preferences, including settings like flip.
        player (int, optional): Indicates which side is controlled by the local player. Defaults to None.
    """
    sound.play_drag(load)
    if player is None:
        # In multiplayer, the 'side' is also the local player
        FLIP = side and load["flip"]
    else:
        FLIP = player and load["flip"]

    piece = CHESS.PIECES[side][getType(side, board, fro)]
    x1, y1 = fro[0] * 50, fro[1] * 50
    x2, y2 = to[0] * 50, to[1] * 50
    if FLIP:
        x1, y1 = 450 - x1, 450 - y1
        x2, y2 = 450 - x2, 450 - y2

    stepx = (x2 - x1) / 50.0
    stepy = (y2 - y1) / 50.0

    # Determine tile color for the origin square; helps redraw background cleanly
    col = (180, 100, 30) if (fro[0] + fro[1]) % 2 else (220, 240, 240)
    
    clk = pygame.time.Clock()
    for i in range(51):
        clk.tick_busy_loop(100)
        drawBoard(win)
        drawPieces(win, board, FLIP)

        pygame.draw.rect(win, col, (x1, y1, 50, 50))
        win.blit(piece, (x1 + (i * stepx), y1 + (i * stepy)))
        pygame.display.update()

    sound.play_move(load)


def showScreen(win, side, board, flags, pos, load, player=None, online=False):
    """Render the main chess screen and handle high-level visual updates.

    This includes drawing the board, flipping for opponents, indicating check/checkmate,
    showing legal moves, and placing interactive buttons. Called on each iteration of
    the game loop to keep the display current.

    Args:
        win (pygame.Surface): The main window surface.
        side (int): Current side to move (0 or 1).
        board (list): Board configuration.
        flags (list): Castling/en passant flags.
        pos (list[int]): Currently selected square [x, y].
        load (dict): Preferences, e.g., 'flip' board for the opposite player.
        player (int, optional): Which side the local user controls, or None for multiplayer. Defaults to None.
        online (bool, optional): If True, show additional online options like draw/resign. Defaults to False.
    """
    multi = False
    if player is None:
        multi = True  # In a local multiplayer scenario, there's no single "owner" side
        player = side

    flip = load["flip"] and player

    # Basic board and menu elements
    drawBoard(win)
    win.blit(BACK, (460, 0))  # A background or a "back" button placeholder

    # For single-player, display whose turn it is
    if not multi:
        win.blit(CHESS.TURN[int(side == player)], (10, 460))

    # If offline, show undo/save icons
    if not online:
        if load["allow_undo"]:
            win.blit(CHESS.UNDO, (10, 12))
        win.blit(CHESS.SAVE, (350, 462))

    # Check if the game has ended or if there's a check
    if isEnd(side, board, flags):
        if isChecked(side, board):
            win.blit(CHESS.CHECKMATE, (100, 12))
            win.blit(CHESS.LOST, (320, 12))
            win.blit(CHESS.PIECES[side]["k"], (270, 0))
        else:
            win.blit(CHESS.STALEMATE, (160, 12))
    else:
        if online:
            win.blit(CHESS.DRAW, (10, 12))
            win.blit(CHESS.RESIGN, (400, 462))

        if isChecked(side, board):
            win.blit(CHESS.CHECK, (200, 12))

        # Highlight the selected square if it belongs to the current player
        if isOccupied(side, board, pos) and side == player:
            x = (9 - pos[0]) * 50 if flip else pos[0] * 50
            y = (9 - pos[1]) * 50 if flip else pos[1] * 50
            pygame.draw.rect(win, (255, 255, 0), (x, y, 50, 50))

    drawPieces(win, board, flip)

    # Optionally show the green squares marking legal moves
    if load["show_moves"] and side == player:
        showAvailMoves(win, side, board, pos, flags, flip)

    # For single-player, continuously refresh the display to reflect changes
    if not multi:
        pygame.display.update()