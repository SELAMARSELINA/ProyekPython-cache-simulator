import threading, time, random

THREADS = 4
BLOCKS = 10
ITER = 50

class Simulasi:
    def __init__(self, koheren):
        self.cache = [{} for _ in range(THREADS)]
        self.memori = [0]*BLOCKS
        self.traffic = 0
        self.hit = [0]*THREADS
        self.miss = [0]*THREADS
        self.koheren = koheren

    def read(self, tid, addr):
        if addr in self.cache[tid]:
            self.hit[tid] += 1
        else:
            self.miss[tid] += 1
            self.cache[tid][addr] = self.memori[addr]
            self.traffic += 1

    def write(self, tid, addr, val):
        if self.koheren:
            for i in range(THREADS):
                if i != tid and addr in self.cache[i]:
                    del self.cache[i][addr]
                    self.traffic += 1
        self.cache[tid][addr] = val
        self.memori[addr] = val
        self.traffic += 1

    def tugas(self, tid):
        for _ in range(ITER):
            a = random.randint(0, BLOCKS-1)
            if random.random() < 0.6:
                self.read(tid, a)
            else:
                self.write(tid, a, random.randint(1, 100))

    def jalankan(self):
        t0 = time.time()
        ths = [threading.Thread(target=self.tugas, args=(i,)) for i in range(THREADS)]
        for t in ths: t.start()
        for t in ths: t.join()
        print(f"Koherensi: {self.koheren} | Traffic: {self.traffic} | Hits: {sum(self.hit)} | Misses: {sum(self.miss)} | Waktu: {time.time()-t0:.2f}s")

if __name__ == "__main__":
    Simulasi(False).jalankan()
    Simulasi(True).jalankan()
