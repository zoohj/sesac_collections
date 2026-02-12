from person import Person
from vending_machine import VendingMachine
from payment import CardPayment, CashPayment
from item import Item

cola = Item('콜라', 1000, 4)
cider = Item('사이다', 1100, 3)
water = Item('물', 500, 0)

vm = VendingMachine([cola, cider, water])

me = Person()

card = CardPayment(10000, '카드')
cash = CashPayment(15000, '현금')

# 내가 card, cash를 들고있다.
me.add_payment(card)
me.add_payment(cash)

# me.show_budget()
me.run(vm)