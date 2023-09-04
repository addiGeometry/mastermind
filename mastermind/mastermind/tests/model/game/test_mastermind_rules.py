# pylint: disable=all

"""
Testsuite für das Testen der Regeln des Spiels Mastermind
"""

from . import GameMode, RuleFactory, Rule, SuperMastermindRule, MastermindRule


class TestMastermindRules:
    """
    Testklasse für die Regeln des Spiels Mastermind
    """

    def test_mm_ruleset_object_is_instance_of_rules(self):
        mm_ruleset = RuleFactory.create_rules(GameMode.MASTERMIND)

        assert isinstance(mm_ruleset, Rule)
        assert isinstance(mm_ruleset, MastermindRule)

    def test_mm_ruleset_is_instance_of_mastermind_rules(self):
        mm_ruleset = RuleFactory.create_rules(GameMode.SUPER_MASTERMIND)

        assert isinstance(mm_ruleset, Rule)
        assert isinstance(mm_ruleset, SuperMastermindRule)

    def test_mastermind_rules_is_valid_to_requirements(self):
        codelength = 4
        color_amount = 6
        mm_ruleset = RuleFactory.create_rules(GameMode.MASTERMIND)

        assert mm_ruleset.code_length == codelength
        assert len(mm_ruleset.colors) == color_amount

    def test_super_mastermind_rules_is_valid_to_requirements(self):
        codelength = 5
        color_amount = 8
        mm_ruleset = RuleFactory.create_rules(GameMode.SUPER_MASTERMIND)

        assert mm_ruleset.code_length == codelength
        assert len(mm_ruleset.colors) == color_amount
