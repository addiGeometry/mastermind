"""Diese Klasse enthält den Bot der für das Spiel Mastermind und seine Varianten den letzten
Rateversuch bewertet und beim Initialisieren einen zufälligen Code generiert"""
import random
from pubsub import pub
from mastermind import Colors


class MakerBot:
    """Generiert einen zufälligen Code und bewertet Rateversuche
    AUCH BESSER ALS CHATGPT"""

    def __init__(self, colors, code_length):
        self.code = []
        self.colors = colors
        self.code_length = code_length
        self.set_up_code()

    def set_up_code(self):
        """Erstellt einen zufälligen Code"""
        for _ in range(0, self.code_length):
            codepart = random.choice(self.colors)
            self.code.append(codepart)
        pub.sendMessage("code_set", code=self.code)
        pub.subscribe(self.create_validation, "request_validation")

    def create_validation(self, guess):
        """
        Bewertet den item code und gibt für jeden richtigen Stein an der
        richtigen Position Colors.BLACK zurück und für richtige Farbe,
        aber an der falschen Stelle des Codes Colors.WHITE
        :param guess: ist ein Array mit 4 bzw. 5 Einträgen
        :return: Die Bewertung als Array gefüllt mit Colors.BLACK und Colors.WHITE
        """
        rating = []
        tmp_result = self.code.copy()
        tmp_guess = guess.copy()

        # Setzt die Schwarzen Farben für Farbe an richtiger Stelle
        for i in range(len(guess)):
            if tmp_guess[i] == tmp_result[i]:
                tmp_guess[i] = None
                tmp_result[i] = None
                rating.append(Colors.BLACK)

        # Setzt die Weißen Farben für Farbe an falscher Stelle
        for i in range(len(tmp_guess)):
            if tmp_guess[i] is not None and tmp_guess[i] in tmp_result:
                tmp_result[tmp_result.index(tmp_guess[i])] = None
                tmp_guess[i] = None
                rating.append(Colors.WHITE)

        print(f"rating: {rating}")
        pub.sendMessage("add_rating", rating=rating)
        return rating
