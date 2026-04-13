import pandas as pd
import time
from DataClasses import Bar


class BarDataFeedCSV:
    def __init__(self, path):
        df = pd.read_csv(path)

        self.timestamp = df['timestamp'].to_numpy()
        self.close = df['close'].to_numpy()
        self.open = df['open'].to_numpy()
        self.high = df['high'].to_numpy()
        self.low = df['low'].to_numpy()
        self.volume = df['volume'].to_numpy()
        self.i = 0

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= len(self.close):
            raise StopIteration

        i = self.i
        self.i = i + 1
        return Bar(
            timestamp=self.timestamp[i],
            open=self.open[i],
            high=self.high[i],
            low=self.low[i],
            close=self.close[i],
            volume=self.volume[i]
        )

class Strategy:
    pass

class Engine:
    def __init__(self, datafeed: BarDataFeedCSV, strategy: Strategy):
        self.feed = datafeed
        self.strategy = strategy

    def run(self):

        for event in self.feed:
            pass



def main():
    pass

if __name__ == "__main__":
    feed = BarDataFeedCSV(path="SBER1min.csv")

    start = time.perf_counter()
    close = feed.close

    strategy = Strategy()
    engine = Engine(datafeed=feed, strategy=strategy)
    engine.run()

    end = time.perf_counter()

    print(f"Execution time {end - start} seconds")