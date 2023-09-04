import pygame as pg
from mastermind import GameController
from mastermind import GuiController
from mastermind import RequestTransmitter
from mastermind import NetworkController
from mastermind import GameBoard
from mastermind import Colors
from mastermind import GameMode
from mastermind import Role
import json
import requests

if __name__ == "__main__":
    gui = True

    if gui:
        pg.init()
        game = GuiController()

  #   Initialize
    game_board = GameBoard()
    game_controller = GameController(game_board)
    network_controller = NetworkController()
    request_transmitter = RequestTransmitter(True, network_controller, game_controller)
#
    #Test
    network_controller.network_log = True

    #Run
    game.run()
