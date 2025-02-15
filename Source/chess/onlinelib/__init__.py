'''
This file is a part of Chess application.
In this file, we define the main functions for online chess, and aggregate
other functions for importing from [online.py](Source/chess/online.py).
'''

import pygame
import pygame.event

# Importing all required symbols from [chess.lib.__init__.py](Source/chess/lib/__init__.py)
# See [chess/lib/__init__.py](Source/chess/lib/__init__.py) for more details.
from chess.lib import (
    start, isOccupied, isValidMove, animate, makeMove, encode,
    decode, initBoardVars, isEnd, sound, showScreen
)

# Importing helper functions for the online lobby and popups from
# [chess.onlinelib.utils](Source/chess/onlinelib/utils.py).
from chess.onlinelib.utils import (
    getPlayers, showLobby, request, draw, readable, read, flush, write, showUpdateList, showLoading
)


def lobby(win, sock, key, load):
    """Handle all lobby-related logic for the online chess mode.

    This function displays the online lobby by calling
    [`showLobby`](Source/chess/onlinelib/utils.py), retrieves
    the latest player list from the server, and processes
    user inputs (e.g., refreshing the list, requesting a game).
    It communicates with the server via the provided socket,
    sending and receiving instructions based on lobby interactions.

    Args:
        win (pygame.Surface): The surface onto which the lobby UI is drawn.
        sock (socket.socket): An open socket connected to the chess server.
        key (int): Unique identifier for the local player.
        load (dict): Configuration and preferences loaded from the user’s settings.

    Returns:
        int: A status or error code indicating the next action:
             - 0 if the user quits the entire application.
             - 1 if the user navigates back to a previous menu.
             - 2 if the server closes or an error disrupts the connection.
             - Other codes for advanced scenarios or internal states.
    """
    clock = pygame.time.Clock()
    playerList = getPlayers(sock)  # Fetch initial list of active players.

    while True:
        clock.tick(10)  # Update at 10 FPS to avoid resource overuse.

        # If the player list is None, it implies a server error or disconnection.
        if playerList is None:
            return 2

        # Render the lobby UI with current player list.
        showLobby(win, key, playerList)

        # Process all Pygame events (e.g., mouse clicks, window close requests).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If user closes the entire window, inform server and exit.
                write(sock, "quit")
                return 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Clicking top-right area triggers a "back to main menu" request.
                if 460 < x < 500 and 0 < y < 50:
                    write(sock, "quit")
                    return 1

                # Clicking "Refresh" button to reload player list.
                if 270 < x < 300 and 85 < y < 115:
                    playerList = getPlayers(sock)

                # Clicking any "Request" button in the player list area.
                if 300 < x < 475:
                    for i in range(len(playerList)):
                        if 122 + 30 * i < y < 148 + 30 * i:
                            write(sock, "rg" + playerList[i][:4])
                            msg = read()

                            # If connection is closed or broken after we attempt a match.
                            if msg == "close":
                                return 2

                            elif msg == "msgOk":
                                # Show a request popup for user to confirm or decline match.
                                ret = request(win, sock)
                                if ret in [0, 1, 2]:
                                    return ret
                                elif ret == 4:
                                    # Start a chess game as the initiating player.
                                    newret = chess(win, sock, 0, load)
                                    if newret in [0, 1, 2]:
                                        return newret

                            elif msg.startswith("err"):
                                # Show an update/error popup if the server responded with an error.
                                showUpdateList(win)

                            # Refresh the player list after the request is processed.
                            playerList = getPlayers(sock)
                            break

        # Check for any unsolicited messages (e.g., incoming game requests).
        if readable():
            msg = read()
            if msg == "close":
                return 2

            elif msg.startswith("gr"):
                # "gr" indicates another player is requesting a game with us.
                ret = request(win, sock, msg[2:])
                if ret == 4:
                    # Local player accepted; notify server we are ready.
                    write(sock, "gmOk" + msg[2:])
                    newret = chess(win, sock, 1, load)
                    if newret in [0, 1, 2]:
                        return newret
                else:
                    # If declined or the server closed, inform server and propagate the code.
                    write(sock, "gmNo" + msg[2:])
                    if ret == 2:
                        return ret
                # Refresh the list in case of changes after the request.
                playerList = getPlayers(sock)


