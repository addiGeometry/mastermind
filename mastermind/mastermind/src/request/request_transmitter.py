"""
Diese Klasse ist die (delegations)Schnittstelle welche entscheidet an welche Klasse die
Requests weitergeleitet werden als Requests zählen z.B. requestValidation oder requestRating
im Online-Modus wird dann eine Anfrage an den NetworkManager gestellt
im Offline Modus wird eine Anfrage an den Bot gestellt
die Antworten der jeweiligen Instanz werden dann wieder über Events vermittelt, z.B. addRating,
welches beim GameController ankommen wird

Somit hört diese Klasse auf fast alle Events 
"""
from pubsub import pub
from . import Colors, Role, MakerBot, BreakerBot
from ..model.game.mastermind_rules import GameMode
from mastermind.src.utils.checker import Checker


class RequestTransmitter:
    """Diese Klasse reagiert auf fast jedes Event und schickt, falls nötig über das Netzwerk
    eine JSON Anfrage an einen anderen Spieler"""

    def __init__(self, online_modus, network_controller, game_controller):
        self.online = online_modus
        self.network_controller = network_controller
        self.game_controller = game_controller

        self.player_name = "NONE"
        self.role = "NONE"
        self.game_id = -1
        self.positions = -1
        self.colors = -1

        self.bot = None

        self.subscribe()

    def set_network_info(self, ip, port):
        """Setzt die Netzwerk Konfigurationen wie IP-Addresse und Port"""
        # IP & Port werden im Front-End defensiv abgefragt
        self.network_controller.set_ip(ip)
        self.network_controller.set_port(port)

    def set_role(self, role):
        """Rolle setzen (Jeder hat für seine Instanz seine Rolle festgelegt)"""
        self.set_up_rule_data()
        self.role = role
        self.init_bot()

    def set_online_mode(self, online_mode):
        """Onlinemodus setzen"""
        self.online = online_mode

    def init_bot(self):
        """Anhand der gegebenen Informationen die richtige Botklasse erstellen"""
        if self.online:
            self.bot = None
        else:
            # Achtung umgekehrt da man Maker wählt und dann Breakerbot will
            if self.role == Role.MAKER:
                self.bot = BreakerBot(self.game_controller.rule_set.colors, self.positions)
            elif self.role == Role.BREAKER:
                self.bot = MakerBot(self.game_controller.rule_set.colors, self.positions)

    def request_validation(self, guess):
        """Sendet eine Anfrage an den Server, mit dem einem Rate versuch
        die Antwort ist die Bewertung"""

        request = self.create_request(self.game_id,
                                      self.player_name,
                                      self.positions,
                                      self.colors,
                                      guess)

        answer = self.network_controller.transmit(request).json()
        value = answer['value']
        rating = self.int_str_to_color_list(value)
        pub.sendMessage("add_rating", rating=rating)
        pub.sendMessage("request_guess", code_length=len(guess))  # Todo checken ob Parameter benötigt wird

    def handshake(self, ):

        """Wird verwendet, um eine neue Game-ID von der Online API anzufordern"""
        if self.online:
            # Handshake mit dem Ziel gameid zu setzen
            request = self.create_request(0,
                                          self.player_name,
                                          self.positions,
                                          self.colors,
                                          "")
            answer = self.network_controller.transmit(request).json()
            self.game_id = answer['gameid']
            return answer

    def set_player_name(self, username):
        """Setzt Spielernamen"""
        self.player_name = username

    def set_up_rule_data(self):
        """Codelänge und mögliche Farben werden gesetzt"""

        self.positions = self.game_controller.rule_set.code_length
        self.colors = len(self.game_controller.rule_set.colors)

    def create_request(self, game_id, gamer_id, positions, colors, value):
        """Erstellt ein Request-Objekt"""
        value = self.list_to_int(value)
        req = {
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            '$id': 'https://htwberlin.com/ssr/superhirnserver/move_schema.json',
            'title': 'Move',
            'gameid': game_id,
            'gamerid': gamer_id,
            'positions': positions,
            'colors': colors,
            'value': value
        }
        return req

    def list_to_int(self, list_values):
        """Verändert eine Liste aus Farben zu einem String aus Int Werten"""
        int_values = [int(color) for color in list_values]
        str_values = [str(value) for value in int_values]
        res = ''.join(str_values)
        return res

    def int_str_to_color_list(self, intstr):
        """Verändert einen String aus Int Werten zu einer Liste aus Farben"""
        int_values = [int(char) for char in intstr]
        enum_values = [Colors(value) for value in int_values]
        return enum_values

    def clear_data(self):
        """Setzt alle Werte zurück"""
        self.game_controller.clear_game()
        self.player_name = "NONE"
        self.role = "NONE"
        self.game_id = -1
        self.positions = -1
        self.colors = -1
        self.unsubscribe_all()

    def start_game(self, anzahl_zuege: int, code_length: int, anzahl_farben: int):
        """Wenn das start_game Event ankommt wird die subscribe_by_onlinemode() aufgerufen"""
        self.subscribe_by_onlinemode()

    def subscribe(self):
        # Click-Events
        pub.subscribe(self.set_online_mode, "clicked_online_play")
        pub.subscribe(self.set_role, "clicked_role")  # Rolle
        pub.subscribe(self.set_online_mode, "clicked_online")

        pub.subscribe(self.handshake, "handshake")

        # Set-Up Events
        pub.subscribe(self.start_game, "start_game")
        pub.subscribe(self.set_player_name, "username_set")
        pub.subscribe(self.set_network_info, "transmit_network_data")

        # While In-Game
        # pub.subscribe(self.init_bot, "possible-guesses-empty")

        # Tear-Down Events
        pub.subscribe(self.clear_data, "clear_data")
    def subscribe_by_onlinemode(self):
        """Anmelden für das Event request_validation"""
        if self.online:
            pub.subscribe(self.request_validation, "request_validation")

    def unsubscribe_all(self):
        """Abmelden von dem Event request_validation"""
        try:
            pub.unsubscribe(self.request_validation, "request_validation")
        except Exception:
            pass

    def init_game(self, player_name, game_mode, role, online_mode, ip, port):
        """Initialisiert das Spiel in dieser Klasse für die Netzwerk Kommunikation"""
        if online_mode:
            self.set_online_mode(True)
            self.set_network_info(ip, port)

        self.game_controller.create_game(game_mode, role)
        self.player_name = player_name
        self.set_role(role)
