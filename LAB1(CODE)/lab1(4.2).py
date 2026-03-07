from abc import ABC, abstractmethod

# 4.1 Розділені інтерфейси (з попереднього кроку)
class Callable(ABC):
    @abstractmethod
    def make_call(self):
        pass

class SmsSendable(ABC):
    @abstractmethod
    def send_sms(self):
        pass

class NetworkConnectable(ABC):
    @abstractmethod
    def connect_to_network(self):
        pass

# 4.2 Спеціалізований IoT-пристрій
# Він наслідує ТІЛЬКИ NetworkConnectable, бо йому потрібна лише мережа
class IoTDevice(NetworkConnectable):
    def connect_to_network(self):
        print("IoT-датчик: Встановлено з'єднання з вишкою зв'язку. Передача телеметрії...")

# Смартфон реалізує всі інтерфейси (множинне успадкування)
class Smartphone(Callable, SmsSendable, NetworkConnectable):
    def make_call(self):
        print("Смартфон: Здійснюється голосовий дзвінок.")

    def send_sms(self):
        print("Смартфон: SMS надіслано.")

    def connect_to_network(self):
        print("Смартфон: Підключено до мережі 4G/5G.")

# --- Перевірка роботи коду ---

print("Тест IoT-пристрою:")
sensor = IoTDevice()
sensor.connect_to_network()
# У об'єкта sensor немає методів make_call() або send_sms(),
# що повністю відповідає принципу ISP.

print("\nТест Смартфона:")
phone = Smartphone()
phone.make_call()
phone.connect_to_network()