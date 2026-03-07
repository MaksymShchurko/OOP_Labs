class Subscriber:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

class SmsService:
    def send_sms(self, phone, massage):
        print(f"Sending SMS on {phone}: {massage}")


class BalanceCalculator:
    def calculate_balance(self, tariff_rate, duration):
        return tariff_rate * duration

sub = Subscriber("Maks", "+380999111233")
sms = SmsService()
calc = BalanceCalculator()

sms.send_sms(sub.phone, "your balacne increased")
current_balance = calc.calculate_balance(1.5, 20)
print(f"Balance status:{sub.name}, {current_balance} грн")