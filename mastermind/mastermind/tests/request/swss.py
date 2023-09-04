from . import GameBoard, GameController, NetworkController, RequestTransmitter, Role, Colors, GameMode
IP = "localhost"
PORT = 3001

class TestRequestTransmitter:
    IP = "localhost"
    PORT = 3000

    def test_with_real_server_mastermind_only_handshake(self):
        # Set-Up
        ip = IP
        port = PORT

        game_board = GameBoard()
        game_controller = GameController(game_board)
        network_controller = NetworkController()
        network_controller.ip = IP
        network_controller.port = PORT
        request_transmitter = RequestTransmitter(True, network_controller, game_controller)
        request_transmitter.game_id = 0
        request_transmitter.positions = 4
        request_transmitter.colors = 6

        # Enable Network Log
        network_controller.msg = True

        print("Test-Cases: Mastermind:")
        game_controller.create_game(GameMode.MASTERMIND, Role.BREAKER)
        request_transmitter.handshake()

        # Tear-Down
        game_controller.clear_game()

    def test_with_real_server_mastermind(self):
        # Set-Up
        ip = IP
        port = PORT

        game_board = GameBoard()
        game_controller = GameController(game_board)
        network_controller = NetworkController()
        network_controller.ip = IP
        network_controller.port = PORT
        request_transmitter = RequestTransmitter(True, network_controller, game_controller)
        request_transmitter.game_id = 0
        request_transmitter.positions = 4
        request_transmitter.colors = 6

        # Enable Network Log
        network_controller.msg = True

        print("Test-Cases: Mastermind:")
        game_controller.create_game(GameMode.MASTERMIND, Role.BREAKER)
        request_transmitter.handshake()
        request_transmitter.request_validation([Colors.BLUE, Colors.RED, Colors.BROWN, Colors.YELLOW])

        # Tear-Down
        game_controller.clear_game()