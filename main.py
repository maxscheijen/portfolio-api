from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, status, HTTPException
from yfinance import Ticker

from prices import get_prices, transactions
from schemas import Asset, CurrentPrice

app = FastAPI()


@app.get("/ping/", status_code=status.HTTP_200_OK)
def api_status():
    return {"status": "OK", "status_code": status.HTTP_200_OK}


@app.get("/prices/current", status_code=status.HTTP_200_OK)
async def price_asset(ticker: str, exchange: Optional[str] = None) -> CurrentPrice:
    if exchange:
        ticker = ticker + "." + exchange
    try:
        price = Ticker(ticker=ticker.upper()).history(period="1d")["Close"].iloc[0]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{ticker} can not be found or is not valid. You could also try specifying an exchange.")
    return CurrentPrice(ticker=ticker, current_price=price, last_updated=str(datetime.now().date()))


@app.get("/portfolio/type/list")
def get_type():
    for transaction in transactions.keys():
        transactions[transaction][""]


@app.get("/")
async def get_price_assets() -> List[Asset]:
    tickers = ["VWRL.AS", "IWDA.AS", "BTC-EUR"]
    return get_prices(tickers=tickers)
