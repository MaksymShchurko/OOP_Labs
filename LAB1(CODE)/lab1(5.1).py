from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log(self, message):
        pass

class FileLogger(Logger):
    def log(self, message):
        print(f"[FILE] Запис у лог-файл: {message}")

class ServerLogger(Logger):
    def log(self, message):
        print(f"[SERVER] Відправка логу на віддалений сервер: {message}")

class ConsoleLogger(Logger):
    def log(self, message):
        print(f"[CONSOLE] Вивід логу в консоль: {message}")

class NetworkMonitor:
    def __init__(self, logger: Logger):
        self.logger = logger

    def check_status(self):
        status = "Мережа працює стабільно"
        self.logger.log(status)

# Демонстрація виконання завдання 5.2
if __name__ == "__main__":
    file_logger = FileLogger()
    server_logger = ServerLogger()
    console_logger = ConsoleLogger()

    monitor1 = NetworkMonitor(file_logger)
    monitor1.check_status()

    monitor2 = NetworkMonitor(server_logger)
    monitor2.check_status()

    monitor3 = NetworkMonitor(console_logger)
    monitor3.check_status()