

import time

class Timer:
    def __init__(self):
        self.start = time.perf_counter()
        self.last = self.start

    def lap(self, label=""):
        now = time.perf_counter()
        dt = now - self.last
        #print(f"[{label}] Δt = {dt:.4f} s")
        self.last = now
        return dt

    def total(self):
        #print(f"Total elapsed = {time.perf_counter() - self.start:.4f} s")
        return (time.perf_counter() - self.start)