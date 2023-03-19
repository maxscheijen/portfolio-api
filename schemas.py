from typing import List
from pydantic import BaseModel


class Transaction(BaseModel):
    date: str
    amount: float
    price: float
    fee: float = 0


class Asset(BaseModel):
    id: str
    symbol: str
    current_price: float
    price_change_24h: float
    total_dividend: float
    type: str
    transactions: List[Transaction]
    history: List[dict]

class CurrentPrice(BaseModel):
    ticker: str
    current_price: float
    last_updated: str
