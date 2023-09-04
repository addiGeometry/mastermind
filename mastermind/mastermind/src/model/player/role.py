"""
Die zwei Rollen die ein Mastermind spieler haben kann
"""

from enum import Enum


class Role(Enum):
    """
    Rolle (des Spielers)
    """
    MAKER = 0
    BREAKER = 1
