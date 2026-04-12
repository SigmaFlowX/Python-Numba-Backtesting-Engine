import csv
from DataClasses import Bar
import time


class DataFeedCSV:
    def __init__(self, path: str):
        self.path = path
        self.file = None
        self.reader = None

    def reset(self):
        if self.file:
            self.file.close()

        self.file = open(self.path, "r")
        next(self.file)

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        line = next(self.file)
        ts, o, h, l, c, v, *_ = line.strip().split(",")

        return Bar(
            timestamp=ts,
            open=float(o),
            high=float(h),
            low=float(l),
            close=float(c),
            volume=float(v),
        )

def main():
    pass

if __name__ == "__main__":
    feed = DataFeedCSV(path="SBER1min.csv")

    start = time.perf_counter()
    for bar in feed:
        pass
    end = time.perf_counter()
    print(f"Execution time {end - start} seconds")