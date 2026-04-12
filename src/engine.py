import pandas as pd
import time


class BarDataFeedCSV:
    def __init__(self, path):
        df = pd.read_csv(path)

        self.timestamp = df['timestamp'].to_numpy
        self.close = df['close'].to_numpy
        self.open = df['open'].to_numpy
        self.high = df['high'].to_numpy
        self.low = df['low'].to_numpy
        self.volume = df['volume'].to_numpy
        self.i = 0

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i > len(self.close):
            raise StopIteration

        bar = (
            self.timestamp[self.i],
            self.open[self.i],
            self.high[self.i],
            self.low[self.i],
            self.close[self.i],
            self.volume[self.i],
        )
        self.i = self.i + 1
        return bar



def main():
    pass

if __name__ == "__main__":
    feed = BarDataFeedCSV(path="SBER1min.csv")

    start = time.perf_counter()
    for bar in feed:
        pass
    end = time.perf_counter()
    print(f"Execution time {end - start} seconds")