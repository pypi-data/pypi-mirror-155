import tqdm
import sys
import logging
import threading

logger = logging.getLogger("Main")


class TqdmManager:

    TQDM_MIN_LABEL = 50

    def __init__(self):
        self.items = {}         # key = HMC name, value = list of tqdm objects
        self.freePosition = 0   # first tqdm free slot
        self.lock = threading.Lock()


    def add(self, key, num):
        self.lock.acquire()
        self.items[key] = [tqdm.tqdm(position=n+self.freePosition,
                            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}', 
                            leave=False, 
                            file=sys.stdout,) for n in range(0, num)]
        self.freePosition += num
        self.lock.release()


    def reset(self, key, level, total):
        self.lock.acquire()
        self.items[key][level].reset(total=total)
        emptyLabel = f'{"":<{TqdmManager.TQDM_MIN_LABEL}}'
        self.items[key][level].set_description(
            f'{emptyLabel:<{TqdmManager.TQDM_MIN_LABEL}}')
        self._reset(key, level+1)
        self.lock.release()


    def setDescription(self, key, level, label):
        if level == 0:
            label = f'{key}: {label}'
        else:
            label = ' '*(level-1)*3 + '`- ' + label
        self.lock.acquire()
        self.items[key][level].set_description(
            f'{label:<{TqdmManager.TQDM_MIN_LABEL}}')
        self._reset(key, level+1)
        self.lock.release()

    
    def update(self, key, level, num):
        self.lock.acquire()
        self.items[key][level].update(num)
        self._reset(key, level+1)
        self.lock.release()


    def _reset(self, key, level):
        emptyLabel = f'{"":<{TqdmManager.TQDM_MIN_LABEL}}'
        for n in range(level, len(self.items[key])):
            self.items[key][n].reset(total=0)
            self.items[key][n].set_description(emptyLabel)


    def refresh(self):
        self.lock.acquire()
        for items in self.items.values():
            for n in range(0, len(items)):
                items[n].refresh()
        self.lock.release()


    def close(self):
        self.lock.acquire()
        for items in self.items.values():
            for n in range(0, len(items)):
                items[n].close()
        self.lock.release()  

