"""
This file is part of the Chess application.
It defines various non-GUI helper functions for encoding and decoding moves, as well
as initializing board variables and other utility functionalities.
"""

from datetime import datetime
import os
import time

# Maps numeric columns (1..8) to their corresponding letter identifiers as used in algebraic notation.
LETTER = ["", "a", "b", "c", "d", "e", "f", "g", "h"]


def encode(fro, to, promote=None):
    """Convert internal game move notation to a standard algebraic notation string.

    This function uses the global [`LETTER`](Source/chess/lib/utils.py) array
    to build a 4-character string (e.g., "e2e4") and appends the promotion piece
    type if provided.

    Args:
        fro (list[int, int]): A pair [x, y] denoting the origin square in internal format.
        to (list[int, int]): A pair [x, y] denoting the destination square in internal format.
        promote (str, optional): The character representing a piece to promote to (e.g., "q").
                                 Defaults to None.

    Returns:
        str: Algebraic notation for the move, optionally including a promotion piece
             (e.g., "e7e8q").
    """
    data = LETTER[fro[0]] + str(9 - fro[1]) + LETTER[to[0]] + str(9 - to[1])
    if promote is not None:
        return data + promote
    return data


def decode(data):
    """Convert a standard algebraic notation string back to the internal game format.

    This function interprets the 4-character move string (e.g., "e2e4") and reconstructs
    the coordinate pairs required by the engine. If a promotion piece is appended, it is
    returned as the third element in the returned list.

    Args:
        data (str): A string containing the move in standard notation (e.g., "e2e4q").

    Returns:
        list: A list with two coordinate pairs and a promotion character (or None),
              e.g. [[4, 6], [4, 4], 'q'].
    """
    ret = [
        [LETTER.index(data[0]), 9 - int(data[1])],
        [LETTER.index(data[2]), 9 - int(data[3])],
    ]
    if len(data) == 5:
        ret.append(data[4])
    else:
        ret.append(None)
    return ret


def initBoardVars():
    """Set up the initial board state, including side-to-move and other flags.

    The board is represented as two lists that track the piece positions for each side.
    The side variable (bool) indicates which side is active (False for one side, True for the other),
    while the flags array holds castling or other special conditions.

    Returns:
        tuple: A tuple containing (side, board, flags).
               side (bool): Indicates which side is active (False or True).
               board (list): 2D list of piece placements for both sides.
               flags (list): Additional game flags (castling rights, etc.).
    """
    side = False
    board = [
        [
            [1, 7, "p"], [2, 7, "p"], [3, 7, "p"], [4, 7, "p"],
            [5, 7, "p"], [6, 7, "p"], [7, 7, "p"], [8, 7, "p"],
            [1, 8, "r"], [2, 8, "n"], [3, 8, "b"], [4, 8, "q"],
            [5, 8, "k"], [6, 8, "b"], [7, 8, "n"], [8, 8, "r"],
        ], [
            [1, 2, "p"], [2, 2, "p"], [3, 2, "p"], [4, 2, "p"],
            [5, 2, "p"], [6, 2, "p"], [7, 2, "p"], [8, 2, "p"],
            [1, 1, "r"], [2, 1, "n"], [3, 1, "b"], [4, 1, "q"],
            [5, 1, "k"], [6, 1, "b"], [7, 1, "n"], [8, 1, "r"],
        ]
    ]
    flags = [[True for _ in range(4)], None]
    return side, board, flags


def undo(moves, num=1):
    """Remove the last 'num' moves from the move history.

    This function is useful for reversing the state of the game if the user or an AI
    decides to revert a certain number of moves.

    Args:
        moves (list): The entire move history as a list of strings or tuples.
        num (int, optional): Number of moves to remove. Defaults to 1.

    Returns:
        list: The updated move list after removing the specified number of moves.
    """
    if len(moves) in range(num):
        return moves
    return moves[:-num]


