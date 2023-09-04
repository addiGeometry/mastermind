# pylint: disable=all
from unittest.mock import patch, MagicMock
from . import GameController, GameBoard, GameMode, Role, MastermindRule, Colors
from pubsub import pub


class TestGameController:

    def test_init_game_controller_attr(self):
        controller = GameController(game_board=GameBoard)
        assert controller.role is None
        assert controller.rule_set is None
        assert controller.game_board is not None

    def test_game_controller_create_game(self):
        controller = GameController(game_board=GameBoard)
        with patch.object(controller, 'start_game') as mock_start_game:
            pub.sendMessage("create_game", game_mode=GameMode.MASTERMIND, role=Role.MAKER)
            mock_start_game.assert_called_once()

    def test_game_controller_start_game(self):
        controller = GameController(game_board=GameBoard)
        with patch("pubsub.pub.sendMessage") as mock_send_message:
            controller.create_game(GameMode.MASTERMIND, Role.MAKER)

            # Überprüfen, ob die 'sendMessage'-Methode mit dem erwarteten 'start_game'-Event aufgerufen wurde
            expected_event = "start_game"
            expected_kwargs = {
                "anzahl_zuege": controller.rule_set.amount_turns,
                "code_length": controller.rule_set.code_length,
                "anzahl_farben": len(controller.rule_set.colors)
            }
            mock_send_message.assert_called_once_with(expected_event, **expected_kwargs)

    def test_game_controller_set_get_code(self):
        controller = GameController(game_board=GameBoard)
        code = "1234"
        pub.sendMessage("code_set", code=code)

        assert controller.get_code() == code

    def test_game_controller_add_guess(self):
        controller = GameController(game_board=GameBoard)
        pub.sendMessage("create_game", game_mode=GameMode.MASTERMIND, role=Role.MAKER)
        guess = [Colors.WHITE, Colors.BLUE, Colors.GREEN, Colors.BLACK]

        with patch.object(controller.game_board, 'add_guessing_attempt') as mock_add_guessing_attempt:
            pub.sendMessage("add_guess", guess=guess)

        # Überprüfen, ob add_guessing_attempt aufgerufen wurde
        mock_add_guessing_attempt.assert_called_once_with(guess)

    def test_game_controller_add_rating(self):
        game_board_mock = MagicMock()

        game_controller = GameController(game_board_mock)

        rating = [Colors.BLACK, Colors.WHITE]
        pub.sendMessage("add_rating", rating=rating)

        game_board_mock.add_rating.assert_called_once_with(rating)


    def test_game_controller_give_up_clear_game(self):
        game_board_mock = MagicMock()

        game_controller = GameController(game_board_mock)

        pub.sendMessage("give_up", role="example_role")

        game_board_mock.clear_board.assert_called_once()

    def test_game_controller_get_code_length(self):
        game_board_mock = MagicMock()
        code = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW]
        game_board_mock.code = code

        game_controller = GameController(game_board_mock)

        result = game_controller.get_code_length()

        assert result == len(code)

    pass
