# Programming Language: Python
# Project Type: Multiplayer Chess Game
# Key Functionalities: Managing online chess gameplay, socket connection initialization,
#                      background thread management, and error handling for online lobby.
# Target Users: Developers maintaining or extending the Chess application.
# Code Style: PEP8 with Google-style docstrings and inline comments

'''
This file is a part of the Chess application.
It manages the chess gameplay for the online section of the application by initializing
socket connections to the server, handling background thread communication, and invoking
the lobby interface. It uses functions from the online library for connection handling.
See [chess.onlinelib](Source/chess/onlinelib) for more details.
'''

import socket
import threading

from chess.onlinelib import showLoading, write, read, lobby, flush, bgThread  # Reference to [chess.onlinelib](Source/chess/onlinelib)

VERSION = "v1.0"  # Application version for online compatibility checks.
PORT = 26104      # Network port to connect to the chess server.

def main(win, addr, load, ipv6=False):
    """Initialize the online chess session and transition to the online lobby.

    This function displays a loading screen, establishes a socket connection
    (IPv4 or IPv6 based on the parameter), launches a background thread to handle
    asynchronous communication, and invokes the lobby interface based on server response.
    Appropriate error messages are shown for version mismatches, server busy state,
    or if the server is locked.

    Args:
        win (pygame.Surface): The display surface where loading screens and messages are shown.
        addr (str): The server address to connect to.
        load (dict): User configuration loaded from preferences to pass to the lobby.
        ipv6 (bool, optional): Flag indicating whether to use IPv6. Defaults to False.

    Returns:
        int: Status code indicating outcome. Returns 1 for errors or when the back button is selected,
             or a different integer based on further lobby interactions.
    """
    # Show initial loading screen before starting connection.
    showLoading(win)
    
    # Create a socket using IPv6 or IPv4 depending on the flag.
    if ipv6:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        servaddr = (addr, PORT, 0, 0)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servaddr = (addr, PORT)

    try:
        # Attempt to connect to the server.
        sock.connect(servaddr)
    except Exception:
        # If connection fails, show error loading screen with error code 1.
        showLoading(win, 1)
        return 1

    # Start a background thread for asynchronous communication.
    thread = threading.Thread(target=bgThread, args=(sock,))
    thread.start()
    
    # Send application identifier and version over the socket.
    write(sock, "PyChess")
    write(sock, VERSION)

    ret = 1  # Default return code for error scenarios.
    msg = read()  # Read the response from the server.
    
    # Process server response according to protocol.
    if msg == "errVer":
        # Version mismatch error.
        showLoading(win, 2)
    elif msg == "errBusy":
        # Server is busy.
        showLoading(win, 3)
    elif msg == "errLock":
        # Server locked; likely a resource or access issue.
        showLoading(win, 4)
    elif msg.startswith("key"):
        # Valid response: extract key value and launch the lobby interface.
        ret = lobby(win, sock, int(msg[3:]), load)
    else:
        # Unhandled message from server; log details and display error.
        print(msg)
        showLoading(win, 5)

    # Terminate the connection by signaling a quit message.
    write(sock, "quit")
    sock.close()
    thread.join()
    flush()  # Clear any buffered network data.

    # If lobby returns a code indicating special handling, display appropriate loading screen.
    if ret == 2:
        showLoading(win, -1)
        return 1
    return ret