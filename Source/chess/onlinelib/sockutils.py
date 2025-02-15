"""
This file is part of the Chess application.
It provides utility functions and wrappers for socket-related operations, including:
 - A background thread to continuously read messages from the server
 - Convenience methods for sending, receiving, and flushing messages
 - Helper functions to track and list connected players
"""

import queue
import socket

# Queue used as an in-memory buffer to safely handle incoming messages from the server.
q = queue.Queue()

# Indicates whether the background thread is still running (False) or has stopped (True).
# Combined with q.empty(), it shows if there's any pending or new message.
isdead = True


def bgThread(sock):
    """Continuously receive messages from the server and store them in a shared queue.

    Once this thread terminates or detects a 'close' signal from the server, it will
    mark the connection as dead. Messages are limited by size to 8 bytes at a time.

    Args:
        sock (socket.socket): An open socket connected to the server.
    """
    global isdead
    isdead = False
    while True:
        try:
            msg = sock.recv(8).decode("utf-8").strip()
        except:
            # If an exception occurs (e.g., socket error), break out of the loop.
            break

        # Detect an empty or "close" message, signifying a disconnect intention.
        if not msg or msg == "close":
            break

        # Ignore placeholder messages that contain only dots.
        if msg != "........":
            q.put(msg)

    isdead = True


def isDead():
    """Check if the background thread has finished and the message queue is empty.

    Returns:
        bool: True if no active thread is reading messages and the buffer has no messages left.
    """
    return q.empty() and isdead


def read():
    """Retrieve the next message from the queue if available.

    If the background thread is dead and no messages remain, return 'close'
    to indicate the connection is effectively closed.

    Returns:
        str: The next message from the queue, or 'close' if the thread is dead and buffer is empty.
    """
    if isDead():
        return "close"
    return q.get()


def readable():
    """Determine if any messages are available or if the connection has ended.

    Returns:
        bool: True if the connection is dead (so 'close' is effectively readable) or if
        a message exists in the queue; otherwise False.
    """
    if isDead():
        return True
    return not q.empty()


def flush():
    """Clear any pending messages in the queue until it is empty or a 'close' is encountered.

    Returns:
        bool: False if a 'close' signal is found in the process (indicating disconnection),
              True otherwise.
    """
    while readable():
        if read() == "close":
            return False
    return True


def write(sock, msg):
    """Send a message to the server, ensuring correct padding and ignoring send failures.

    This function pads messages to a fixed size (8 bytes). It intentionally catches
    errors, avoiding exceptions if sending fails.

    Args:
        sock (socket.socket): An open socket connected to the server.
        msg (str): The message to send. If empty, no data is sent.
    """
    if msg:
        buffedmsg = msg + (" " * (8 - len(msg)))
        try:
            sock.sendall(buffedmsg.encode("utf-8"))
        except:
            pass


def getPlayers(sock):
    """Request the current list of players from the server and read the results.

    If the flush operation encounters a 'close' signal, or if the server closes
    mid-request, this function will return None.

    Args:
        sock (socket.socket): The socket used to query the server.

    Returns:
        tuple or None: A tuple of player info strings if successful, or None on failure.
    """
    if not flush():
        return None

    write(sock, "pStat")
    msg = read()

    if msg.startswith("enum"):
        data = []
        # The last character in "enumX" indicates how many players to read from the queue.
        for _ in range(int(msg[-1])):
            newmsg = read()
            if newmsg == "close":
                return None
            else:
                data.append(newmsg)
        return tuple(data)

    return None