# pylint: disable=all
import unittest
from unittest.mock import Mock, call, patch
from mastermind import NetworkController, GameController, RequestTransmitter, Colors, Role
from mastermind.src.model.game.mastermind_rules import MastermindRule
from mastermind.src.bot.code_breaker.breaker_bot import BreakerBot
from mastermind.src.bot.code_maker.maker_bot import MakerBot
from pubsub import pub


class TestRequestTransmitter(unittest.TestCase):

    def setUp(self):
        self.network_manager = Mock(spec=NetworkController)
        self.game_controller = Mock(spec=GameController)

        self.game_controller.rule_set = Mock()
        self.game_controller.rule_set.colors = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.WHITE,
                                                Colors.YELLOW, Colors.BLACK]
        self.game_controller.get_code_length = Mock(return_value=4)

        self.request_transmitter = RequestTransmitter(online_modus=True, network_controller=self.network_manager,
                                                      game_controller=self.game_controller)

    def tearDown(self):
        self.network_manager = None
        self.game_controller = None
        self.request_transmitter = None

    def test_set_network_info(self):
        self.request_transmitter.set_network_info("127.0.0.1", 80)

        self.network_manager.set_ip.assert_called_with("127.0.0.1")
        self.network_manager.set_port.assert_called_with(80)

    def test_set_role(self):
        self.request_transmitter.init_bot = Mock()
        self.request_transmitter.set_up_rule_data = Mock()

        test_role = Role.MAKER
        self.request_transmitter.set_role(test_role)

        self.assertEqual(self.request_transmitter.role, test_role)

        self.request_transmitter.init_bot.assert_called_once()
        self.request_transmitter.set_up_rule_data.assert_called_once()

    def test_set_online_mode_true(self):
        self.request_transmitter.set_online_mode(True)
        self.assertTrue(self.request_transmitter.online)

    def test_set_online_mode_false(self):
        self.request_transmitter.set_online_mode(False)
        self.assertFalse(self.request_transmitter.online)

    def test_init_bot_online(self):
        self.request_transmitter.positions = 4

        self.request_transmitter.online = True
        self.request_transmitter.init_bot()
        self.assertIsNone(self.request_transmitter.bot)

    def test_init_bot_offline_maker(self):
        self.request_transmitter.positions = 4
        self.request_transmitter.online = False
        self.request_transmitter.role = Role.MAKER
        self.request_transmitter.init_bot()
        self.assertIsInstance(self.request_transmitter.bot, BreakerBot)

    @patch('pubsub.pub.sendMessage')
    def test_request_validation(self, mock_pub_send):
        self.request_transmitter.create_request = Mock(return_value='mock_request')
        self.request_transmitter.int_str_to_color_list = Mock(return_value='mock_rating')
        self.network_manager.transmit = Mock(return_value=Mock(json=Mock(return_value={'value': 'mock_value'})))

        self.request_transmitter.request_validation('mock_guess')

        self.request_transmitter.create_request.assert_called_once_with(self.request_transmitter.game_id,
                                                                        self.request_transmitter.player_name,
                                                                        self.request_transmitter.positions,
                                                                        self.request_transmitter.colors,
                                                                        'mock_guess')
        self.network_manager.transmit.assert_called_once_with('mock_request')
        self.request_transmitter.int_str_to_color_list.assert_called_once_with('mock_value')
        mock_pub_send.assert_any_call("add_rating", rating='mock_rating')
        mock_pub_send.assert_any_call("request_guess", code_length=len('mock_guess'))

    def test_handshake(self):
        self.request_transmitter.create_request = Mock(return_value='mock_request')
        self.network_manager.transmit = Mock(return_value=Mock(json=Mock(return_value={'gameid': 'mock_gameid'})))

        result = self.request_transmitter.handshake()

        self.request_transmitter.create_request.assert_called_once_with(0,
                                                                        self.request_transmitter.player_name,
                                                                        self.request_transmitter.positions,
                                                                        self.request_transmitter.colors,
                                                                        "")
        self.network_manager.transmit.assert_called_once_with('mock_request')
        self.assertEqual(self.request_transmitter.game_id, 'mock_gameid')
        self.assertEqual(result, {'gameid': 'mock_gameid'})

    def test_set_player_name(self):
        test_name = "TestPlayer"
        self.request_transmitter.set_player_name(test_name)
        self.assertEqual(self.request_transmitter.player_name, test_name)

    def test_set_up_rule_data(self):
        self.rule_set = Mock(spec=MastermindRule)
        self.game_controller.rule_set = self.rule_set

        self.rule_set.code_length = 4
        self.rule_set.colors = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.WHITE,
                                Colors.YELLOW, Colors.BLACK]

        self.request_transmitter.set_up_rule_data()

        self.assertEqual(self.request_transmitter.positions, 4)
        self.assertEqual(len(self.rule_set.colors), 6)

    def test_create_request(self):
        game_id = 1
        gamer_id = "TestPlayer"
        positions = 4
        colors = 6
        value = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.WHITE]

        expected_request = {
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            '$id': 'https://htwberlin.com/ssr/superhirnserver/move_schema.json',
            'title': 'Move',
            'gameid': game_id,
            'gamerid': gamer_id,
            'positions': positions,
            'colors': colors,
            'value': self.request_transmitter.list_to_int(value)  # Assuming list_to_int works correctly
        }

        actual_request = self.request_transmitter.create_request(game_id, gamer_id, positions, colors, value)
        self.assertEqual(actual_request, expected_request)

    def test_list_to_int(self):
        color_list = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.WHITE]
        expected_result = "1327"  # Based on Colors.RED=1, Colors.BLUE=3, Colors.GREEN=2, Colors.WHITE=7
        actual_result = self.request_transmitter.list_to_int(color_list)
        self.assertEqual(actual_result, expected_result)

    def test_int_str_to_color_list(self):
        int_str = "1377"
        expected_result = [Colors.RED, Colors.BLUE, Colors.WHITE, Colors.WHITE]  # Corrected expected result
        actual_result = self.request_transmitter.int_str_to_color_list(int_str)
        self.assertEqual(actual_result, expected_result)

    def test_clear_data(self):
        pub.subscribe(lambda: None, "request_validation")
        self.request_transmitter.clear_data()
        self.assertEqual(self.request_transmitter.player_name, "NONE")
        self.assertEqual(self.request_transmitter.role, "NONE")
        self.assertEqual(self.request_transmitter.game_id, -1)
        self.assertEqual(self.request_transmitter.positions, -1)
        self.assertEqual(self.request_transmitter.colors, -1)
        self.assertIsNone(self.request_transmitter.bot)

    def test_start_game(self):
        with patch.object(self.request_transmitter, 'subscribe_by_onlinemode') as mock_method:
            self.request_transmitter.start_game(10, 4, 6)
            mock_method.assert_called_once()

    def test_subscribe_by_onlinemode(self):
        with patch('pubsub.pub.subscribe') as mock_subscribe:
            self.request_transmitter.online = True
            self.request_transmitter.subscribe_by_onlinemode()
            mock_subscribe.assert_called_once_with(self.request_transmitter.request_validation, "request_validation")

    def test_unsubscribe_all(self):
        with patch('pubsub.pub.unsubscribe') as mock_unsubscribe:
            self.request_transmitter.unsubscribe_all()
            mock_unsubscribe.assert_called_once_with(self.request_transmitter.request_validation, "request_validation")

    def test_init_game(self):
        with patch.object(self.request_transmitter, 'set_online_mode') as mock_set_online_mode, \
                patch.object(self.request_transmitter, 'set_network_info') as mock_set_network_info, \
                patch.object(self.request_transmitter, 'set_role') as mock_set_role:
            player_name = "TestPlayer"
            game_mode = "TestMode"
            role = Role.MAKER
            online_mode = True
            ip = "127.0.0.1"
            port = 80
            self.request_transmitter.init_game(player_name, game_mode, role, online_mode, ip, port)
            mock_set_online_mode.assert_called_once_with(online_mode)
            mock_set_network_info.assert_called_once_with(ip, port)
            mock_set_role.assert_called_once_with(role)
            self.assertEqual(self.request_transmitter.player_name, player_name)
