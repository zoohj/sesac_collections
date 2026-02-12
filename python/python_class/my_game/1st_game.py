'''
my_game.main의 Docstring


캐릭터 - 이름, 역할 

어떻게 싸우는지

역할 클래스 - 전사, 마법사
공격은 똑같음 : 방법이 다름

무기 - 역할마다 (어떤 종류의 도구)

무기를 들어야 필살기를 씀(맨손은 못함)

'''

from abc import ABC, abstractmethod

class Character(ABC):
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.is_weapon = False

    def equip_weapon(self, weapon):
        self.weapon = weapon
        self.is_weapon = True
        
    def attack(self):
        print("맨손 공격")
    
    def special_move(self):
        print("내 손에 있는게 없는데 무슨 필살기냐")
    

class Wizard(Character):
    def __init__(self, name):
        role = "wizard"
        super().__init__(name, role)
    

    def equip_weapon(self, weapon):
        if weapon == "지팡이":
            print("지팡이 장착햇음")
            return super().equip_weapon(weapon)
        else:
            print("안배운걸 어케 쓰라고 주냐")

    def attack(self):
        if self.is_weapon:
            print("지팡이로 얍")
        else: 
            super().attack()
    def special_move(self):
        if self.is_weapon:
            print("익스펙토페트로놈")
        else:
            return super().special_move()
    
class Warrior(Character):
    def __init__(self, name):
        role = "warrior"
        super().__init__(name, role)

    def equip_weapon(self, weapon):
        if weapon == "검":
            print("검 장착햇음")
            return super().equip_weapon(weapon)
        else:
            print("안배운걸 어케 쓰라고 주냐")

    def attack(self): 
        if self.is_weapon:
            print("검으로 얍")
        else: 
            super().attack()

    def special_move(self):
        if self.is_weapon:
            print("강력한 베기")
        else:
            return super().special_move()
    

"""
캐릭터("아더","전사")
도구 장착("_") [지팡이, 검]
공격 - 행동   hj.attack() => 행동
맨손 일반공격은 전사나 마법사나 똑같음
필살기 써(아더)
"""

wizard1= Wizard("hj")
wizard1.attack()
wizard1.equip_weapon("검")
wizard1.special_move()
wizard1.equip_weapon("지팡이")
wizard1.special_move()