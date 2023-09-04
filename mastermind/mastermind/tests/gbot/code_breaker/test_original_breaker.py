# pylint: disable=all
from unittest.mock import Mock, call

import pytest
from pubsub import pub

from . import RuleFactory, GameMode, BreakerBot, Colors


class TestOriginalBreaker:

    @pytest.fixture
    def breaker_bot(self):
        fact = RuleFactory()
        master = fact.create_rules(GameMode.MASTERMIND)
        return BreakerBot(master.colors, master.code_length)

    def test_count_black_pegs(self, breaker_bot):
        code = [1, 2, 3, 4]
        guess = [1, 2, 3, 4]
        black_pegs = breaker_bot._count_black_pegs(code, guess)
        assert black_pegs == 4

    def test_count_white_pegs(self, breaker_bot):
        code = [1, 2, 3, 4]
        guess = [4, 3, 2, 1]
        white_pegs = breaker_bot._count_white_pegs(code, guess)
        assert white_pegs == 4

    def test_count_pegs(self, breaker_bot):
        code = [1, 2, 3, 4]
        guess = [1, 2, 3, 4]
        black_pegs, white_pegs = breaker_bot._count_pegs(code, guess)
        assert black_pegs == 4
        assert white_pegs == 0

    def test_find_max_hit_count(self, breaker_bot):
        groups = [(1, [1, 2, 3]), (2, [4, 5, 6]), (3, [7, 8, 9])]
        max_hit_count = breaker_bot._find_max_hit_count(groups)
        assert max_hit_count == 3

    def test_generate_next_guess(self, breaker_bot):
        next_guess = breaker_bot.generate_next_guess()
        assert isinstance(next_guess, list)
        assert len(next_guess) == 4

    def test_reduce_codes_event(self, breaker_bot):
        mock_pub = Mock(spec=pub)
        pub.subscribe = mock_pub.subscribe
        pub.sendMessage = mock_pub.sendMessage

        breaker_bot.generate_next_guess()
        mock_pub.sendMessage.assert_called_once_with("add_guess", guess=[Colors.BLUE, Colors.BLUE, Colors.GREEN, Colors.GREEN])

        rating = [Colors.BLACK, Colors.BLACK, Colors.WHITE]
        breaker_bot.reduce_codes(rating)
        breaker_bot.generate_next_guess()

        expected_calls = [
            call("add_guess", guess=[Colors.BLUE, Colors.BLUE, Colors.GREEN, Colors.GREEN]),
            call("add_guess", guess=[Colors.RED, Colors.BLUE, Colors.BLUE, Colors.GREEN])
        ]
        mock_pub.sendMessage.assert_has_calls(expected_calls)

    def test_generate_next_guess_event(self, breaker_bot):
        mock_pub = Mock(spec=pub)
        pub.subscribe = mock_pub.subscribe
        pub.sendMessage = mock_pub.sendMessage

        breaker_bot.generate_next_guess()

        mock_pub.sendMessage.assert_called_once_with("add_guess", guess=[Colors.BLUE, Colors.BLUE, Colors.GREEN, Colors.GREEN])
