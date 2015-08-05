from random import random, sample
from human import Human
from virus import Virus
from battle_dmg import analyzer
from queue import Queue

mutation_human = 0.0001 # 1만분의 1
mutation_virus = 0.0001   # 만분의 1
cvt_table = [
[1, 1], [1, 2], [1, 3], [1, 4],
[2, 1], [2, 2], [2, 3], [2, 4],
[3, 1], [3, 2], [3, 3], [3, 4],
[4, 1], [4, 2], [4, 3], [4, 4]]

class GenePool:
    failure = [None] * 100

    def __init__(self, first_human, tr):
        self.human_pool = first_human
        self.human_pool[32].virus = Virus()
        self.human_pool[65].virus = Virus()
        self.breedable = set()
        self.infenction_schd = {}
        self.battle = analyzer()
        self.years = tr
        self.last_match = self.max =  0
        self.die_years = [0] * 2000
        self.dy_pos = 0
        self.lastdeath = 0
        while self.process():
            pass

    def breed(self, parents, pos):
        parent1, parent2 = parents
        if self.human_pool[pos] != None:
            print('[!] Human exists')
            return -1

        b1 = self.human_pool[parent1].base[int(random()*2)]
        for id_, base in enumerate(b1):
            if random() < mutation_human:
                tmp = cvt_table[base]
                tmp[int(random() * 2)] = int(random() * 4) + 1
                b1[id_] = (tmp[0] - 1) * 4 + tmp[1]
                if b1[id_] == 16:
                    b1[id_] -= 1

        b2 = self.human_pool[parent2].base[int(random()*2)]
        for id_, base in enumerate(b2):
            if random() < mutation_human:
                tmp = cvt_table[base]
                tmp[int(random() * 2)] = int(random() * 4) + 1
                b2[id_] = (tmp[0] - 1) * 4 + tmp[1]
                if b2[id_] == 16:
                    b2[id_] -= 1

        self.human_pool[pos] = Human(3000, (b1, b2))
        #print('[%d] %d, %d breed to' % (self.years.value, parent1, parent2), pos)

    def clone(self, pos):
        if pos < 99:
            tmp = self.human_pool[pos].virus.base
            for id_, base in enumerate(tmp):
                if random() < mutation_virus:
                    m = cvt_table[base]
                    m[int(random() * 2)] = int(random() * 4) + 1
                    tmp[id_] = (m[0] - 1) * 4 + m[1]
                    if tmp[id_] == 16:
                        tmp[id_] -= 1

            self.infenction_schd[pos + 1] = Virus(tmp)

        if pos > 0:
            tmp = self.human_pool[pos].virus.base
            for id_, base in enumerate(tmp):
                if random() < mutation_virus:
                    m = cvt_table[base]
                    m[int(random() * 2)] = int(random() * 4) + 1
                    tmp[id_] = (m[0] - 1) * 4 + m[1]
                    if tmp[id_] == 16:
                        tmp[id_] -= 1

            self.infenction_schd[pos - 1] = Virus(tmp)
        #print('clone from', pos)

    def unit_process(self, pos):
        if self.human_pool[pos] == None:
            return

        try:
            self.human_pool[pos].virus = self.infenction_schd[pos]
            del self.infenction_schd[pos]
        except KeyError:
            pass
        if self.human_pool[pos].health < 0:
            self.clone(pos)
            self.die_years[self.dy_pos] = self.human_pool[pos].years
            self.dy_pos += 1
            self.dy_pos %= 2000
            self.human_pool[pos] = None
            #print("[%d]" % self.years.value, pos, 'died')
            self.lastdeath = self.years.value
            try:
                self.breedable.remove(pos)
            except KeyError:
                pass
            return

        if self.human_pool[pos].virus != None:
            self.human_pool[pos].health -= self.battle.battle(self.human_pool[pos].virus.base, self.human_pool[pos].visible)

        self.human_pool[pos].years += 1
        if self.human_pool[pos].years > 20:
            self.breedable.add(pos)

        #TODO: Reporting, average lifetime calculation

    def process(self):
        self.years.value += 1
        if self.human_pool == GenePool.failure:
            return False

        deadland = list()
        for human in range(len(self.human_pool)):
            self.unit_process(human)
            if self.human_pool[human] == None: #Dead!
                deadland.append(human)
        if len(self.breedable) > 1:
            for land in deadland:
                self.breed(tuple(sample(self.breedable, 2)), land)
        avg = 0
        for i in range(2000):
            avg += self.die_years[i]

        avg /= 2000
        if int(avg) != self.last_match:
            if self.max < int(avg):
                self.max = int(avg)
                print('[%d], Average %d' % (self.years.value, avg))
            else:
                print('[%d], Average %d, Max %d' % (self.years.value, avg, self.max))
            self.last_match = int(avg)


        '''if self.years.value > self.lastdeath + 1000:
            for human in range(63, 73):
                if self.human_pool[human] != None:
                    print(human, self.human_pool[human].base)
                else:
                    print(self.human_pool[human])
            print(self.human_pool)
            print(self.breedable)
            self.battle.print_()
            return False'''

        return True
