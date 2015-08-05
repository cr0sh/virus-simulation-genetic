from random import random

class Human:

    @staticmethod
    def mix(b1, b2):
        if b1 == b2:
            return b1

        even = (b1 % 2, b2 % 2)
        if even[0] == even[1]:
            if b1 > b2:
                return b1
            else:
                return b2
        elif even[0] > even[1]:
            return b1
        else:
            return b2

    def __init__(self, health, base_set = None): #100*0=3000이 권장됨 (초기수명 30으로 설정)
        if base_set != None and len(base_set) == 2:
            self.base = base_set
        else:
            if base_set != None:
                print('[!] base_set is malformed')
                print(base_set)

            self.base = [list(map(lambda x: int(random()*16), range(32))), list(map(lambda x: int(random()*16), range(32)))]

        self.visible = []

        for i in range(32):
            self.visible.append(Human.mix(self.base[0][i], self.base[0][i]))

        self.health = health
        self.years = 0
        self.virus = None
