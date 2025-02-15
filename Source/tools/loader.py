# Programming Language: Python
# Project Type: Multiplayer Chess Game
# Key Functionalities: Loading images, fonts, texts, and graphical resources for the Chess application.
# Target Users: Developers maintaining or extending the Chess application.
# Code Style: PEP8 with Google-style docstrings and inline comments

"""
This module loads all the images, font resources, and texts used across the Chess application.

It provides a centralized repository of graphical resources and helper functions to render
numbers and date-time strings on the screen. Additionally, the module organizes related texts
and images into classes for easy access by various parts of the application.
"""

import os.path
import pygame

# Initialize the pygame.font module so that fonts can be loaded.
pygame.font.init()

# Set the path for the custom font used in the application.
FONT = os.path.join("res", "Asimov.otf")

# Load fonts in various sizes for different UI elements.
head = pygame.font.Font(FONT, 80)
large = pygame.font.Font(FONT, 50)
medium = pygame.font.Font(FONT, 38)
small = pygame.font.Font(FONT, 27)
vsmall = pygame.font.Font(FONT, 17)

# Define common RGB color constants for drawing text and graphics.
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (200, 20, 20)

# Pre-render numeric characters and common punctuation for performance.
NUM = [vsmall.render(str(i), True, WHITE) for i in range(10)]
LNUM = [small.render(str(i), True, WHITE) for i in range(10)]
BLNUM = [small.render(str(i), True, BLACK) for i in range(10)]
SLASH = vsmall.render("/", True, WHITE)
COLON = vsmall.render(":", True, WHITE)

def putNum(win, num, pos):
    """
    Render a number string on the specified surface using very small font.

    This function iterates over each character in the number, rendering it individually.
    
    Args:
        win (pygame.Surface): Surface on which the number will be drawn.
        num (int or str): The number to be rendered.
        pos (tuple): The (x, y) coordinates where the first digit will be placed.
    """
    for cnt, i in enumerate(list(str(num))):
        # Offset each digit to avoid visual overlap.
        win.blit(NUM[int(i)], (pos[0] + (cnt * 9), pos[1]))

def putLargeNum(win, num, pos, white=True):
    """
    Render a number string on the specified surface using a larger font.

    The function chooses between white or black colored numbers based on the flag.
    
    Args:
        win (pygame.Surface): Surface on which the number will be drawn.
        num (int or str): The number to be rendered.
        pos (tuple): The (x, y) coordinates where the first digit will be placed.
        white (bool): If True, renders the number in white; otherwise, in black.
    """
    for cnt, i in enumerate(list(str(num))):
        color_choice = LNUM if white else BLNUM
        win.blit(color_choice[int(i)], (pos[0] + (cnt * 14), pos[1]))

def putDT(win, DT, pos):
    """
    Display a formatted date and time string on the provided surface.

    The date-time string is expected to have a format of "dd/mm/yyyy hh:mm:ss".
    It splits the string into date and time components, renders each part, and
    places slashes and colons accordingly to maintain the expected formatting.
    
    Args:
        win (pygame.Surface): Surface on which the date-time string will be drawn.
        DT (str): A string representing date and time (e.g., "31/12/2022 23:59:59").
        pos (tuple): The starting (x, y) coordinates for the date portion.
    """
    var = DT.split()  # Split into [date, time]
    date = var[0].split("/")
    time_part = var[1].split(":")

    # Render each date segment with appropriate spacing.
    for cnt, num in enumerate(map(lambda x: format(int(x), "02"), date)):
        putNum(win, num, (pos[0] + 24 * cnt - 5, pos[1]))

    # Render the slash separators between day, month, and year.
    win.blit(SLASH, (pos[0] + 13, pos[1]))
    win.blit(SLASH, (pos[0] + 35, pos[1]))

    # Render each time segment (hours, minutes, seconds) below the date.
    for cnt, num in enumerate(map(lambda x: format(int(x), "02"), time_part)):
        putNum(win, num, (pos[0] + 24 * cnt, pos[1] + 21))

    # Render the colon separators between hours, minutes, and seconds.
    win.blit(COLON, (pos[0] + 20, pos[1] + 21))
    win.blit(COLON, (pos[0] + 44, pos[1] + 21))

