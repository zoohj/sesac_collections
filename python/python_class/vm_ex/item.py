class Item:

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.name} : 가격 {self.price}"
    
    def show_info(self):
        if self.stock > 0:
            text = '재고 있음'
        else:
            text = '재고 없음'
        print(f"{self.name} / {self.price}원 / {text}")


