from payments import Cash
class Customer:
    def __init__(self, name, payment_method):
        self.name = name
        self.payment_method = payment_method
        self.selected_vm = None
    
    def insert_money(self, vm, money):
        # 현금 넣음
        print("돈 넣음")
        self.selected_vm = vm
        # if payment == Cash():
        self.selected_vm.receive_money(money)
    
    def select_product(self, product_name):
        self.selected_vm.cell_product(product_name)

    def purchase(self, product_name):
        self.vending_machine.purchase
        pass




'''

뭘해야하는데?-

1. 자판기 선택 (음료수, 과자) 자판기 이름도 있어야겠네 이름보다는 카테고리..?

2. 사용자가 가지고있는 결제방식으로 물건 구매 - 자판기가 가능한 결제방식인지(기본은 그냥 다되는걸로 해놓자)

3. 자판기 안에 있는 물건 중 하나 선택

물건이 뭐가 있는지 알려줘야할 듯

3. 결제(자판기가 가능한지 안한지 확인)

product, payment

'''