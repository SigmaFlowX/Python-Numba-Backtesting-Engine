from dataclasses import dataclass
from datetime import datetime

@dataclass
class Signal:
    ticker:str
    side: str
    price: float
    size: float
    timestamp: datetime

@dataclass
class Order:
    ticker:str
    side:str
    size: float
    price: float
    timestamp: datetime

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
    timestamp: datetime
    ticker: str
    open: float
    high: float
    low: float
    close: float
    volume: float

@dataclass
class Fill:
    ticker: str
    side: str
    size: float
    price: float
    timestamp: datetime
    fee: float