def splitstr(string, index=57):
    """
    Split a string into a list of substrings each with a maximum length specified by index.

    Args:
        string (str): The string to be split.
        index (int, optional): Maximum length of each substring. Defaults to 57.

    Returns:
        list[str]: A list of substrings.
    """
    data = []
    while len(string) >= index:
        data.append(string[:index])
        string = string[index:]
    data.append(string)
    return data

# Load background image sprites and other images required by the application.
BGSPRITE = pygame.image.load(os.path.join("res", "img", "bgsprites.jpg"))
PSPRITE = pygame.image.load(os.path.join("res", "img", "piecesprite.png"))
BACK = pygame.image.load(os.path.join("res", "img", "back.png"))

class CHESS:
    """
    Container class for chess-specific resources such as piece images and game status texts.
    
    Attributes:
        PIECES (tuple): A tuple of two dictionaries mapping piece types to their sprite subsurfaces
                        for each side.
        CHECK, STALEMATE, CHECKMATE, LOST: Rendered texts to indicate game status.
        CHOOSE, SAVE, UNDO: Rendered texts for in-game menu options.
        MESSAGE, MESSAGE2, YES, NO: Rendered messages for in-game prompts.
        TURN: Tuple indicating turn status messages.
        DRAW, RESIGN: Rendered texts for draw and resign actions.
        TIMEUP: Tuple of rendered texts indicating time-up scenarios.
        OK, COL: Rendered texts for menu navigation.
    """
    PIECES = ({}, {})
    for i, ptype in enumerate(["k", "q", "b", "n", "r", "p"]):
        for side in range(2):
            # Extract each piece's image from the general pieces sprite.
            PIECES[side][ptype] = PSPRITE.subsurface((i * 50, side * 50, 50, 50))

    CHECK = small.render("CHECK!", True, BLACK)
    STALEMATE = small.render("STALEMATE!", True, BLACK)
    CHECKMATE = small.render("CHECKMATE!", True, BLACK)
    LOST = small.render("LOST", True, BLACK)
    CHOOSE = small.render("CHOOSE:", True, BLACK)
    SAVE = small.render("Save Game", True, BLACK)
    UNDO = small.render("Undo", True, BLACK)

    MESSAGE = (
        small.render("Do you want to quit", True, WHITE),
        small.render("this game?", True, WHITE),
    )

    MESSAGE2 = (
        small.render("Game saved. Now do", True, WHITE),
        small.render("you want to quit?", True, WHITE),
    )

    YES = small.render("YES", True, WHITE)
    NO = small.render("NO", True, WHITE)
    MSG = vsmall.render("Game will be saved with ID", True, WHITE)
    SAVE_ERR = vsmall.render("ERROR: SaveGame Limit Exeeded", True, WHITE)

    TURN = (
        small.render("Others turn", True, BLACK),
        small.render("Your turn", True, BLACK),
    )

    DRAW = small.render("Draw", True, BLACK)
    RESIGN = small.render("Resign", True, BLACK)

    TIMEUP = (
        vsmall.render("Time Up!", True, WHITE),
        vsmall.render("Technically the game is over, but you", True, WHITE),
        vsmall.render("can still continue if you wish to - :)", True, WHITE),
    )

    OK = small.render("Ok", True, WHITE)
    COL = small.render(":", True, BLACK)

class LOADGAME:
    """
    Contains texts and images for the "Load Game" menu interface.
    
    It includes headings, game list displays, deletion confirmations, and navigation controls.
    """
    HEAD = large.render("Load Games", True, WHITE)
    LIST = medium.render("List of Games", True, WHITE)
    EMPTY = small.render("There are no saved games yet.....", True, WHITE)
    GAME = small.render("Game", True, WHITE)
    TYPHEAD = vsmall.render("Game Type:", True, WHITE)
    TYP = {
        "single": vsmall.render("SinglePlayer", True, WHITE),
        "mysingle": vsmall.render("SinglePlayer", True, WHITE),
        "multi": vsmall.render("MultiPlayer", True, WHITE),
    }
    DATE = vsmall.render("Date-", True, WHITE)
    TIME = vsmall.render("Time-", True, WHITE)

    DEL = pygame.image.load(os.path.join("res", "img", "delete.jpg"))
    LOAD = small.render("LOAD", True, WHITE)

    MESSAGE = (
        small.render("Are you sure that you", True, WHITE),
        small.render("want to delete game?", True, WHITE),
    )
    YES = small.render("YES", True, WHITE)
    NO = small.render("NO", True, WHITE)

    LEFT = medium.render("<", True, WHITE)
    RIGHT = medium.render(">", True, WHITE)
    PAGE = [medium.render("Page " + str(i), True, WHITE) for i in range(1, 5)]

