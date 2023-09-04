# pylint: disable=all
import pytest
from unittest.mock import patch, MagicMock
import json

import requests

from ...src.net.network_controller import NetworkController


class TestNetworkController:

    def test_set_ip(self):
        network_controller = NetworkController()

        # Gültige IP-Adresse
        ip = '192.168.0.1'
        network_controller.set_ip(ip)
        assert network_controller.ip == ip

        # Ungültige IP-Adresse
        invalid_ip = 'not_an_ip_address'
        network_controller.set_ip(invalid_ip)
        assert network_controller.ip == ''

    def test_set_port(self):
        network_controller = NetworkController()

        # Gültiger Port
        port = 8080
        network_controller.set_port(port)
        assert network_controller.port == port

        # Ungültiger Port
        invalid_port = 'not_a_port'
        network_controller.set_port(invalid_port)
        assert network_controller.port == -1

        # Ungültiger Port
        invalid_port = 66000
        network_controller.set_port(invalid_port)
        assert network_controller.port == -1

    def test_transmit(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'success'}

        with patch.object(requests, 'post', return_value=mock_response) as mock_post:
            # Erstellen des NetworkController-Objekts
            network_controller = NetworkController()
            network_controller.set_ip('192.168.0.1')
            network_controller.set_port(8080)

            # Testnachricht
            request = {'command': 'example'}

            # Aufrufen der transmit-Methode
            response = network_controller.transmit(request)

            # Überprüfen, ob die Anfrage an die richtige URL gesendet wurde
            mock_post.assert_called_with('http://192.168.0.1:8080/',
                                         data=json.dumps(request),
                                         headers={'Content-Type': 'application/json'})

            # Überprüfen, ob die Antwort korrekt zurückgegeben wurde
            assert response.json() == {'status': 'success'}

    def test_is_valid_ip(self):
        # Gültige IP-Adresse
        valid_ip = '192.168.0.1'
        assert NetworkController.is_valid_ip(valid_ip)

        # Ungültige IP-Adresse
        invalid_ip = 'not_an_ip_address'
        assert not NetworkController.is_valid_ip(invalid_ip)
