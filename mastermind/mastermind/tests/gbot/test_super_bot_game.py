# pylint: disable=all
import pytest
from pubsub import pub

from . import Colors, MakerBot, RuleFactory, GameMode, BreakerBot


class TestBotEvaluation:
    """ACHTUNG alle Tests dieser Klasse brauchen deutlich länger zum Durchlaufen, wirklich ALLE!!!"""
    @pytest.fixture
    def breaker(self):
        fact = RuleFactory()
        breaker = fact.create_rules(GameMode.SUPER_MASTERMIND)
        return BreakerBot(breaker.colors, breaker.code_length)

    @pytest.fixture
    def maker(self):
        fact = RuleFactory()
        master = fact.create_rules(GameMode.SUPER_MASTERMIND)
        return MakerBot(master.colors, master.code_length)

    '''def test_super_bot_game(self, maker, breaker):
        for i in range(10):
            print(i)
            gue = breaker.generate_next_guess()
            if gue == -1:
                print("Real Code ist: ", maker.code)
                break
            else:
                vali = maker.create_validation(gue)
                if vali.count(Colors.BLACK) == 5:
                    print("Gewonnen in ", i, " Zügen")
                    break
                breaker.reduce_codes(vali)
        assert gue == maker.code
        assert i <= 10

    def test_super_bot_game_max_7_turns(self, maker, breaker):
        for i in range(7):
            gue = breaker.generate_next_guess()
            if gue == -1:
                print("Real Code ist: ", maker.code)
                break
            else:
                vali = maker.create_validation(gue)
                if vali.count(Colors.BLACK) == 5:
                    print("Gewonnen in ", i, " Zügen")
                    break
                breaker.reduce_codes(vali)
        assert gue == maker.code
        assert i <= 7

    def test_super_game_multi_times(self, maker, breaker):
        for _ in range(10):
            self.test_super_bot_game(maker, breaker)
            self.test_super_bot_game_max_7_turns(maker, breaker)'''
    pass