class MAIN:
    """
    Contains primary texts and icons used in the main menu of the Chess application.
    """
    HEADING = head.render("Py-Chess", True, WHITE)
    VERSION = vsmall.render("Version 1.0", True, WHITE)
    ICON = pygame.image.load(os.path.join("res", "img", "icon.gif"))
    BG = [BGSPRITE.subsurface((i * 500, 0, 500, 500)) for i in range(4)]

    SINGLE = medium.render("SinglePlayer", True, WHITE)
    MULTI = medium.render("MultiPlayer", True, WHITE)
    ONLINE = medium.render("Online", True, WHITE)
    LOAD = medium.render("Load Game", True, WHITE)
    HOWTO = small.render("Howto", True, WHITE)
    ABOUT = medium.render("About", True, WHITE)
    PREF = medium.render("Preferences", True, WHITE)
    STOCK = small.render("Configure Stockfish", True, WHITE)

    SINGLE_H = medium.render("SinglePlayer", True, GREY)
    MULTI_H = medium.render("MultiPlayer", True, GREY)
    ONLINE_H = medium.render("Online", True, GREY)
    LOAD_H = medium.render("Load Game", True, GREY)
    HOWTO_H = small.render("Howto", True, GREY)
    ABOUT_H = medium.render("About", True, GREY)
    PREF_H = medium.render("Preferences", True, GREY)
    STOCK_H = small.render("Configure Stockfish", True, GREY)

class PREF:
    """
    Defines texts and options for the Preferences menu.
    """
    HEAD = large.render("Preferences", True, WHITE)

    SOUNDS = medium.render("Sounds", True, WHITE)
    FLIP = medium.render("Flip screen", True, WHITE)
    CLOCK = medium.render("Show Clock", True, WHITE)
    SLIDESHOW = medium.render("Slideshow", True, WHITE)
    MOVE = medium.render("Moves", True, WHITE)
    UNDO = medium.render("Allow undo", True, WHITE)

    COLON = medium.render(":", True, WHITE)

    TRUE = medium.render("True", True, WHITE)
    FALSE = medium.render("False", True, WHITE)

    SOUNDS_H = (
        vsmall.render("Play different sounds", True, WHITE),
        vsmall.render("and music", True, WHITE),
    )
    FLIP_H = (
        vsmall.render("This flips the screen", True, WHITE),
        vsmall.render("after each move", True, WHITE),
    )
    CLOCK_H = (
        vsmall.render("Show a clock in chess", True, WHITE),
        vsmall.render("when timer is disabled", True, WHITE),
    )
    SLIDESHOW_H = (
        vsmall.render("This shows a slide of", True, WHITE),
        vsmall.render("backgrounds on screen", True, WHITE),
    )
    MOVE_H = (
        vsmall.render("This shows all the legal", True, WHITE),
        vsmall.render("moves of a selected piece", True, WHITE),
    )
    UNDO_H = (
        vsmall.render("This allows undo if", True, WHITE),
        vsmall.render("set to be true", True, WHITE),
    )

    BSAVE = medium.render("Save", True, WHITE)
    TIP = vsmall.render("TIP: Hover the mouse over the feature", True, WHITE)
    TIP2 = vsmall.render("name to know more about it.", True, WHITE)

    PROMPT = (
        vsmall.render("Are you sure you want to leave?", True, WHITE),
        vsmall.render("Any changes will not be saved.", True, WHITE),
    )

    YES = small.render("YES", True, WHITE)
    NO = small.render("NO", True, WHITE)

