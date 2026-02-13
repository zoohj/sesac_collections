class VendingMachine:

    def __init__(self, items):
        self.items = items

    def show_items(self):
        
        for index, item in enumerate(self.items):
            print(index, end=" : ")
            item.show_info()

    def choose_payment(self, wallet):
        for key, payment in wallet:
            print(key, payment)
        choice = input('뭐로 결제할래?')

        return wallet[choice]

    def choose_item(self):
        choice = int(input('뭐살래?'))
        item = self.items[choice]

        if item.stock == 0:
            print('재고가 없습니다.')
            return False, item

        return True, item

    def run(self, wallet):

        # 뭘 살지 보여주고
        self.show_items()

        # 뭘 살지 정하고
        success, item = self.choose_item()

        if not success:
            return

        # 결제 방식을 선택하고
        payment = self.choose_payment(wallet)
        print(f'{payment} 결제를 선택함!')

        # 결제하고
        is_payment_success = payment.pay(item.price)

        if not is_payment_success:
            print('잔액이 부족합니다')
            return


        # 물건 받고
        print(f'{item.name}을 받았습니다.')

        # 재고 줄어들고
        item.stock -= 1
