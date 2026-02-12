'''
Vending_machine.main의 Docstring

사람이 자판기에서 물건 구입
현금결제, 카드결제

사람은 이름, 결제방식(payment_method)

자판기는 상품을 가지고 있음 결제방식도 자판기마다 다름

상품 - 상품명, 가격 

'''

from customers import Customer
from payments import Cash, Card
from vending_machines import Beverage
from products import Product


me = Customer("현지", Cash())
# you = Customer("유지", Card())

#자판기 설정
a=Product("솔의눈", 2000)
b=Product("피크닉", 1500)
c=Product("생수", 1000)
beverage_vending_machine = Beverage(a)


print(me.payment_method)
print(beverage_vending_machine)
#내가 구매? 자판기에서 구매? 내가 구매해야지 상품 선택도해야하는디 
# 내가 상품을 선택해서 구매

me.insert_money(beverage_vending_machine,2000)

# 결제가 완료되었습니다. 사용자가 가지고있는 방식으로 자동 결제? 아니면 가격 넣기?
# 물건 나와

me.select_product("솔의눈")


'''
뭘해야하는데?- 
1. 자판기 선택 (음료수, 과자) 자판기 이름도 있어야겠네 이름보다는 카테고리..?
2. 사용자가 가지고있는 결제방식으로 물건 구매 - 자판기가 가능한 결제방식인지(기본은 그냥 다되는걸로 해놓자)
3. 자판기 안에 있는 물건 중 하나 선택
물건이 뭐가 있는지 알려줘야할 듯
3. 결제(자판기가 가능한지 안한지 확인)
product, payment
상태..?
준비 상태, 잔액 충전 상태, 재고 부족 상태, 결제 처리
'''
