# Programming Language: Python
# Project Type: Multiplayer Chess Application Server
# Key Functionalities: Managing client connections, message routing, game session handling, and logging
# Target Users: Developers maintaining or extending the Chess server
# Code Style: PEP8, with Google-style docstrings for functions

"""
Chess Server Module

This module implements an online server for the Multiplayer Chess application.
It manages client connections, facilitates game sessions, logs server activity,
and provides administrative command handling for runtime control.

Usage:
    Run this module directly to start the Chess server. For configuration details,
    see the accompanying documentation (onlinehowto.txt).

Requirements:
    - Python 3.6 or above
"""

import queue
import random
import socket
import threading
import time
from urllib.request import urlopen

# Configurable constants used by the server; users may modify these if they understand the implications.
LOG = False
IPV6 = False

# Server version and network configuration parameters.
VERSION = "v1.0"
PORT = 26104
START_TIME = time.perf_counter()
LOGFILENAME = time.asctime().replace(" ", "_").replace(":", "-")

# Global variables that track connected clients and server state.
busyPpl = set()    # Set of player keys currently busy in a game
end = False        # Flag to indicate server shutdown
lock = False       # Flag to lock the server (prevent new connections)
logQ = queue.Queue()   # Queue to buffer log output
players = []       # List of connected players as tuples (socket, key)
total = totalsuccess = 0  # Statistics for total and successful connection attempts

def makeInt(num):
    """Convert a string to an integer safely.

    Args:
        num (str): The input string representing a number.

    Returns:
        int or None: The converted integer or None if conversion fails.
    """
    try:
        return int(num)
    except ValueError:
        return None

def getTime():
    """Calculate the elapsed time since the server started.

    Returns:
        str: A human-readable string expressing the time elapsed.
    """
    sec = round(time.perf_counter() - START_TIME)
    minutes, sec = divmod(sec, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days} days, {hours} hours, {minutes} minutes, {sec} seconds"

def getIp(public):
    """Retrieve the public or private IP address of the server.

    Args:
        public (bool): If True, fetch the public IP; otherwise, get the local address.

    Returns:
        str: The detected IP address. Falls back to '127.0.0.1' on error.
    """
    if public:
        try:
            ip = urlopen("https://api64.ipify.org").read().decode()
        except Exception:
            ip = "127.0.0.1"
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.connect(('10.255.255.255', 1))
                ip = s.getsockname()[0]
            except Exception:
                ip = '127.0.0.1'
    return ip

def log(data, key=None, adminput=False):
    """Log messages with context for both players and administrative commands.

    Args:
        data (str or None): Message string. If None, signals end of logging.
        key (int or None): Player key for contextual logging; default is None.
        adminput (bool): If True, indicates an administrator command.
    """
    global logQ
    # Construct message header based on the origin of the log message.
    if adminput:
        text = ""
    elif key is None:
        text = "SERVER: "
    else:
        text = f"Player{key}: "
    
    if data is not None:
        text += data
        # Print non-admin messages to stdout for real-time feedback.
        if not adminput:
            print(text)
        # Buffer the log message if logging is enabled.
        if LOG:
            logQ.put(time.asctime() + ": " + text + "\n")
    else:
        # None signals termination of the logging thread.
        logQ.put(None)

def read(sock, timeout=None):
    """Receive and decode a message from a client socket.

    This function handles timeouts and ensures the message is properly formatted.
    
    Args:
        sock (socket.socket): The client socket.
        timeout (float, optional): Timeout duration in seconds.

    Returns:
        str: The decoded message or "quit" if an error occurs.
    """
    try:
        sock.settimeout(timeout)
        msg = sock.recv(8).decode("utf-8").strip()
    except Exception:
        msg = "quit"
    return msg if msg else "quit"
 
def write(sock, msg):
    """Send a message to the specified client socket with fixed-length padding.

    This wrapper ensures that messages are sent in a consistent 8-byte format
    to handle TCP packet fragmentation and potential packet loss gracefully.

    Args:
        sock (socket.socket): The target client socket.
        msg (str): The message to be sent.
    """
    if msg:
        buffedmsg = msg + (" " * (8 - len(msg)))  # Pad message to 8 characters.
        try:
            sock.sendall(buffedmsg.encode("utf-8"))
        except Exception:
            pass

def genKey():
    """Generate a unique 4-digit key for a new player.

    Iteratively generates a random key and checks that it isn't assigned to another player.

    Returns:
        int: A unique player key.
    """
    key = random.randint(1000, 9999)
    for player in players:
        if player[1] == key:
            # Recursively generate a new key if collision occurs.
            return genKey()
    return key

