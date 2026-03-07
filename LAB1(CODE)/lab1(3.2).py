class NetworkConnection:
    def connect(self):
        print("Встановлення з'єднання...")

class WifiConnection(NetworkConnection):
    def connect(self):
        print("Wifi connected")

class LTEConnection(NetworkConnection):
    def connect(self):
        print("LTE connected")

class SatelliteConnection(NetworkConnection):
    def connect(self):
        # Реалізація специфічної логіки всередині, щоб не порушувати LSP
        if self._check_signal():
            print("Satellite connection established")
        else:
            print("ERROR, Satellite not found")

    def _check_signal(self):
        return True

def start_communication(connection: NetworkConnection):
    connection.connect()

# Тепер виконуємо код
wifi = WifiConnection()
sat = SatelliteConnection()

print("Wifi test:")
start_communication(wifi)

print("\nSatellite test:")
start_communication(sat)