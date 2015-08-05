class Virus:
    def __init__(self, base_set=None):
        if base_set != None and len(base_set) == 8:
            self.base = base_set
        else:
            # list(map(lambda x: int(random()*16), range(8)))
            self.base = [4, 10, 12, 8, 2, 9, 12, 6] #초기값 임의 설정

        self.attacks = 0
