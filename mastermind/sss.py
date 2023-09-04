from mastermind.src.net.network_controller import NetworkController


class SSS:
    def runder(self):
        net = NetworkController()
        net.set_ip("127.0.0.1")
        net.set_port(3000)
        net.network_log = True
        net.transmit("Test")

if __name__ == "main":
    SSS.runder