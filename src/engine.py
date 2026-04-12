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
        self.reader = csv.DictReader(self.file)

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        row = next(self.reader)
        return Bar(
            timestamp=row["timestamp"],
            open=float(row["open"]),
            high=float(row["high"]),
            low=float(row["low"]),
            close=float(row["close"]),
            volume=float(row["volume"]),
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