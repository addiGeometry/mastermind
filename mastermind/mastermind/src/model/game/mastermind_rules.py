"""
Modul für die verschiedenen Mastermind-Spielmodi.
Enthält eine Enum und die entsprechenden Regeln.
Regeln ermöglichen dem Controller und dem View, bzw. anderen Spielteilnehmern, nach
den Regeln des Spielmodus zu Spielen.
"""
from typing import List
from enum import Enum
from abc import ABC, abstractmethod
from ..colors import Colors

__all__ = ["GameMode", "Rule", "MastermindRule", "SuperMastermindRule", "RuleFactory"]


class GameMode(Enum):
    """
    Enum für die Möglichen Spielmodi des Spiels Mastermind
    """
    MASTERMIND = 1
    SUPER_MASTERMIND = 2


class Rule(ABC):
    """
    Abstrakte Klasse für Spielregeln
    """

    __slots__ = ["_colors", "_code_length", "_amount_turns"]

    @abstractmethod
    def __init__(self):
        """
        Erzeugung eines Rule-Objects
        """
        self._colors = []
        self._code_length = -1
        self._amount_turns = -1

    @property
    def colors(self) -> List[Colors]:
        """
        return: List[Colors] - die Farben in dem Spielmodus
        """
        return self._colors

    @colors.setter
    def colors(self, value: List[Colors]) -> None:
        self._colors = value

    @property
    def code_length(self) -> int:
        """
        return: int - die Kode länge für den Spielmodus
        """
        return self._code_length

    @code_length.setter
    def code_length(self, value: int) -> None:
        self._code_length = value

    @property
    def amount_turns(self) -> int:
        """
        return: int - die Kode länge für den Spielmodus
        """
        return self._amount_turns

    @amount_turns.setter
    def amount_turns(self, value: int) -> None:
        self._amount_turns = value


class MastermindRule(Rule):
    """
    Regeln für den Spielmodus Mastermind Orignal
    """

    def __init__(self):
        self.amount_turns = 10
        self.code_length = 4
        self.colors = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.WHITE,
                       Colors.YELLOW, Colors.BLACK]


class SuperMastermindRule(Rule):
    """
    Regeln für den Spielmodus Super Mastermind
    """
    def __init__(self):
        self.amount_turns = 10
        self.code_length = 5
        self.colors = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.WHITE,
                       Colors.YELLOW, Colors.BLACK, Colors.ORANGE, Colors.BROWN]


class RuleFactory(ABC):
    """
    Factory zum Erzeugen von Spielregeln
    """

    @staticmethod
    def create_rules(mode: GameMode) -> Rule:
        """
        Methode der Factory zum Erzeugen der entsprechenden Spielregeln
        """
        if mode == GameMode.MASTERMIND:
            rule_set = MastermindRule()
            return rule_set
        elif mode == GameMode.SUPER_MASTERMIND:
            rule_set = SuperMastermindRule()
            return rule_set
        else:
            raise TypeError("Wrong input for Method: create_rules")
