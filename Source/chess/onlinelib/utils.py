"""
This file is part of the Chess application. It defines GUI utility functions for online chess,
including popups for errors, draw requests, and general notifications.

References:
    - [chess.onlinelib.sockutils](Source/chess/onlinelib/sockutils.py):
        Contains networking utilities for reading/writing data over sockets.
    - [tools.loader](Source/tools/loader.py):
        Provides the ONLINE, BACK, putLargeNum, and putNum assets and methods.
"""

import pygame

# Networking utilities: [readable](Source/chess/onlinelib/sockutils.py),
# [read](Source/chess/onlinelib/sockutils.py), [write](Source/chess/onlinelib/sockutils.py)
from chess.onlinelib.sockutils import readable, read, write

# Graphical resources and helper methods: [ONLINE, BACK, putLargeNum, putNum] (Source/tools/loader.py)
from tools.loader import ONLINE, BACK, putLargeNum, putNum


def showUpdateList(win):
    """Display a short popup indicating a connection error when joining a game.

    Args:
        win (pygame.Surface): The display surface for rendering the popup.
    """
    # Draw a dark rectangle as the popup background.
    pygame.draw.rect(win, (0, 0, 0), (110, 220, 280, 60))
    pygame.draw.rect(win, (255, 255, 255), (110, 220, 280, 60), 4)
    win.blit(ONLINE.ERRCONN, (120, 240))  # Show error message.

    pygame.display.update()
    for _ in range(50):
        pygame.time.delay(50)
        # Consume any pending events to keep the UI responsive.
        for _ in pygame.event.get():
            pass


def showLoading(win, errcode=0):
    """Show a loading message or an error popup before entering the lobby.

    Draws a bordered rectangle with text depending on the error code. If errcode
    is zero, just show a “loading” message. Otherwise, it displays an error message
    and a button to go back.

    Args:
        win (pygame.Surface): The display surface being used.
        errcode (int, optional): The error code determining which message is displayed.
                                 Zero indicates normal loading. Defaults to 0.
    """
    pygame.draw.rect(win, (0, 0, 0), (100, 220, 300, 80))
    pygame.draw.rect(win, (255, 255, 255), (100, 220, 300, 80), 4)
    win.blit(ONLINE.ERR[errcode], (115, 240))  # Select the correct message from the error list.

    if errcode == 0:
        # If no error, simply update the display and return.
        pygame.display.update()
        return

    # Draw a button for going back if there's an error.
    pygame.draw.rect(win, (255, 255, 255), (220, 270, 65, 20), 2)
    win.blit(ONLINE.GOBACK, (220, 270))
    pygame.display.update()

    # Wait for the user to click the button before closing the popup.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 220 < event.pos[0] < 285 and 270 < event.pos[1] < 290:
                    return


def popup(win, sock, typ):
    """Show a small popup message for events like player leaving, resignation, or draw acceptance.

    Args:
        win (pygame.Surface): The display surface for rendering the popup.
        sock (socket.socket): Connected socket for sending/receiving messages.
        typ (str): The type of popup to display, such as 'left', 'resigned', or 'draw'.
                   Used to select the corresponding message in ONLINE.POPUP.
    """
    pygame.draw.rect(win, (0, 0, 0), (130, 220, 240, 80))
    pygame.draw.rect(win, (255, 255, 255), (130, 220, 240, 80), 4)
    win.blit(ONLINE.POPUP[typ], (145, 240))

    # Draw a "Go Back" button on the popup.
    pygame.draw.rect(win, (255, 255, 255), (220, 270, 65, 20), 2)
    win.blit(ONLINE.GOBACK, (220, 270))
    pygame.display.update()

    ret = 3  # Default return value for multi-case usage.
    while True:
        # Check if there's an incoming "close" message to terminate the connection.
        if readable() and read() == "close":
            write(sock, "quit")
            ret = 2

        # Wait for user to click the button to exit the popup.
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 220 < event.pos[0] < 285 and 270 < event.pos[1] < 290:
                    write(sock, "end")
                    return ret


