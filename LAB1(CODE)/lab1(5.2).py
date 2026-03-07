from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log(self, message):
        pass

class FileLogger(Logger):
    def log(self, message):
        print(f"[FILE] Запис у файл: {message}")

class ServerLogger(Logger):
    def log(self, message):
        print(f"[SERVER] Відправка на сервер: {message}")

class ConsoleLogger(Logger):
    def log(self, message):
        print(f"[CONSOLE] Вивід у консоль: {message}")

class NetworkMonitor:
    def __init__(self, logger: Logger):
        self.logger = logger

    def check_status(self):
        status = "Мережа працює стабільно"
        self.logger.log(status)

if __name__ == "__main__":
    file_log = FileLogger()
    server_log = ServerLogger()
    console_log = ConsoleLogger()

    monitor1 = NetworkMonitor(file_log)
    monitor1.check_status()

    monitor2 = NetworkMonitor(server_log)
    monitor2.check_status()

    monitor3 = NetworkMonitor(console_log)
    monitor3.check_status()