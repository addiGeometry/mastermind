"""
Die Klasse Gameboard ist das Modell des Spiels.
Sie besitzt die Rate versuche, deren Bewertungen und auch den zu erratenden Code.
"""

class GameBoard:
    """
    GameBoard für das Spiel Mastermind und auch seine Erweiterungen, dieses stellt alle benötigten
    Methoden die beim GameBoard benötigt werden zur Verfügung
    """
    __slots__ = ["guessing_attempts", "rule", "ratings", "code",
                     "code_length"]

    def __init__(self):
        self.guessing_attempts = []
        self.ratings = []
        self.code = ""
        self.code_length = 0

    def add_guessing_attempt(self, guess):
        """Rate versuch hinzufügen"""
        self.guessing_attempts.append(guess)

    def add_rating(self, rating):
        """Rate versuch-Bewertung hinzufügen"""
        self.ratings.append(rating)

    def set_code(self, code):
        """Code setzten"""
        self.code = code

    def set_code_length(self, length):
        """Codelänge setzten"""
        self.code_length = length

    def clear_board(self):
        """Daten löschen"""
        self.code = ""
        self.ratings.clear()
        self.guessing_attempts.clear()