def request(win, sock, key=None):
    """Display a request popup used for game initialization steps.

    Depending on whether the key parameter is None, this either shows a waiting
    screen for the opponent’s response or prompts the local player to accept/decline
    a match request.

    Args:
        win (pygame.Surface): The display surface for rendering the popup.
        sock (socket.socket): The socket for sending/receiving messages.
        key (int, optional): If not None, represents the unique key used for
                             matching players. Defaults to None.

    Returns:
        int: An integer code representing next action (e.g., start, quit, pass, etc.).
    """
    if key is None:
        # Display "waiting for the opponent" message.
        pygame.draw.rect(win, (0, 0, 0), (100, 210, 300, 100))
        pygame.draw.rect(win, (255, 255, 255), (100, 210, 300, 100), 4)
        win.blit(ONLINE.REQUEST1[0], (120, 220))
        win.blit(ONLINE.REQUEST1[1], (105, 245))
        win.blit(ONLINE.REQUEST1[2], (135, 270))
    else:
        # Display a prompt to accept/decline a match request using a key code.
        pygame.draw.rect(win, (0, 0, 0), (100, 160, 300, 130))
        pygame.draw.rect(win, (255, 255, 255), (100, 160, 300, 130), 4)
        win.blit(ONLINE.REQUEST2[0], (110, 175))
        win.blit(ONLINE.REQUEST2[1], (200, 175))
        win.blit(ONLINE.REQUEST2[2], (105, 200))
        putNum(win, key, (160, 175))
        win.blit(ONLINE.OK, (145, 240))
        win.blit(ONLINE.NO, (305, 240))
        pygame.draw.rect(win, (255, 255, 255), (140, 240, 50, 28), 2)
        pygame.draw.rect(win, (255, 255, 255), (300, 240, 50, 28), 2)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            # If user closes game window while waiting, signal a quit.
            if key is None and event.type == pygame.QUIT:
                write(sock, "quit")
                return 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If key is None and user clicks top-right corner, treat it like a quit.
                if key is None and 460 < event.pos[0] < 500 and 0 < event.pos[1] < 50:
                    write(sock, "quit")
                    return 1

                # If key is not None, handle accept (OK) or decline (NO).
                elif key is not None and 240 < event.pos[1] < 270:
                    if 140 < event.pos[0] < 190:
                        return 4  # Accept
                    elif 300 < event.pos[0] < 350:
                        return 3  # Decline

        # Process incoming server messages for starting, closing, or passing.
        if readable():
            msg = read()
            if msg == "close":
                return 2
            if msg == "quit":
                return 3
            if key is None:
                if msg == "nostart":
                    write(sock, "pass")
                    return 3
                if msg == "start":
                    write(sock, "ready")
                    return 4


