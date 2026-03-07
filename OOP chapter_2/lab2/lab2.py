import asyncio
import random
import time
import networkx as nx
import matplotlib.pyplot as plt


# --- 1. КЛАСИ ОБ'ЄКТІВ (ООП) ---

class Packet:
    def __init__(self, src_name, dest_name, protocol="TCP"):
        self.src = src_name
        self.dest = dest_name
        self.protocol = protocol
        self.path = []


class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []  # Для зірки (двосторонні зв'язки)
        self.next_node = None  # Для кільця (послідовний зв'язок)

    async def transfer(self, packet, network, mode="star"):
        packet.path.append(self.name)

        if self.name == packet.dest:
            return True

        # Симуляція затримки та ймовірності втрати
        await asyncio.sleep(random.uniform(0.05, 0.15))
        if random.random() < network.loss_rate:
            network.packets_lost += 1
            return False

        if mode == "star":
            # Логіка зірки: якщо ми не ціль, передаємо сусідам (через роутер)
            for neighbor in self.connections:
                if neighbor.name not in packet.path:
                    return await neighbor.transfer(packet, network, mode)
        else:
            # Логіка кільця: тільки наступному вузлу
            if self.next_node:
                return await self.next_node.transfer(packet, network, mode)

        return False


# --- 2. КЛАС КЕРУВАННЯ МЕРЕЖЕЮ ---

class NetworkSimulation:
    def __init__(self, name, loss_rate=0.1):
        self.name = name
        self.nodes = []
        self.loss_rate = loss_rate
        self.packets_sent = 0
        self.packets_lost = 0
        self.total_time = 0

    async def run_test(self, src_idx, dest_idx, mode="star", protocol="TCP"):
        self.packets_sent += 1
        src = self.nodes[src_idx]
        dest = self.nodes[dest_idx]
        packet = Packet(src.name, dest.name, protocol)

        start = time.time()
        success = await src.transfer(packet, self, mode)
        duration = time.time() - start

        if success:
            self.total_time += duration
            print(
                f"[{self.name}] {protocol}: {src.name} -> {dest.name} | Успішно за {duration:.3f}с | Шлях: {' -> '.join(packet.path)}")
        else:
            print(f"[{self.name}] {protocol}: {src.name} -> {dest.name} | ПОМИЛКА (Втрата або розрив)")

    def report(self):
        success = self.packets_sent - self.packets_lost
        avg_delay = self.total_time / success if success > 0 else 0
        throughput = success / self.total_time if self.total_time > 0 else 0
        print(f"\n--- ЗВІТ ПРОДУКТИВНОСТІ: {self.name} ---")
        print(f"Відправлено: {self.packets_sent} | Втрачено: {self.packets_lost}")
        print(f"Сер. затримка: {avg_delay:.4f} с | Пропускна здатність: {throughput:.2f} пак/с\n")

    def draw(self, is_ring=False):
        # Використовуємо DiGraph для обох, щоб стрілки показували напрямок руху
        G = nx.DiGraph()

        for node in self.nodes:
            if is_ring:
                G.add_edge(node.name, node.next_node.name)
            else:
                # Для зірки малюємо зв'язки від периферії до центру і навпаки
                for conn in node.connections:
                    G.add_edge(node.name, conn.name)

        plt.figure(figsize=(7, 6))

        # Вибір алгоритму розташування вузлів
        pos = nx.circular_layout(G) if is_ring else nx.spring_layout(G)

        # Виправлений виклик функції малювання
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color='skyblue' if not is_ring else 'lightgreen',
            node_size=1500,
            arrowsize=20,  # Розмір стрілки
            arrows=True,  # Явно вказуємо малювати стрілки (виправляє помилку)
            font_weight='bold',
            connectionstyle='arc3, rad = 0.1'  # Трохи згинаємо лінії для краси
        )

        plt.title(f"Топологія: {self.name}")
        plt.show()


# --- 3. ГОЛОВНИЙ ЗАПУСК ---

async def main():
    # --- СТВОРЕННЯ ЗІРКИ ---
    star_net = NetworkSimulation("STAR_NETWORK")
    router = Node("Central_Router")
    pcs = [Node(f"PC_{i}") for i in range(1, 5)]
    star_net.nodes = [router] + pcs
    for pc in pcs:
        router.connections.append(pc)
        pc.connections.append(router)

    # --- СТВОРЕННЯ КІЛЬЦЯ ---
    ring_net = NetworkSimulation("RING_NETWORK")
    nodes_r = [Node(f"RingNode_{i}") for i in range(1, 6)]
    ring_net.nodes = nodes_r
    for i in range(len(nodes_r)):
        nodes_r[i].next_node = nodes_r[(i + 1) % len(nodes_r)]

    # --- ЗАПУСК СИМУЛЯЦІЇ ---
    print("=== ЗАПУСК МОДЕЛЮВАННЯ ТРАФІКУ ===\n")

    # Симуляція для Зірки (TCP)
    tasks_star = [star_net.run_test(1, 3, "star", "TCP"), star_net.run_test(2, 4, "star", "TCP")]

    # Симуляція для Кільця (UDP)
    tasks_ring = [ring_net.run_test(0, 3, "ring", "UDP"), ring_net.run_test(4, 1, "ring", "UDP")]

    await asyncio.gather(*tasks_star, *tasks_ring)

    # --- ЗВІТИ ТА ВІЗУАЛІЗАЦІЯ ---
    star_net.report()
    ring_net.report()

    star_net.draw(is_ring=False)
    ring_net.draw(is_ring=True)


if __name__ == "__main__":
    asyncio.run(main())