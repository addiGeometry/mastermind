"""
Die Netzwerkkontrolle erfolgt durch den NetworkController
"""
import ipaddress
import json
import requests


class NetworkController:
    """Diese Klasse sendet Requests über das Netzwerk und empfängt sie"""

    def __init__(self):
        self.ip = ""
        self.port = -1
        self.headers = {'Content-Type': 'application/json'}
        self.network_log = False

    def set_ip(self, ip):
        """Setzt die IP Addresse"""
        self.ip = ip

    def set_port(self, port):
        self.port = port

    def transmit(self, request):
        print(request)
        """Sendet Nachricht über Netzwerk und empfängt Antwort"""
        answer = requests.post(f"http://{self.ip}:{self.port}/",
                               data=json.dumps(request),
                               headers=self.headers,
                               timeout=10)
        if self.network_log:
            print(f"Answer: {answer.json()}")
        return answer

    @staticmethod
    def is_valid_ip(ip):
        """ Überprüft eine IP"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