class ONLINE:
    """
    Holds resources and texts for the Online Lobby functionality.
    """
    ERR = (
        vsmall.render("Attempting to connect to server..", True, WHITE),
        vsmall.render("[ERR 1] Couldn't find the server..", True, WHITE),
        vsmall.render("[ERR 2] Versions are incompatible..", True, WHITE),
        vsmall.render("[ERR 3] Server is full (max = 10)..", True, WHITE),
        vsmall.render("[ERR 4] The server is locked...", True, WHITE),
        vsmall.render("[ERR 5] Unknown error occurred...", True, WHITE),
        vsmall.render("You got disconnected from server..", True, WHITE),
    )
    GOBACK = vsmall.render("Go Back", True, WHITE)
    EMPTY = small.render("No one's online, you are alone.", True, WHITE)

    LOBBY = large.render("Online Lobby", True, WHITE)
    LIST = medium.render("List of Players", True, WHITE)
    PLAYER = small.render("Player", True, WHITE)
    DOT = small.render(".", True, WHITE)

    ACTIVE = small.render("ACTIVE", True, GREEN)
    BUSY = small.render("BUSY", True, RED)
    REQ = small.render("Send Request", True, WHITE)
    YOUARE = medium.render("You Are", True, WHITE)
    
    ERRCONN = vsmall.render("Unable to connect to that player..", True, WHITE)
    REFRESH = pygame.image.load(os.path.join("res", "img", "refresh.png"))

    REQUEST1 = (
        vsmall.render("Please wait for the other player to", True, WHITE),
        vsmall.render("accept your request. Game will begin", True, WHITE),
        vsmall.render("shortly. You will play as white", True, WHITE),
    )
    REQUEST2 = (
        vsmall.render("Player", True, WHITE),
        vsmall.render("wants to play with you.", True, WHITE),
        vsmall.render("Accept to play. You will play as black", True, WHITE),
    )

    DRAW1 = (
        vsmall.render("Sent a request to your opponent for", True, WHITE),
        vsmall.render("draw, wait for reply.", True, WHITE),
    )

    DRAW2 = (
        vsmall.render("Your opponent is requesting for a", True, WHITE),
        vsmall.render("draw, please reply.", True, WHITE),
    )
    
    POPUP = {
        "quit": vsmall.render("Opponent got disconnected", True, WHITE),
        "resign": vsmall.render("The opponent has resigned", True, WHITE),
        "draw": vsmall.render("A draw has been agreed", True, WHITE),
        "end": vsmall.render("Game ended, opponent left", True, WHITE),
        "abandon": vsmall.render("Opponent abandoned match", True, WHITE),
    }

    NO = small.render("NO", True, WHITE)
    OK = small.render("OK", True, WHITE)

class ONLINEMENU:
    """
    Resources for the online menu interface.
    """
    HEAD = large.render("Online", True, WHITE)
    with open(os.path.join("res", "texts", "online.txt")) as f:
        TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]
    CONNECT = small.render("Connect", True, WHITE)

class SINGLE:
    """
    Contains UI texts and images for the Singleplayer menu.
    """
    HEAD = large.render("Singleplayer", True, WHITE)
    SELECT = pygame.image.load(os.path.join("res", "img", "select.jpg"))
    CHOOSE = small.render("Choose:", True, WHITE)
    START = small.render("Start Game", True, WHITE)
    OR = medium.render("OR", True, WHITE)
    
    with open(os.path.join("res", "texts", "single1.txt")) as f:
        PARA1 = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]

    with open(os.path.join("res", "texts", "single2.txt")) as f:
        PARA2 = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]
        
    LEVEL = small.render("Level:", True, WHITE)
    BACK = vsmall.render("Go Back", True, WHITE)
    _CONFIG = (
        "It looks like you have not configured",
        "stockfish. To play, you have to do",
        "that.",
    )
    CONFIG = [vsmall.render(i, True, WHITE) for i in _CONFIG]
    OK = vsmall.render("Ok", True, WHITE)
    NOTNOW = vsmall.render("Not Now", True, WHITE)

