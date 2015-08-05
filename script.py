from random import random

for i in range(100):
    print('[', str(list(map(lambda x: int(random()*16), range(32)))) + '\n', str(list(map(lambda x: int(random()*16), range(32)))), '],')
