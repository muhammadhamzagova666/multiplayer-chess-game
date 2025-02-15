"""
This file is a part of the Chess application.
In this file, we define the core chess-related functions.
For a better understanding of the variables used here, refer to docs.txt.
"""


def copy(board):
    """Produce a deep copy of the provided board structure.

    This function creates a new list of lists, ensuring changes to the
    copied board do not affect the original.
    """
    return [[list(j) for j in board[i]] for i in range(2)]


def getType(side, board, pos):
    """Retrieve the piece type at the given position for the specified side.

    Args:
        side (int): Indicates the side (0 or 1).
        board (list): Two lists containing piece data for both sides.
        pos (list): [x, y] coordinates on the board.

    Returns:
        str or None: The piece type string (e.g., 'k', 'q', 'p') if found,
                     or None if the square is empty.
    """
    for piece in board[side]:
        if piece[:2] == pos:
            return piece[2]


def isOccupied(side, board, pos):
    """Check if a given position is occupied by any piece of the specified side.

    Utilizes [`getType`](Source/chess/lib/core.py) to determine if a piece
    is present at the position.

    Args:
        side (int): Indicates the side to test (0 or 1).
        board (list): Board data structure.
        pos (list): [x, y] coordinates.

    Returns:
        bool: True if a piece of the given side occupies the position, False otherwise.
    """
    return getType(side, board, pos) is not None


def isEmpty(board, *poslist):
    """Verify that one or more board positions are empty, regardless of side.

    Iterates through each position in poslist, checking if
    [`isOccupied`](Source/chess/lib/core.py) indicates a piece is present.

    Args:
        board (list): Main board structure.
        *poslist: One or more [x, y] positions to verify.

    Returns:
        bool: True if all specified positions are empty, False otherwise.
    """
    for pos in poslist:
        for side in range(2):
            if isOccupied(side, board, pos):
                return False
    return True


def isChecked(side, board):
    """Determine if the current side's king is in check.

    The function locates the king for the given side, then scans
    the opposing side's possible raw moves to see if the king's position is threatened.

    Args:
        side (int): Side whose king status is being evaluated.
        board (list): Current board data.

    Returns:
        bool: True if the king is in check, otherwise False.
    """
    for piece in board[side]:
        if piece[2] == "k":
            for opp_piece in board[not side]:
                # If the king's position is within the opponent's raw moves, it's in check.
                if piece[:2] in rawMoves(not side, board, opp_piece):
                    return True
            return False


def legalMoves(side, board, flags):
    """Generate all possible legal moves for the specified side.

    Combines [`availableMoves`](Source/chess/lib/core.py) for each piece
    to produce a generator of valid [origin, destination] pairs.

    Args:
        side (int): Side to evaluate (0 or 1).
        board (list): Board data structure.
        flags (list): Castling and en passant flags.

    Yields:
        list: A pair of positions [[x1, y1], [x2, y2]] indicating a possible move.
    """
    for piece in board[side]:
        for pos in availableMoves(side, board, piece, flags):
            yield [piece[:2], pos]


def isEnd(side, board, flags):
    """Determine if the game has ended for the current side.

    If no legal moves are available for the given side,
    the game is considered ended (checkmate or stalemate).

    Args:
        side (int): Side to evaluate (0 or 1).
        board (list): Board data structure.
        flags (list): Castling and en passant flags.

    Returns:
        bool: True if the side has no legal moves, False otherwise.
    """
    for _ in legalMoves(side, board, flags):
        return False
    return True


def move(side, board, fro, to, promote="p"):
    """Perform a move on the board, including special rules like castling or en passant.

    This function updates piece positions and removes captured pieces. It can also
    handle pawn promotion by replacing the pawn with the new piece type.

    Args:
        side (int): The side making the move (0 or 1).
        board (list): Board data structure (directly modified here).
        fro (list[int]): Origin [x, y].
        to (list[int]): Destination [x, y].
        promote (str, optional): Promotion piece type, defaults to 'p'.

    Returns:
        list: An updated reference to the modified board.
    """
    UP = 8 if side else 1
    DOWN = 1 if side else 8
    # en passant is allowed if a diagonal move leads to an otherwise empty square
    ALLOWENP = fro[1] == 4 + side and to[0] != fro[0] and isEmpty(board, to)
    # Remove captured piece from the opposite side if it occupies the 'to' square
    for piece in board[not side]:
        if piece[:2] == to:
            board[not side].remove(piece)
            break

    # Move the piece for the acting side
    for piece in board[side]:
        if piece[:2] == fro:
            piece[:2] = to
            # Handle castling by moving the rook if needed
            if piece[2] == "k":
                if fro[0] - to[0] == 2:
                    move(side, board, [1, DOWN], [4, DOWN])
                elif to[0] - fro[0] == 2:
                    move(side, board, [8, DOWN], [6, DOWN])

            # Handle pawn promotion or en passant capture
            if piece[2] == "p":
                if to[1] == UP:
                    board[side].remove(piece)
                    board[side].append([to[0], UP, promote])
                if ALLOWENP:
                    board[not side].remove([to[0], fro[1], "p"])
            break

    return board


