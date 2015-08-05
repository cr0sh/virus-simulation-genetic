from human import Human
from virus import Virus
from genepool import GenePool
from time_report import trProcess
from multiprocessing import Value

def entry_point(*args):
    times = Value('L', 0)
    #trProcess(times).start()
    pool = GenePool(list(map(lambda x: Human(3000), range(100))), times)

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point()
