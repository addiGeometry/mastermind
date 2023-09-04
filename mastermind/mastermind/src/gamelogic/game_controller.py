"""
Diese Klasse dient als Control-Objekt des Game_Board(Modell)
Es reagiert nur auf Events die das Modell verändern!
"""

from pubsub import pub
from . import GameMode, GameBoard, Role, RuleFactory, Colors, Rule


class GameController:
    """
    GameController für die veränderung des Modells zuständig
    und hört auf die dafür benötigten Events
    """
    def __init__(self, game_board):
        self.game_board = game_board
        self.role = None
        self.rule_set = None

        # Menu Listener
        pub.subscribe(self.create_game, "create_game")

        # Game-Action Listener
        pub.subscribe(self.add_guess, "add_guess")
        pub.subscribe(self.add_rating, "add_rating")
        pub.subscribe(self.give_up, "give_up")
        pub.subscribe(self.set_code, "code_set")

        pub.subscribe(self.request_code, "request_code")

    def create_game(self, game_mode: GameMode, role: Role):
        """
        Create a game instance. This method will be triggered by the event 'create_game'
        """
        self.rule_set = RuleFactory.create_rules(game_mode)
        self.role = role
        self.start_game()

    def get_code_length(self):
        return len(self.game_board.code)

    def start_game(self):
        """
        Startet das Spiel
        :return: None
        """
        pub.sendMessage("start_game",
                        anzahl_zuege=self.rule_set.amount_turns,
                        code_length=self.rule_set.code_length,
                        anzahl_farben=len(self.rule_set.colors))

    def get_code(self):
        """
        Gibt den richtigen Code zurück
        :return: String
        """
        return self.game_board.code

    def add_guess(self, guess):
        """
        Fügt einen neuen Rateversuch zum game_board hinzu
        :param guess:
        :return: None
        """
        if self.rule_set.code_length == len(guess):
            self.game_board.add_guessing_attempt(guess)

    def add_rating(self, rating):
        """
        Fügt eine Bewertung für den letzten Rateversuch zum game_board hinzu
        :param rating:
        :return: None
        """
        if rating ==[Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK]:
            pub.sendMessage("game_won")
        self.game_board.add_rating(rating)

    def give_up(self, role):
        """Beendet das spiel, falls eine bestimmte Rolle das Spiel aufgibt"""
        self.clear_game()

    def clear_game(self):
        """Löscht alle Daten für ein nächstes Spiel"""
        self.game_board.clear_board()
        self.role = None
        self.rule_set = None

    def set_code(self, code):
        """Setzt den Code"""
        print(f"code:{code}")
        self.game_board.code = code

    def request_code(self):
        pub.sendMessage("send_code", code=self.game_board.code)