def getSFpath():
    """Resolve the file path to the Stockfish engine from a config file.

    The path is expected to be stored inside 'res/stockfish/path.txt'. If the file exists,
    the function reads and returns the engine path. Otherwise, None is returned.

    Returns:
        str or None: The path string if present in the config file, or None if not found.
    """
    conffile = os.path.join("res", "stockfish", "path.txt")
    if os.path.exists(conffile):
        with open(conffile, "r") as f:
            return f.read().strip()
    return None


def rmSFpath():
    """Remove the Stockfish engine path file if it exists.

    This is typically called when the user wants to reset or change the configuration
    for the Stockfish engine path.
    """
    os.remove(os.path.join("res", "stockfish", "path.txt"))


def getTime():
    """Obtain the current high-resolution time in milliseconds.

    Uses time.perf_counter() for high-resolution timing, then rounds it to
    the nearest millisecond.

    Returns:
        int: Elapsed milliseconds as an integer.
    """
    return round(time.perf_counter() * 1000)


def updateTimer(side, mode, timer):
    """Update a game timer array based on whose turn just ended.

    The timer array typically holds remaining time for each side. This function
    adjusts the timer for the given side by 'mode' seconds, converting from seconds
    to milliseconds if necessary.

    Args:
        side (bool): Which side's timer should be updated (False or True).
        mode (int): Time adjustment in seconds, or -1 for no updates if the clock is stopped.
        timer (list[int]): Two-element list representing the time for each side in milliseconds.

    Returns:
        list or None: An updated list of millisecond timers. Returns None if timer is None.
    """
    if timer is None:
        return None

    ret = list(timer)
    if mode != -1:
        ret[side] += (mode * 1000)
    return ret


def saveGame(moves, gametype="multi", player=0, level=0, mode=None, timer=None, cnt=0):
    """Persist a chess game into a TXT file under 'res/savedGames'.

    Files are named sequentially (game0.txt, game1.txt, etc.). If the chosen file name
    already exists, the function attempts the next number recursively up to 20 times.
    The file stores all moves in algebraic notation, along with the date/time and some
    custom data depending on the game mode.

    Args:
        moves (list[str]): A list of moves in long algebraic notation (e.g., "e2e4").
        gametype (str, optional): Type of the game (e.g., "multi", "single", etc.).
                                  Defaults to "multi".
        player (int, optional): Which side the user is (0 or 1). Defaults to 0.
        level (int, optional): Difficulty level if the gametype is single-player. Defaults to 0.
        mode (int or None, optional): Additional mode parameter (e.g., time control). Defaults to None.
        timer (list[int] or None, optional): Two-element list of time left for each side. Defaults to None.
        cnt (int, optional): Internal counter for file naming attempts. Defaults to 0.

    Returns:
        int: The file index if the game was saved successfully, or -1 if saving was aborted.
    """
    if cnt >= 20:
        return -1

    name = os.path.join("res", "savedGames", "game" + str(cnt) + ".txt")
    if os.path.isfile(name):
        # If file exists, increment 'cnt' and try again
        return saveGame(moves, gametype, player, level, mode, timer, cnt + 1)

    # Build up a string detailing the game type, date/time, moves, and additional info.
    if gametype == "single":
        gametype += " " + str(player) + " " + str(level)
    elif gametype == "mysingle":
        gametype += " " + str(player)

    dt = datetime.now()
    date = "/".join(map(str, [dt.day, dt.month, dt.year]))
    cur_time = ":".join(map(str, [dt.hour, dt.minute, dt.second]))
    datentime = " ".join([date, cur_time])

    movestr = " ".join(moves)
    extra_info = []
    if mode is not None:
        extra_info.append(str(mode))
        if timer is not None:
            extra_info.extend(map(str, timer))
    extra_info = " ".join(extra_info)

    text = "\n".join([gametype, datentime, movestr, extra_info])

    # Write the final string to a new text file.
    with open(name, "w") as file:
        file.write(text)
    return cnt