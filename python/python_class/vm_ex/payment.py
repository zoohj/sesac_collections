from abc import ABC, abstractmethod

class Payment(ABC):
    
    def __init__(self, money, name):
        # 결제 한도 금액
        self.name = name
        self.money = money

    def pay(self, price):
        if self.money >= price:
            self.money -= price
            return True
        
        elif self.money < price:
            return False


    def __str__(self):
        return f"{self.name}"

class CardPayment(Payment):
    pass

class CashPayment(Payment):
    pass