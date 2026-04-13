import pandas as pd
import time
from DataClasses import Bar, Signal, Order, Fill


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
    def __init__(self):
        self.prices = []

    def on_bar(self, bar: Bar):
        self.prices.append(bar.close)

        if len(self.prices) < 10:
            return None

        if bar.close > sum(self.prices[-10:]) / 10:
            return Signal(side="BUY", size=1, price=bar.close)

    def on_event(self, event):
        if isinstance(event, Bar):
            return self.on_bar(event)


class Portfolio:
    def __init__(self):
        self.position = 0
        self.cash = 1_000_000

    def on_signal(self, signal):
        if signal.side == "BUY":
            return Order("BUY", signal.size, signal.price)
        elif signal.side == "SELL":
            return Order("SELL", signal.size, signal.price)

    def on_fill(self, fill):
        if fill.side == "BUY":
            self.position += fill.size
            self.cash -= fill.size * fill.price

        elif fill.side == "SELL":
            self.position -= fill.size
            self.cash += fill.size * fill.price


class Execution:
    def execute(self, order):
        return Fill(order.side, order.size, order.price)

class Engine:
    def __init__(self, datafeed: BarDataFeedCSV, strategy: Strategy):
        self.feed = datafeed
        self.strategy = strategy

    def run(self):

        for event in self.feed:
            signal = self.strategy.on_event(event)
            print(signal)



def main():
    pass

if __name__ == "__main__":
    feed = BarDataFeedCSV(path="SBER1min.csv")

    start = time.perf_counter()
    close = feed.close


    engine = Engine(datafeed=feed, strategy=Strategy())
    engine.run()

    end = time.perf_counter()

    print(f"Execution time {end - start} seconds")