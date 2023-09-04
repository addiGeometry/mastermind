"""
Der Breaker löst das Spiel Mastermind, je nachdem welcher Spielmodus gespielt wird dauert
es unterschiedlich lange einen nächsten Rate-Versuch zu berechnen
"""
import itertools
import copy
import time

from pubsub import pub
from mastermind import Colors


class BreakerBot:
    """
        Initialisiert die Klasse Breaker4.
        :param colors: Eine Liste der verfügbaren Farben.
        :param code_length: Die Länge des Codes.
    """

    def __init__(self, colors, code_length):
        pub.subscribe(self.reduce_codes, "add_rating")
        pub.subscribe(self.generate_next_guess, "request_guess")
        global P
        global S
        global prevGuesses
        global numPegs
        global numColours
        global firstGuess
        global recentGuess
        global guessCount
        P = []  # Set, das alle möglichen Kombinationen enthält
        S = []  # Set, das alle möglichen Antworten enthält
        prevGuesses = []
        numPegs = code_length
        self.col = colors
        numColours = len(colors)
        if code_length == 4:
            firstGuess = [self.col[1], self.col[1], self.col[2], self.col[2]]
        if code_length == 5:
            firstGuess = [self.col[1], self.col[1], self.col[2], self.col[2], self.col[3]]

        recentGuess = firstGuess
        guessCount = 1
        self._setup()

    def _setup(self):
        """
        Funktion zum Initialisieren der Arrays P und S mit allen möglichen Kombinationen.
        """
        global P
        global S
        global numColours
        r = []

        for i in self.col:
            r.append(i)

        comb = itertools.product(r, repeat=numPegs)

        for i in comb:
            P.append(list(i))

        S = copy.deepcopy(P)
        # print(S)

    def _count_black_pegs(self, code, guess):
        """
        Hilfsfunktion, um die Anzahl der schwarzen Stifte zu zählen.
        :param code: Der geheime Code.
        :param guess: Der geratene Code.
        :return: Die Anzahl der schwarzen Stifte.
        """
        black_pegs = 0

        for i in range(len(guess)):
            if guess[i] == code[i]:
                black_pegs += 1

        return black_pegs

    def _count_white_pegs(self, code, guess):
        """
        Hilfsfunktion, um die Anzahl der weißen Stifte zu zählen.
        :param code: Der geheime Code.
        :param guess: Der geratene Code.
        :return: Die Anzahl der weißen Stifte.
        """
        temp_code = code[:]  # Kopiere die Liste, um die ursprüngliche Liste nicht zu verändern
        white_pegs = 0

        for i in guess:
            if i in temp_code:
                temp_code.remove(i)
                white_pegs += 1

        return white_pegs

    def _count_pegs(self, code, guess):
        """
        Funktion, um die Anzahl der schwarzen und weißen Stifte für einen gegebenen Code
        und eine gegebene Vermutung zu zählen.
        :param code: Der geheime Code.
        :param guess: Der geratene Code.
        :return: Ein Tupel mit der Anzahl der schwarzen und weißen Stifte.
        """
        black_pegs = self._count_black_pegs(code, guess)
        white_pegs = self._count_white_pegs(code, guess)

        # Es werden die schwarzen und weißen Pins getrennt voneinander gezählt deshalb müssen
        # wir von den weißen die schwarzen abziehen
        white_pegs -= black_pegs

        return black_pegs, white_pegs

    def _remove_impossible(self, recent_black_pegs, recent_white_pegs):
        """
        Funktion, um unmögliche Codes aus S basierend auf neuen Informationen zu entfernen.
        :param recent_black_pegs: Die Anzahl der schwarzen Stifte des aktuellen Versuchs.
        :param recent_white_pegs: Die Anzahl der weißen Stifte des aktuellen Versuchs.
        """
        global S
        global recentGuess

        temp_s = copy.deepcopy(S)

        # Iteriere durch S und entferne Codes, die basierend auf den neuen Informationen keine möglichen Antworten sind
        for code in temp_s:
            black_count, white_count = self._count_pegs(code, recentGuess)

            if black_count != recent_black_pegs or white_count != recent_white_pegs:
                S.remove(code)

    def _find_max_hit_count(self, groups):
        """
        Funktion zum Finden und Zurückgeben der maximalen Trefferanzahl aller Gruppen.
        :param groups: Eine Liste von Gruppen von Codes.
        :return: Die maximale Trefferanzahl.
        """
        grp_hit_count = 0
        max_hit_count = 0

        for key, group in groups:
            grp_hit_count = len(list(group))
            if grp_hit_count > max_hit_count:
                max_hit_count = grp_hit_count

        return max_hit_count

    def reduce_codes(self, rating):
        """
        Funktion zur Reduzierung der möglichen Codes basierend auf der Bewertung des letzten Versuchs.
        :param rating: Die Bewertung des letzten Versuchs.
        """
        global recentGuess
        global prevGuesses

        recent_black_pegs = rating.count(Colors.BLACK)
        recent_white_pegs = rating.count(Colors.WHITE)
        self._remove_impossible(recent_black_pegs, recent_white_pegs)
        prevGuesses.append(firstGuess)

    def generate_next_guess(self):
        """
        Funktion zur Generierung der nächsten Vermutung.
        :return: Die nächste Vermutung.
        """
        global P
        global S
        global prevGuesses
        global firstGuess
        global recentGuess
        global guessCount
        groups = []
        best_min_eliminated = []
        best_guesses = []

        if guessCount == 1:
            print("")
            print("# of Possibilities: ", len(S))
            print("First Guess: ", firstGuess)
            guessCount += 1
            pub.sendMessage("add_guess", guess=firstGuess)
            return firstGuess

        for guess in P:  # P enthält alle möglichen Codes
            if (not guess in prevGuesses):
                # Alle Vermutungen in S sind sortiert und nach den resultierenden Stiftzähler-Werten gruppiert.
                # Schauen Sie sich Schritt 6 von Knuths Fünf-Vermutungs-Algorithmus an,
                # um die MinMax-Technik zu verstehen.
                data = sorted(S, key=lambda x: (self._count_pegs(guess, x)))
                groups = itertools.groupby(data, lambda x: (self._count_pegs(guess, x)))

                # Finde heraus, welche Gruppe uns die höchste Trefferanzahl liefert.
                # Dies ist die Gruppe, die die meisten Möglichkeiten eliminieren wird.
                max_hit_count = self._find_max_hit_count(groups)
                min_eliminated = len(S) - max_hit_count

                # Füge die Vermutung und den Wert (höchste minimale Anzahl eliminiert)
                # zu den Listen hinzu, um sie später zu vergleichen.
                best_min_eliminated.append(min_eliminated)
                best_guesses.append(guess)

        # Finde die maximale Anzahl von minimierten Vermutungen und alle entsprechenden Indizes.
        max_min_eliminated = max(best_min_eliminated)
        indices = [index for index, value in enumerate(best_min_eliminated) if value == max_min_eliminated]

        next_guess = []
        flag_first_guess = True

        # Durchlaufe die Indizes und schaue, ob wir eine in S finden können. Andernfalls verwenden wir den ersten.
        # Grund: Wenn wir mehrere mögliche beste Vermutungen haben, versuchen wir, eine aus S zu wählen
        # (sofern sie existiert). Dies gibt uns die Möglichkeit, den Code früher zu erraten.
        for i in indices:
            if best_guesses[i] in S:
                next_guess = best_guesses[i]
                break
            elif flag_first_guess:
                next_guess = best_guesses[i]
                flag_first_guess = False

        print("")
        print("# of Possibilities: ", len(S))

        if len(S) < 1:  # Wird nur durch falsche Bewertungen ausgelöst
            print("Error: No possible combination, based on given information")
            print("Please double check your responses for mistakes and try again")
            pub.sendMessage("possible-guesses-empty")
            return -1
            # exit()

        print("Next Guess: ", next_guess)

        guessCount += 1
        recentGuess = next_guess
        pub.sendMessage("add_guess", guess=next_guess)

        return next_guess
