from dataclasses import dataclass

@dataclass
class Signal:
    side: str
    size: float

@dataclass
class Order:
    side:str
    size: float
    price: float

@dataclass
class OrderBook:
    ticker:str
    bids: dict[float, float]
    asks: dict[float, float]

@dataclass
class Position:
    size: float
    entry_price: float

@dataclass
class Bar:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float