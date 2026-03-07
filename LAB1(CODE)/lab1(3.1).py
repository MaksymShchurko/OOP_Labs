#3.1
class NetworkConnetion():
    def connect(self):
        print("Connecting to the Network...")

class WiFiConnection(NetworkConnetion):
    def connect(self):
        print("WiFi connected!")

class LTE(NetworkConnetion):
    def connect(self):
        print("LTE connected!")

def establish_communication(connection: NetworkConnetion):
    connection.connect()

wifi = WiFiConnection()
lte = LTE()

establish_communication(wifi)
establish_communication(lte)