def getByKey(key):
    """Retrieve the socket corresponding to the given player key.

    Args:
        key (str or int): The player's key.

    Returns:
        socket.socket or None: The player's socket if found; otherwise, None.
    """
    for player in players:
        if player[1] == makeInt(key):
            return player[0]

def mkBusy(*keys):
    """Mark one or more players as busy (engaged in a game).

    Args:
        *keys: Variable length player keys.
    """
    global busyPpl
    for key in keys:
        busyPpl.add(makeInt(key))

def rmBusy(*keys):
    """Mark one or more players as no longer busy.

    Args:
        *keys: Variable length player keys.
    """
    global busyPpl
    for key in keys:
        busyPpl.discard(makeInt(key))

def game(sock1, sock2):
    """Facilitate message exchange between two players during a game session.

    This function relays messages from one player's socket to the other's until
    the game ends or one player sends "quit".

    Args:
        sock1 (socket.socket): Socket of the initiating player.
        sock2 (socket.socket): Socket of the opponent.

    Returns:
        bool: True if a disconnection occurred during the match; False otherwise.
    """
    while True:
        msg = read(sock1)
        write(sock2, msg)
        if msg == "quit":
            return True
        elif msg in ["draw", "resign", "end"]:
            return False

def player(sock, key):
    """Handle continuous communication with a connected client.

    Processes various commands received from the client including game requests,
    state inquiries, and disconnection notifications.

    Args:
        sock (socket.socket): The client's socket.
        key (int): The unique key assigned to the player.
    """
    while True:
        msg = read(sock)
        if msg == "quit":
            return
        elif msg == "pStat":
            log("Request for player statistics received.", key)
            latestplayers = list(players)
            latestbusy = list(busyPpl)
            # Allow status reporting only when player count is within reasonable limits.
            if 0 < len(latestplayers) < 11:
                write(sock, "enum" + str(len(latestplayers) - 1))
                for _, i in latestplayers:
                    if i != key:
                        # Append status indicator: "b" for busy, "a" for active.
                        write(sock, str(i) + ("b" if i in latestbusy else "a"))
        elif msg.startswith("rg"):
            log(f"Received game request to play with Player{msg[2:]}", key)
            oSock = getByKey(msg[2:])
            if oSock is not None:
                if makeInt(msg[2:]) not in busyPpl:
                    mkBusy(key, msg[2:])
                    write(oSock, "gr" + str(key))
                    write(sock, "msgOk")
                    newMsg = read(sock)
                    if newMsg == "ready":
                        log(f"Player{key} starting game as white")
                        if game(sock, oSock):
                            return
                        else:
                            log(f"Player{key} completed the game")
                    elif newMsg == "quit":
                        write(oSock, "quit")
                        return
                    rmBusy(key)
                else:
                    log(f"Player{key} attempted game request to busy player", key)
                    write(sock, "errPBusy")
            else:
                log(f"Player{key} sent an invalid key", key)
                write(sock, "errKey")
        elif msg.startswith("gmOk"):
            log(f"Accepted game request from Player{msg[4:]}", key)
            oSock = getByKey(msg[4:])
            write(oSock, "start")
            log(f"Player{key} starting game as black", key)
            if game(sock, oSock):
                return
            else:
                log(f"Player{key} completed the game", key)
                rmBusy(key)
        elif msg.startswith("gmNo"):
            log(f"Rejected game request from Player{msg[4:]}", key)
            write(getByKey(msg[4:]), "nostart")
            rmBusy(key)

def logThread():
    """Continuously flush log messages from the buffer to a server log file.

    This background thread ensures that all log messages are written to disk.
    When a None message is encountered, the thread terminates.
    """
    global logQ
    while True:
        time.sleep(1)
        with open("SERVER_LOG_" + LOGFILENAME + ".txt", "a") as f:
            while not logQ.empty():
                data = logQ.get()
                if data is None:
                    return
                else:
                    f.write(data)

def kickDisconnectedThread():
    """Periodically check for and remove disconnected clients.

    This background thread iterates over the list of players and attempts a
    non-intrusive message send. If a client does not respond properly, the player
    is removed from the active list.
    """
    global players
    while True:
        time.sleep(10)
        for sock, key in players.copy():
            try:
                ret = sock.send(b"........")
            except Exception:
                ret = 0
            if ret > 0:
                cntr = 0
                diff = 8
                while True:
                    cntr += 1
                    if cntr == 8:
                        ret = 0
                        break
                    if ret == diff:
                        break
                    diff -= ret
                    try:
                        ret = sock.send(b"." * diff)
                    except Exception:
                        ret = 0
                        break
            if ret == 0:
                log(f"Player{key} disconnected. Removing from active players list.")
                try:
                    players.remove((sock, key))
                except Exception:
                    pass