def moveTest(side, board, fro, to):
    """Test if a hypothetical move would leave the acting side's king in check.

    Clones the board using [`copy`](Source/chess/lib/core.py) before moving pieces,
    so the actual game state remains unaffected.

    Args:
        side (int): Side making the hypothetical move (0 or 1).
        board (list): Board data structure.
        fro (list[int]): Origin square [x, y].
        to (list[int]): Destination square [x, y].

    Returns:
        bool: True if the king is NOT in check after the move, False if still in check.
    """
    return not isChecked(side, move(side, copy(board), fro, to))


def isValidMove(side, board, flags, fro, to):
    """Check whether a move is valid within board boundaries and piece constraints.

    Ensures the destination is within standard board limits and not occupied
    by the same side. Also checks if [`rawMoves`](Source/chess/lib/core.py)
    confirm the move and [`moveTest`](Source/chess/lib/core.py) verifies
    that the king is not placed in check.

    Args:
        side (int): Side attempting the move (0 or 1).
        board (list): Main board data.
        flags (list): Castling/en passant flags.
        fro (list[int]): Origin [x, y].
        to (list[int]): Destination [x, y].

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if 0 < to[0] < 9 and 0 < to[1] < 9 and not isOccupied(side, board, to):
        piece = fro + [getType(side, board, fro)]
        if to in rawMoves(side, board, piece, flags):
            return moveTest(side, board, fro, to)


def makeMove(side, board, fro, to, flags, promote="q"):
    """Execute a move fully, including flag updates and side-switching.

    Calls [`move`](Source/chess/lib/core.py) to change board positions,
    then updates castling/en passant flags via [`updateFlags`](Source/chess/lib/core.py),
    and finally flips the side.

    Args:
        side (int): The side making the move.
        board (list): Board data structure to modify.
        fro (list[int]): Origin [x, y].
        to (list[int]): Destination [x, y].
        flags (list): Castling and en passant flags.
        promote (str, optional): Promotion piece type, defaults to 'q'.

    Returns:
        tuple: (next_side, resulting_board, updated_flags)
               next_side (bool): The new side (True or False).
               resulting_board (list): The updated board.
               updated_flags (list): The new flags.
    """
    newboard = move(side, copy(board), fro, to, promote)
    newflags = updateFlags(side, newboard, fro, to, flags)
    return not side, newboard, newflags


def updateFlags(side, board, fro, to, flags):
    """Adjust castling and en passant flags after a completed move.

    Checks if rooks or kings have moved to disable castling rights, and sets
    or removes en passant coordinates based on the last move of a pawn.

    Args:
        side (int): The side that just moved.
        board (list): Current board data (with move already applied).
        fro (list[int]): The origin square [x, y].
        to (list[int]): The destination square [x, y].
        flags (list): Existing flags ([castling_info], en_passant_pos).

    Returns:
        list: Updated flags reflecting castling or en passant changes.
    """
    castle = list(flags[0])
    # Disable castling if the king or its respective rook has moved
    if [5, 8, "k"] not in board[0] or [1, 8, "r"] not in board[0]:
        castle[0] = False
    if [5, 8, "k"] not in board[0] or [8, 8, "r"] not in board[0]:
        castle[1] = False
    if [5, 1, "k"] not in board[1] or [1, 1, "r"] not in board[1]:
        castle[2] = False
    if [5, 1, "k"] not in board[1] or [8, 1, "r"] not in board[1]:
        castle[3] = False

    enP = None
    # Set en passant if a pawn moved forward two squares
    if getType(side, board, to) == "p":
        if fro[1] - to[1] == 2:
            enP = [to[0], 6]
        elif to[1] - fro[1] == 2:
            enP = [to[0], 3]

    return castle, enP


def availableMoves(side, board, piece, flags):
    """Generate all legally available moves for a single piece, filtered for checks.

    This function wraps [`rawMoves`](Source/chess/lib/core.py) and ensures
    no move places the piece’s own king in check by calling
    [`moveTest`](Source/chess/lib/core.py).

    Args:
        side (int): The side of the piece.
        board (list): Board data structure.
        piece (list): Piece data in form [x, y, 'ptype'].
        flags (list): Castling and en passant flags.

    Yields:
        list[int]: Valid destination coordinates [dest_x, dest_y].
    """
    for dest in rawMoves(side, board, piece, flags):
        if 0 < dest[0] < 9 and 0 < dest[1] < 9 and not isOccupied(side, board, dest):
            if moveTest(side, board, piece[:2], dest):
                yield dest


def rawMoves(side, board, piece, flags=[None, None]):
    """Compute all possible moves for a piece, ignoring legality checks like self-check.

    This includes castling moves (if flags are given) and en passant captures. 
    Note that many moves returned may still be illegal if they place the king in check.

    Args:
        side (int): The side of the piece (0 or 1).
        board (list): Board representation where board[0] and board[1] hold each side’s pieces.
        piece (list): A piece in the format [x, y, 'ptype'].
        flags (list, optional): [castling_info, en_passant_pos]. Defaults to [None, None].

    Yields:
        list[int]: Candidate move [destination_x, destination_y], which may or may not be ultimately valid.
    """
    x, y, ptype = piece
    # Pawn handling (forward moves, captures, two-step moves, en passant)
    if ptype == "p":
        if not side:
            # White pawns move upward (decreasing y)
            if y == 7 and isEmpty(board, [x, 6], [x, 5]):
                yield [x, 5]
            if isEmpty(board, [x, y - 1]):
                yield [x, y - 1]
            for diag in ([x + 1, y - 1], [x - 1, y - 1]):
                if isOccupied(1, board, diag) or flags[1] == diag:
                    yield diag
        else:
            # Black pawns move downward (increasing y)
            if y == 2 and isEmpty(board, [x, 3], [x, 4]):
                yield [x, 4]
            if isEmpty(board, [x, y + 1]):
                yield [x, y + 1]
            for diag in ([x + 1, y + 1], [x - 1, y + 1]):
                if isOccupied(0, board, diag) or flags[1] == diag:
                    yield diag

    elif ptype == "n":
        # Knight's L-shaped moves
        yield from (
            [x + 1, y + 2], [x + 1, y - 2], [x - 1, y + 2], [x - 1, y - 2],
            [x + 2, y + 1], [x + 2, y - 1], [x - 2, y + 1], [x - 2, y - 1]
        )

    elif ptype == "b":
        # Diagonal movement in four directions
        for i in range(1, 8):
            yield [x + i, y + i]
            if not isEmpty(board, [x + i, y + i]):
                break
        for i in range(1, 8):
            yield [x + i, y - i]
            if not isEmpty(board, [x + i, y - i]):
                break
        for i in range(1, 8):
            yield [x - i, y + i]
            if not isEmpty(board, [x - i, y + i]):
                break
        for i in range(1, 8):
            yield [x - i, y - i]
            if not isEmpty(board, [x - i, y - i]):
                break

    elif ptype == "r":
        # Straight-line rook moves
        for i in range(1, 8):
            yield [x + i, y]
            if not isEmpty(board, [x + i, y]):
                break
        for i in range(1, 8):
            yield [x - i, y]
            if not isEmpty(board, [x - i, y]):
                break
        for i in range(1, 8):
            yield [x, y + i]
            if not isEmpty(board, [x, y + i]):
                break
        for i in range(1, 8):
            yield [x, y - i]
            if not isEmpty(board, [x, y - i]):
                break

    elif ptype == "q":
        # Queen moves are a combination of bishop + rook moves
        yield from rawMoves(side, board, [x, y, "b"], flags)
        yield from rawMoves(side, board, [x, y, "r"], flags)

    elif ptype == "k":
        # King moves plus castling (if not in check and squares are empty)
        if flags[0] is not None and not isChecked(side, board):
            # White castling
            if flags[0][0] and isEmpty(board, [2, 8], [3, 8], [4, 8]):
                if moveTest(0, board, [5, 8], [4, 8]):
                    yield [3, 8]
            if flags[0][1] and isEmpty(board, [6, 8], [7, 8]):
                if moveTest(0, board, [5, 8], [6, 8]):
                    yield [7, 8]
            # Black castling
            if flags[0][2] and isEmpty(board, [2, 1], [3, 1], [4, 1]):
                if moveTest(1, board, [5, 1], [4, 1]):
                    yield [3, 1]
            if flags[0][3] and isEmpty(board, [6, 1], [7, 1]):
                if moveTest(1, board, [5, 1], [6, 1]):
                    yield [7, 1]

        # Single-square king moves in all directions
        yield from (
            [x - 1, y - 1], [x, y - 1], [x + 1, y - 1], [x - 1, y],
            [x - 1, y + 1], [x, y + 1], [x + 1, y + 1], [x + 1, y]
        )