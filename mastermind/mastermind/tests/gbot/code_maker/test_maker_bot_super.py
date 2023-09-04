# pylint: disable=all
from unittest.mock import Mock

import pytest
from pubsub import pub

from . import MakerBot, Colors


class TestMakerBotSuperMastermind:
    @pytest.fixture
    def maker(self):
        colors = [Colors.RED, Colors.BLUE, Colors.YELLOW, Colors.GREEN, Colors.WHITE, Colors.BLACK]
        code_length = 5
        return MakerBot(colors, code_length)

    def test_create_validation_correct_guess(self, maker):
        maker.code = [Colors.RED, Colors.BLUE, Colors.YELLOW, Colors.GREEN, Colors.WHITE]
        guess = [Colors.RED, Colors.BLUE, Colors.YELLOW, Colors.GREEN, Colors.WHITE]
        expected_rating = [Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK]
        assert maker.create_validation(guess) == expected_rating

    def test_create_validation_correct_colors_wrong_positions(self, maker):
        maker.code = [Colors.RED, Colors.BLUE, Colors.YELLOW, Colors.GREEN, Colors.WHITE]
        guess = [Colors.GREEN, Colors.YELLOW, Colors.BLUE, Colors.WHITE, Colors.RED]
        expected_rating = [Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.WHITE]
        assert maker.create_validation(guess) == expected_rating

    def test_create_validation_incorrect_colors(self, maker):
        maker.code = [Colors.RED, Colors.BLUE, Colors.YELLOW, Colors.GREEN, Colors.WHITE]
        guess = [Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK]
        expected_rating = []
        assert maker.create_validation(guess) == expected_rating

    def test_create_validation_mixed_rating(self, maker):
        maker.code = [Colors.RED, Colors.BLUE, Colors.YELLOW, Colors.GREEN, Colors.WHITE]
        guess = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.BLUE, Colors.WHITE]
        expected_rating = [Colors.BLACK, Colors.BLACK, Colors.WHITE, Colors.WHITE, Colors.WHITE]
        assert maker.create_validation(guess) == expected_rating

    def test_create_validation_event(self, maker):
        mock_pub = Mock(spec=pub)
        pub.subscribe = mock_pub.subscribe
        pub.sendMessage = mock_pub.sendMessage

        maker.code = [Colors.WHITE, Colors.RED, Colors.BLUE, Colors.GREEN, Colors.BLACK]
        guess = [Colors.RED, Colors.RED, Colors.GREEN, Colors.BLUE, Colors.WHITE]
        rating = maker.create_validation(guess)

        assert rating == [Colors.BLACK, Colors.WHITE, Colors.WHITE, Colors.WHITE]
        mock_pub.sendMessage.assert_called_once_with("add_rating", rating=[Colors.BLACK, Colors.WHITE, Colors.WHITE, Colors.WHITE])

    def test_set_up_code_event(self, maker):
        mock_pub = Mock(spec=pub)
        pub.subscribe = mock_pub.subscribe
        pub.sendMessage = mock_pub.sendMessage

        maker.set_up_code()

        mock_pub.subscribe.assert_called_once_with(maker.create_validation, "request_validation")
        mock_pub.sendMessage.assert_called_once_with("code_set", code=maker.code)
