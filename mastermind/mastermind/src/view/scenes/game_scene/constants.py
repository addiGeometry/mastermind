"""
Konstante für das View
"""
from . import WINDOW_WIDTH, WINDOW_HEIGHT
from typing import Callable


__all__ = [
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "ORANGE",
    "BROWN",
    "BLACK",
    "WHITE",
    "COLORS",
    "TILESIZE"
]

# Game Colors:
RED = (253,34,28)
GREEN = (1,198,90)
YELLOW = (248,238,79)
BLUE = (3,160,229)
ORANGE = (245,160,6)
BROWN = (181,138,81)
BLACK = (0,0,0)
WHITE = (255,255,255)


COLORS = [WHITE, BLACK, RED, GREEN, YELLOW, BLUE, ORANGE, BROWN]


TILESIZE = 70
