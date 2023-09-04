"""
Mastermind ist ein tolles Spiel, bei dem der Rater(Breaker) versucht
einen Kode, erstellt vom Kodierer(Maker) zu erraten.
"""
from mastermind.src.model.player import Role, Player
from mastermind.src.model.colors.colors import Colors
from mastermind.src.model.game.mastermind_rules import *
from mastermind.src.model.game import GameBoard
from mastermind.src.gamelogic.game_controller import GameController
from mastermind.src.view.controller.gui_control import GuiController
from mastermind.src.request.request_transmitter import RequestTransmitter
from mastermind.src.net.network_controller import NetworkController
