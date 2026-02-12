class Person:
    
    def __init__(self):
        # 내가 지불 가능한 결제 방식들.
        self.wallet = {}

    def run(self, vm):
        # self : person instance.
        # vm.run(self)
        vm.run(self.wallet)

    def add_payment(self, payment):
        self.wallet[payment.name] = payment

    def show_budget(self):
        for key, value in self.wallet.items():
            print(key, value)


