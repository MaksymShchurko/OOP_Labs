from abc import ABC, abstractmethod

# 4.1 Розділяємо один великий інтерфейс на три вузькоспеціалізовані
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

# 4.2 Створюємо IoT-пристрій (згідно з ISP він не має зайвих методів)
class IoTDevice(NetworkConnectable):
    def connect_to_network(self):
        print("IoT-пристрій: Підключено до мережі. Передача даних телеметрії...")

# Смартфон реалізує всі інтерфейси, бо він підтримує всі функції
class Smartphone(Callable, SmsSendable, NetworkConnectable):
    def make_call(self):
        print("Смартфон: Виклик абонента...")

    def send_sms(self):
        print("Смартфон: Надсилання SMS...")

    def connect_to_network(self):
        print("Смартфон: Підключено до 4G/5G мережі")

# Демонстрація роботи
print("--- Тестування ISP ---")

# Працюємо з датчиком
sensor = IoTDevice()
sensor.connect_to_network()
# У sensor немає методів make_call() або send_sms(), тому помилки проектування немає

# Працюємо зі смартфоном
iphone = Smartphone()
iphone.make_call()
iphone.connect_to_network()