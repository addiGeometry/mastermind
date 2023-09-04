# pylint: disable=all
from unittest.mock import patch, call

import pytest
from pubsub import pub

from . import Colors, MakerBot, RuleFactory, GameMode, BreakerBot


class TestBotEvaluation:
    @pytest.fixture
    def breaker(self):
        fact = RuleFactory()
        breaker = fact.create_rules(GameMode.MASTERMIND)
        return BreakerBot(breaker.colors, breaker.code_length)

    @pytest.fixture
    def maker(self):
        fact = RuleFactory()
        master = fact.create_rules(GameMode.MASTERMIND)
        return MakerBot(master.colors, master.code_length)

    def test_original_bot_game(self, maker, breaker):
        for i in range(10):
            gue = breaker.generate_next_guess()
            if gue == -1:
                print("Real Code ist: ", maker.code)
                break
            else:
                vali = maker.create_validation(gue)
                if vali.count(Colors.BLACK) == 4:
                    print("Gewonnen in ", i, " Zügen")
                    break
                breaker.reduce_codes(vali)
        assert gue == maker.code
        assert i <= 10

    def test_original_bot_game_fixed_code(self, maker, breaker):
        maker.code = [Colors.GREEN, Colors.GREEN, Colors.GREEN, Colors.GREEN]
        for i in range(10):
            gue = breaker.generate_next_guess()
            if gue == -1:
                print("Real Code ist: ", maker.code)
                break
            else:
                vali = maker.create_validation(gue)
                if vali.count(Colors.BLACK) == 4:
                    print("Gewonnen in ", i, " Zügen")
                    break
                breaker.reduce_codes(vali)
        assert gue == maker.code
        assert i <= 10
    def test_original_bot_game_max_6_turns(self, maker, breaker):
        for i in range(6):
            gue = breaker.generate_next_guess()
            if gue == -1:
                print("Real Code ist: ", maker.code)
                break
            else:
                vali = maker.create_validation(gue)
                if vali.count(Colors.BLACK) == 4:
                    print("Gewonnen in ", i, " Zügen")
                    break
                breaker.reduce_codes(vali)
        assert gue == maker.code
        assert i <= 6

    def test_original_game_multi_times(self, maker, breaker):
        for _ in range(10):
            self.test_original_bot_game(maker, breaker)
            self.test_original_bot_game_max_6_turns(maker, breaker)

    def test_original_game_wrong_rating(self, maker, breaker):
        with patch('pubsub.pub.sendMessage') as mock_send_message:
            for i in range(10):
                gue = breaker.generate_next_guess()
                if gue == -1:
                    print("Real Code ist: ", maker.code)
                    break
                else:

                    vali = maker.create_validation(gue)
                    black = vali.count(Colors.BLACK)
                    white = vali.count(Colors.WHITE)

                    if black != 4 and white != 4 and white+black != 4:
                        vali.append(Colors.WHITE)

                    if vali.count(Colors.BLACK) == 4:
                        print("Gewonnen in ", i, " Zügen")
                        break
                    breaker.reduce_codes(vali)

            mock_send_message.assert_called_with('possible-guesses-empty')
