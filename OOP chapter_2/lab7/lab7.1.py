import asyncio
import websockets


class WebSocketClient:
    def __init__(self):
        self.connection = None

    async def connect(self, url):
        """Встановлює асинхронне з'єднання з сервером[cite: 41]."""
        try:
            self.connection = await websockets.connect(url)
            print(f"Підключено до: {url}")
        except Exception as e:
            print(f"Помилка підключення: {e}")

    async def send_message(self, message):
        """Надсилає повідомлення серверу[cite: 42]."""
        if self.connection:
            try:
                await self.connection.send(message)
                print(f"Відправлено: {message}")
            except Exception as e:
                print(f"Помилка при відправці: {e}")
        else:
            print("З'єднання не встановлено.")

    async def receive_message(self):
        """Отримує повідомлення від сервера[cite: 43]."""
        if self.connection:
            try:
                response = await self.connection.recv()
                return response
            except Exception as e:
                print(f"Помилка при отриманні: {e}")
                return None
        return None

    async def close_connection(self):
        """Закриває з'єднання[cite: 44]."""
        if self.connection:
            await self.connection.close()
            print("З'єднання закрито.")


async def main():
    # Тестування на реальному сервері [cite: 34, 45]
    uri = "wss://ws.postman-echo.com/raw"
    client = WebSocketClient()

    await client.connect(uri)

    # Відправка та отримання повідомлення [cite: 47]
    await client.send_message("Привіт! Це тестове повідомлення через WebSocket.")
    response = await client.receive_message()

    if response:
        print(f"Отримано від сервера: {response}")

    await client.close_connection()


if __name__ == "__main__":
    asyncio.run(main())