def draw(win, sock, requester=True):
    """Display a popup to handle draw requests between players.

    Shows either a waiting prompt (if requester=True) or an accept/reject prompt
    (if requester=False).

    Args:
        win (pygame.Surface): The display surface for rendering.
        sock (socket.socket): Socket used for network communication.
        requester (bool, optional): Whether the local player initiated the draw request.
                                    Defaults to True.

    Returns:
        int: Code indicating the result of the request (draw accepted, rejected, or closed).
    """
    if requester:
        # Show 'Waiting for other player's decision about draw.'
        pygame.draw.rect(win, (0, 0, 0), (100, 220, 300, 60))
        pygame.draw.rect(win, (255, 255, 255), (100, 220, 300, 60), 4)
        win.blit(ONLINE.DRAW1[0], (110, 225))
        win.blit(ONLINE.DRAW1[1], (180, 250))
    else:
        # Show accept/reject draw request UI.
        pygame.draw.rect(win, (0, 0, 0), (100, 160, 300, 130))
        pygame.draw.rect(win, (255, 255, 255), (100, 160, 300, 130), 4)
        win.blit(ONLINE.DRAW2[0], (120, 170))
        win.blit(ONLINE.DRAW2[1], (170, 195))
        win.blit(ONLINE.OK, (145, 240))
        win.blit(ONLINE.NO, (305, 240))
        pygame.draw.rect(win, (255, 255, 255), (140, 240, 50, 28), 2)
        pygame.draw.rect(win, (255, 255, 255), (300, 240, 50, 28), 2

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            # If the requester closes the game window, send "quit" signal.
            if requester and event.type == pygame.QUIT:
                write(sock, "quit")
                return 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If local user can accept or reject draw, handle the button click.
                if not requester and 240 < event.pos[1] < 270:
                    if 140 < event.pos[0] < 190:
                        write(sock, "draw")
                        return 3
                    elif 300 < event.pos[0] < 350:
                        write(sock, "nodraw")
                        return 4

        # Check incoming socket messages for the final outcome.
        if readable():
            msg = read()
            if msg == "close":
                return 2
            if msg == "quit":
                # If opponent quits, show popup and end session.
                return popup(win, sock, msg)
            if requester:
                if msg == "draw":
                    # Opponent accepted the draw request.
                    return popup(win, sock, msg)
                if msg == "nodraw":
                    # Opponent declined the draw request.
                    return 4


def showLobby(win, key, playerlist):
    """Render the online Lobby screen, showing the list of active players and statuses.

    Allows the local user to see their own key, other players’ keys, and whether they are
    active or busy. Also provides a request button to challenge other players to a match.

    Args:
        win (pygame.Surface): Surface on which the lobby is displayed.
        key (int): The local player's unique identifier.
        playerlist (list[str]): List of player entries with their key and status.
    """
    win.fill((0, 0, 0))  # Clear the screen to black before drawing UI elements.
    
    # Draw a title, bounding rectangles, and a "Go Back" button.
    win.blit(ONLINE.LOBBY, (100, 14))
    pygame.draw.rect(win, (255, 255, 255), (65, 10, 355, 68), 4)
    win.blit(BACK, (460, 0))
    win.blit(ONLINE.LIST, (20, 75))
    win.blit(ONLINE.REFRESH, (270, 85))
    pygame.draw.line(win, (255, 255, 255), (20, 114), (190, 114), 3)
    pygame.draw.line(win, (255, 255, 255), (210, 114), (265, 114), 3)

    # If no players are present, display an "empty" message.
    if not playerlist:
        win.blit(ONLINE.EMPTY, (25, 130))

    # Display each player's key and status, along with a "request game" button.
    for cnt, player in enumerate(playerlist):
        pkey, stat = int(player[:4]), player[4]
        yCord = 120 + cnt * 30
        
        # Show a numbered listing of players.
        putLargeNum(win, cnt + 1, (20, yCord))
        win.blit(ONLINE.DOT, (36, yCord))
        win.blit(ONLINE.PLAYER, (52, yCord))
        putLargeNum(win, pkey, (132, yCord))

        # Display a status indicator for the current player: Active or Busy.
        if stat == "a":
            win.blit(ONLINE.ACTIVE, (200, yCord))
        elif stat == "b":
            win.blit(ONLINE.BUSY, (200, yCord))

        # Draw the "Request" button to challenge this player.
        pygame.draw.rect(win, (255, 255, 255), (300, yCord + 2, 175, 26), 2)
        win.blit(ONLINE.REQ, (300, yCord))

    # Display the local user’s key in the bottom area of the screen.
    win.blit(ONLINE.YOUARE, (100, 430))
    pygame.draw.rect(win, (255, 255, 255), (250, 435, 158, 40), 3)
    win.blit(ONLINE.PLAYER, (260, 440))
    putLargeNum(win, key, (340, 440))

    pygame.display.update()