def adminThread():
    """Process administrative commands entered via the server console.

    This thread handles runtime admin commands such as 'report', 'kick', 'lock', and 'quit'.
    It provides real-time logging and feedback for server management.
    """
    global end, lock
    while True:
        msg = input().strip()
        log(msg, adminput=True)
        if msg == "report":
            log(f"{len(players)} players online; {len(players) - len(busyPpl)} active.")
            log(f"{total} connection attempts, {totalsuccess} successful")
            log(f"Active threads: {threading.active_count()}")
            log(f"Uptime: {getTime()}")
            if players:
                log("Connected Players:")
                for cnt, (_, player) in enumerate(players):
                    status = "Busy" if player in busyPpl else "Active"
                    log(f" {cnt+1}. Player{player} - Status: {status}")
        elif msg == "mypublicip":
            log("Determining public IP; please wait...")
            PUBIP = getIp(public=True)
            if PUBIP == "127.0.0.1":
                log("Error: Unable to determine public IP.")
            else:
                log(f"Public IP: {PUBIP}")
        elif msg == "lock":
            if lock:
                log("Server is already locked.")
            else:
                lock = True
                log("Server locked: New connections are now blocked.")
        elif msg == "unlock":
            if lock:
                lock = False
                log("Server unlocked: New connections are now accepted.")
            else:
                log("Server is already in an unlocked state.")
        elif msg.startswith("kick "):
            for k in msg[5:].split():
                sock = getByKey(k)
                if sock is not None:
                    write(sock, "close")
                    log(f"Kicking Player{k}")
                else:
                    log(f"Player{k} does not exist.")
        elif msg == "kickall":
            log("Kicking all connected players.")
            for sock, _ in players.copy():
                write(sock, "close")
        elif msg == "quit":
            lock = True
            log("Kicking all players and shutting down server.")
            for sock, _ in players.copy():
                write(sock, "close")
            log("Exiting application – Goodbye!")
            log(None)  # Signal log thread termination.
            end = True
            # Connect to self to unblock the main accept loop.
            if IPV6:
                with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
                    s.connect(("::1", PORT, 0, 0))
            else:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(("127.0.0.1", PORT))
            return
        else:
            log(f"Invalid command: '{msg}'. Refer to 'onlinehowto.txt' for command usage.")

def initPlayerThread(sock):
    """Handle a new client connection and perform initial handshake.

    Responsible for basic validation of the connection header and version,
    managing player limits, and adding the validated client to the active list.

    Args:
        sock (socket.socket): The client's socket connection.
    """
    global players, total, totalsuccess
    log("New client attempting to connect.")
    total += 1
    # Check client's protocol header.
    if read(sock, 3) != "PyChess":
        log("Invalid client header; closing connection.")
        write(sock, "errVer")
    elif read(sock, 3) != VERSION:
        log("Client version mismatch; closing connection.")
        write(sock, "errVer")
    elif len(players) >= 10:
        log("Server busy; rejecting connection.")
        write(sock, "errBusy")
    elif lock:
        log("Server locked; rejecting new connection.")
        write(sock, "errLock")
    else:
        totalsuccess += 1
        key = genKey()
        log(f"Connection successful. Assigned key: {key}")
        players.append((sock, key))
        write(sock, "key" + str(key))
        player(sock, key)
        write(sock, "close")
        log(f"Player{key} has disconnected.")
        try:
            players.remove((sock, key))
        except Exception:
            pass
        rmBusy(key)
    sock.close()


# Main server socket initialization and configuration.
log(f"Welcome to Chess Server, {VERSION}\n")
log("Initializing server...")

if IPV6:
    log("IPv6 configuration enabled (non-default).")
    mainSock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    mainSock.bind(("::", PORT, 0, 0))
else:
    log("Using default IPv4 configuration.")
    mainSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mainSock.bind(("0.0.0.0", PORT))
    IP = getIp(public=False)
    if IP == "127.0.0.1":
        log("Warning: Machine appears to be offline; only local clients can connect (127.0.0.1).")
    else:
        log(f"Local IP detected: {IP}")
        log("For local clients, please use this IP address.")
    
mainSock.listen(16)
log(f"Server listening on port {PORT}\n")

# Start background threads for admin commands and client management.
threading.Thread(target=adminThread).start()
threading.Thread(target=kickDisconnectedThread, daemon=True).start()
if LOG:
    log("Logging enabled. Starting log thread.")
    threading.Thread(target=logThread).start()

# Main loop: Accept new client connections until server shutdown is signaled.
while True:
    s, _ = mainSock.accept()
    if end:
        break
    threading.Thread(target=initPlayerThread, args=(s,), daemon=True).start()

mainSock.close()