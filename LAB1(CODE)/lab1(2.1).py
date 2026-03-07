#2.1
class ServiceTariff:
    def calculate(self, units):
        return 0

class VoiceTariff(ServiceTariff):
    def calculate(self, minutes):
        return minutes * 0.75 # Ціна за хвилину голосу

class DataTariff(ServiceTariff):
    def calculate(self, megabytes):
        return megabytes * 0.15 # Ціна за МБ даних

# 2.2: Розширюємо систему новим класом RoamingTariff
class RoamingTariff(ServiceTariff):
    def calculate(self, units):
        return units * 5.0


def process_billing(tariff, amount):
    print(f"Тариф {tariff.__class__.__name__}: до сплати {tariff.calculate(amount)} грн")

voice = VoiceTariff()
data = DataTariff()
roaming = RoamingTariff()

process_billing(voice, 100)
process_billing(data, 1000)
process_billing(roaming, 10)