class STOCKFISH:
    """
    Provides texts and instructions for configuring the Stockfish engine.
    """
    HEAD = large.render("Stockfish Engine", True, WHITE)
    CONFIG = small.render("Configure Stockfish", True, WHITE)
    with open(os.path.join("res", "texts", "stockfish", "stockfish.txt"), "r") as f:
        TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]

    with open(os.path.join("res", "texts", "stockfish", "configd.txt"), "r") as f:
        CONFIGURED = [vsmall.render(i, True, GREEN) for i in f.read().splitlines()]

    with open(os.path.join("res", "texts", "stockfish", "nonconfigd.txt"), "r") as f:
        NONCONFIGURED = [vsmall.render(i, True, RED) for i in f.read().splitlines()]

    CLICK = vsmall.render("Click Here", True, WHITE)
    BACK = vsmall.render("Go Back", True, WHITE)
    INSTALL = small.render("Install", True, WHITE)
    TEST = vsmall.render(
        "After all steps are complete, press button below.", True, WHITE
    )

    WIN_HEAD = small.render("Installation Guide for Windows", True, WHITE)
    LIN_HEAD = small.render("Installation Guide for Linux -", True, WHITE)
    MAC_HEAD = small.render("Installation Guide for Mac", True, WHITE)
    OTH_HEAD = small.render("Installation Guide for Other OS", True, WHITE)

    with open(os.path.join("res", "texts", "stockfish", "win.txt"), "r") as f:
        WIN_TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]

    with open(os.path.join("res", "texts", "stockfish", "linux.txt"), "r") as f:
        LIN_TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]

    with open(os.path.join("res", "texts", "stockfish", "linux2.txt"), "r") as f:
        LIN_TEXT2 = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]

    with open(os.path.join("res", "texts", "stockfish", "mac.txt"), "r") as f:
        MAC_TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]

    with open(os.path.join("res", "texts", "stockfish", "other.txt"), "r") as f:
        OTH_TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]

    # Append full paths split into shorter lines for display purposes.
    for line in splitstr(os.path.abspath("res/stockfish/build/stockfish.exe")):
        WIN_TEXT.append(vsmall.render(line, True, WHITE))

    for line in splitstr(os.path.abspath("res/stockfish/build/stockfish")):
        LIN_TEXT2.append(vsmall.render(line, True, WHITE))
        OTH_TEXT.append(vsmall.render(line, True, WHITE))

    LOADING = head.render("Loading", True, WHITE)
    _SUCCESS = ("Setup successful, now you can go", "back and play chess.")
    _NOSUCCESS = (
        "Setup unsuccessful, try to re-",
        "configure. Follow instructions",
        "carefully and try again.",
    )
    SUCCESS = [vsmall.render(i, True, GREEN) for i in _SUCCESS]
    NOSUCCESS = [vsmall.render(i, True, RED) for i in _NOSUCCESS]
    
    PROMPT = (
        small.render("Do you want to quit?", True, WHITE),
        vsmall.render("Stockfish is not configured yet.", True, WHITE)
    )
    YES = small.render("Yes", True, WHITE)
    NO = small.render("No", True, WHITE)

class ABOUT:
    """
    Holds the 'About' texts for the application.
    """
    HEAD = large.render("About PyChess", True, WHITE)
    with open(os.path.join("res", "texts", "about.txt"), "r") as f:
        TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]

class HOWTO:
    """
    Provides instructions and help texts for new users.
    """
    HEAD = large.render("Chess Howto", True, WHITE)
    with open(os.path.join("res", "texts", "howto.txt"), "r") as f:
        TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]

class TIMER:
    """
    Holds texts for the Timer Menu used in the game.
    """
    HEAD = large.render("Timer Menu", True, WHITE)
    
    YES = small.render("Yes", True, WHITE)
    NO = small.render("No", True, WHITE)
    
    PROMPT = vsmall.render("Do you want to set timer?", True, WHITE)
    with open(os.path.join("res", "texts", "timer.txt"), "r") as f:
        TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]

# Quit the font module after all fonts are loaded to free related resources.
pygame.font.quit()