def chess(win, sock, player, load):
    """Manage the actual online chess gameplay once two players connect.

    This function initializes the board state with
    [`initBoardVars`](Source/chess/lib/__init__.py) then listens for socket
    messages to synchronize moves between players. Local inputs are validated
    and sent to the server, while remote moves from the opponent are also applied.
    It relies on functions like [`isValidMove`](Source/chess/lib/__init__.py),
    [`animate`](Source/chess/lib/__init__.py), and
    [`makeMove`](Source/chess/lib/__init__.py) to handle core game logic.

    Args:
        win (pygame.Surface): The surface on which the chessboard is drawn.
        sock (socket.socket): The socket used for sending and receiving moves.
        player (int): Indicates which side the local user controls (0 or 1).
        load (dict): Configuration dict with user preferences.

    Returns:
        int: A code describing the outcome of the online chess game:
             - 0 if the user quits the entire application window.
             - 2 if the server closes or the connection drops unexpectedly.
             - 3 if the local side resigns, the opponent resigns, or the game ends.
    """
    # Prepare the board and environment using [`start`](Source/chess/lib/__init__.py).
    start(win, load)

    # Initialize board position, side, and flags representing game metadata.
    side, board, flags = initBoardVars()

    clock = pygame.time.Clock()
    sel = prevsel = [0, 0]  # Track current and previous selections for piece movement.

    while True:
        # Limit frame rate to 25 FPS for smoother rendering.
        clock.tick(25)

        # Check user input from mouse or window events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # User closed entire window, so we inform the server and exit.
                write(sock, "quit")
                return 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Clicking top-right area requests to end the current match safely.
                if 460 < x < 500 and 0 < y < 50:
                    write(sock, "end")
                    return 3

                # If click is on the board area, attempt to move locally if it's our turn.
                if 50 < x < 450 and 50 < y < 450:
                    x, y = x // 50, y // 50
                    # If the board is flipped for the second player, invert coordinates.
                    if load["flip"] and player:
                        x, y = 9 - x, 9 - y

                    # Play an audio cue if the clicked square is occupied (and it's our side).
                    if isOccupied(side, board, [x, y]) and side == player:
                        # See [`sound.play_click`](tools/sound.py).
                        sound.play_click(load)

                    prevsel = sel
                    sel = [x, y]

                    # Only move if it is our turn and the move is valid.
                    if (side == player
                            and isValidMove(side, board, flags, prevsel, sel)):

                        # If there's a need for pawn promotion, retrieve user choice.
                        promote = getPromote(win, player, board, prevsel, sel)
                        # Relay the move to the server with 'mov' prefix.
                        write(sock, "mov" + encode(prevsel, sel, promote))

                        # Animate the movement locally for a polished user experience.
                        animate(win, player, board, prevsel, sel, load, player)
                        side, board, flags = makeMove(side, board, prevsel, sel, flags, promote)

                elif not isEnd(side, board, flags):
                    # If the board state isn't terminal, check for optional draw/resign triggers.
                    if 0 < x < 70 and 0 < y < 50:
                        # Send a draw request to opponent.
                        write(sock, "draw?")
                        ret = draw(win, sock)
                        if ret in [0, 2, 3]:
                            return ret

                    # Clicking lower-right corner signals resignation.
                    if 400 < x < 500 and 450 < y < 500:
                        write(sock, "resign")
                        return 3

        # Refresh the on-screen board, highlighting selected squares, etc.
        # See [`showScreen`](Source/chess/lib/__init__.py).
        showScreen(win, side, board, flags, sel, load, player, True)

        # Process incoming messages from the server.
        if readable():
            msg = read()

            # If connection dropped entirely.
            if msg == "close":
                return 2

            # Opponent or server indicates quitting/resigning.
            elif msg == "quit" or msg == "resign":
                return popup(win, sock, msg)

            elif msg == "end":
                # If the board state is ended by checkmate, or abrupt abandon.
                msg = "end" if isEnd(side, board, flags) else "abandon"
                return popup(win, sock, msg)

            elif msg == "draw?":
                # Handle draw request from opponent.
                ret = draw(win, sock, False)
                if ret in [2, 3]:
                    return ret

            # If the opponent made a move, apply it locally.
            elif msg.startswith("mov") and side != player:
                fro, to, promote = decode(msg[3:])
                if isValidMove(side, board, flags, fro, to):
                    animate(win, side, board, fro, to, load, player)
                    side, board, flags = makeMove(side, board, fro, to, flags, promote)
                    sel = [0, 0]  # Reset our selection after applying a remote move.
                else:
                    # If there's an invalid move, assume a desync or error.
                    return 2