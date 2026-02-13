'''
my_game.2nd_game의 Docstring

캐릭터
이름, 직업, 무기
공격하기
필살기사용

직업(추상)- 마법사, 전사
공격방식
장착 가능 무기 리스트

무기(추상) - 검, 지팡이
고유 스킬 이름
'''



from abc import ABC, abstractmethod




class Weapon(ABC):
    def __init__(self, name, skill_name):
        self.name = name
        self.skill_name = skill_name
    @abstractmethod
    def skill_name(self):
        pass

class Sword(Weapon):
    def __init__(self):
        super().__init__()
    def skill_name(self):
        pass09
        
class Staff(Weapon):
    def __init__(self):
        self.name = "검"
        self.skill_name = "슁슁쉥쉥"

class Role(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def attack_message(self):
        pass
    @abstractmethod
    def possible_weapon_list(self):
        pass

class Wizard(Role):
    def __init__(self):
        super().__init__()
    def attack_message(self):
        print("익스펙토페트로놈")

class Warior(Role):
    def __init__(self):
        super().__init__()
    def attack_message(self):
        return print("슁슁쉥쉥")

class Character:
    def __init__(self, name, role):
        self.name = name
        self.role = role
    
    def attack():
        pass

    def special_move():
        pass