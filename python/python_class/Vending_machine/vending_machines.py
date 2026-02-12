from abc import ABC, abstractmethod
class VendingMachine(ABC):
    pass

class Beverage(VendingMachine):
    def __init__(self, product):
        self.products = product #[a,b,c]
        for product in self.products:
            product.is_active = False
#돈을 넣은 후에 활성화
        self.insertedAmount = 0
    def __str__(self):
        return f"자판기 소유 상품 - {self.product.name}"
    
    def receive_money(self, money):
        print("자판기 돈 받음") 
        self.insertedAmount = money
        for product in self.products:
            if product.price <= money:
                product.is_active = True
        self.show_active_product()

    def show_active_product(self):
        active_product = []
        for product in self.products:
            if product.is_active == True:
                active_product.append(
                )
            print(f"너가 구매할 수 있는 상품이야 {active_product}")
        
    def cell_product(self, product_name):
        if self.product.name == product_name:
            if self.product.is_active == True:
                print(f"{self.product} 나옴")
                change = self.insertedAmount - self.product.price
                print(f"잔돈 받아가라{change}")
                self.insertedAmount = 0 

