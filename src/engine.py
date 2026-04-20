import pandas as pd
import time
from DataClasses import Bar, Signal, Order, Fill
import matplotlib.pyplot as plt


class BarDataFeedCSV:
    def __init__(self, path, resample_tf = None):
        df = pd.read_csv(path)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')

        if resample_tf:
            df = df.resample(resample_tf).agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()

        self.timestamp = df.index
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

class MetricsCollector:
    def __init__(self):
        self.positions = []
        self.trades = []
        self.equity_curve = []
        self.timestamps = []
        self.prices = []

    def on_fill(self, fill):
        self.trades.append(fill)

    def on_bar(self, bar, portfolio):
        equity = portfolio.cash + portfolio.position * bar.close
        self.equity_curve.append(equity)
        self.timestamps.append(bar.timestamp)
        self.prices.append(bar.close)

    def on_event(self, event, portfolio):
        if isinstance(event, Bar):
            return self.on_bar(event, portfolio)

class MetricsAnalyzer:
    def __init__(self, metrics: MetricsCollector):
        self.metrics = metrics

    def plot_equity(self):
        plt.plot(self.metrics.timestamps, self.metrics.equity_curve)
        plt.grid()
        plt.title("Equity over time")
        plt.show()

    def plot_trades(self):
        plt.plot(self.metrics.timestamps, self.metrics.prices)

        sell_ts = []
        buy_ts = []
        buy_prices = []
        sell_prices = []

        for fill in self.metrics.trades:
            if fill.side == "BUY":
                buy_ts.append(fill.timestamp)
                buy_prices.append(fill.price)
            elif fill.side == "SELL":
                sell_ts.append(fill.timestamp)
                sell_prices.append(fill.price)

        plt.grid()
        plt.title("Trades")
        plt.scatter(buy_ts, buy_prices, color="green")
        plt.scatter(sell_ts, sell_prices, color="red")
        plt.show()




class Strategy:
    def __init__(self, fast_ma_window=5, slow_ma_window=20):
        self.prices = []
        self.fast_ma_window = fast_ma_window
        self.slow_ma_window = slow_ma_window

        self.prev_slow_ma = None
        self.prev_fast_ma = None

    def on_bar(self, bar: Bar, portfolio):
        self.prices.append(bar.close)

        if len(self.prices) < self.slow_ma_window:

            return None
        fast_ma = sum(self.prices[-self.fast_ma_window:]) / self.fast_ma_window
        slow_ma = sum(self.prices[-self.slow_ma_window:]) / self.slow_ma_window

        signal = None

        if self.prev_fast_ma is not None and self.prev_slow_ma is not None:
            if self.prev_fast_ma <= self.prev_slow_ma and fast_ma > slow_ma and portfolio.position == 0:
                signal = Signal(
                    side="BUY",
                    size=5,
                    price=bar.close,
                    timestamp=bar.timestamp
                )
            elif self.prev_fast_ma >= self.prev_slow_ma and fast_ma < slow_ma and portfolio.position > 0:
                signal = Signal(
                    side="SELL",
                    size=portfolio.position,
                    price=bar.close,
                    timestamp=bar.timestamp
                )

        self.prev_fast_ma = fast_ma
        self.prev_slow_ma = slow_ma

        return signal

    def on_event(self, event, portfolio):
        if isinstance(event, Bar):
            return self.on_bar(event, portfolio)


class Portfolio:
    def __init__(self):
        self.position = 0
        self.cash = 10_000

    def on_signal(self, signal):
        if signal.side == "BUY" and self.cash >= signal.size * signal.price:
            return Order("BUY", signal.size, signal.price, signal.timestamp)
        elif signal.side == "SELL":
            return Order("SELL", signal.size, signal.price, signal.timestamp)

    def on_fill(self, fill):
        if fill.side == "BUY":
            self.position += fill.size
            self.cash -= fill.size * fill.price

        elif fill.side == "SELL":
            self.position -= fill.size
            self.cash += fill.size * fill.price


class Execution:
    def execute(self, order):
        return Fill(order.side, order.size, order.price, order.timestamp)

class Engine:
    def __init__(self, datafeed: BarDataFeedCSV, strategy: Strategy, portfolio: Portfolio, execution: Execution, metrics: MetricsCollector):
        self.feed = datafeed
        self.strategy = strategy
        self.portfolio = portfolio
        self.execution = execution
        self.metrics = metrics

    def run(self):

        for event in self.feed:
            self.metrics.on_event(event, self.portfolio)
            signal = self.strategy.on_event(event, self.portfolio)
            if signal:
                order = self.portfolio.on_signal(signal)

                fill = self.execution.execute(order)
                self.metrics.on_fill(fill)

                self.portfolio.on_fill(fill)


def main():
    pass

if __name__ == "__main__":
    feed = BarDataFeedCSV(path="SBER1min.csv", resample_tf="1h")

    start = time.perf_counter()

    engine = Engine(datafeed=feed, strategy=Strategy(), portfolio=Portfolio(), execution=Execution(), metrics=MetricsCollector())
    engine.run()

    end = time.perf_counter()

    print(f"Execution time {end - start} seconds")

    analyzer = MetricsAnalyzer(engine.metrics)
    analyzer.plot_trades()
    analyzer.plot_equity()