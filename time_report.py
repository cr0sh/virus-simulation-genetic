import signal, os
from multiprocessing import Process
from time import time

class trProcess(Process):
    def __init__(self, years):
        super().__init__()
        self.years = years

    def sighand(self, *args):
        os.kill(os.getpid(), signal.SIGTERM)

    def run(self):
        last = 0
        signal.signal(signal.SIGINT, self.sighand)
        while True:
            try:
                if time() - last > 3: #3초간격
                    print(self.years.value)
                    last = time()
            except KeyboardInturrupt:
                pass
