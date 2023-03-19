from typing import Dict, List, Union

from pandas import DataFrame, to_datetime
from yfinance import Tickers

from schemas import Asset

transactions = {
    "VWRL.AS": [
        {"date": "2023-03-15", "price": 94.93, "amount": 5},
        {"date": "2023-02-01", "price": 97.92, "amount": 5},
        {"date": "2023-01-02", "price": 94.22, "amount": 5},
        {"date": "2022-12-01", "price": 99.90, "amount": 5},
        {"date": "2022-11-04", "price": 96.34, "amount": 6},
        {"date": "2022-10-05", "price": 95.87, "amount": 5},
        {"date": "2022-09-09", "price": 100.88, "amount": 5},
        {"date": "2022-08-04", "price": 103.22, "amount": 5},
        {"date": "2022-07-13", "price": 97.54, "amount": 5},
        {"date": "2022-06-01", "price": 101.00, "amount": 5},
        {"date": "2022-05-12", "price": 96.49, "amount": 5},
        {"date": "2022-04-12", "price": 104.70, "amount": 5},
        {"date": "2022-03-03", "price": 102.80, "amount": 3},
        {"date": "2022-02-01", "price": 105.28, "amount": 3},
        {"date": "2022-01-04", "price": 110.52, "amount": 4},
        {"date": "2021-12-10", "price": 108.84, "amount": 2},
        {"date": "2021-11-02", "price": 106.00, "amount": 2},
        {"date": "2021-10-04", "price": 100.38, "amount": 3},
        {"date": "2021-09-01", "price": 103.96, "amount": 3},
        {"date": "2021-08-06", "price": 101.76, "amount": 1},
        {"date": "2021-07-01", "price": 99.79, "amount": 1},
        {"date": "2021-06-02", "price": 96.68, "amount": 1},
        {"date": "2021-05-03", "price": 96.48, "amount": 1},
    ],
    "IWDA.AS": [
        {"date": "2021-09-08", "amount": 3, "price": 73.53},
        {"date": "2021-11-15", "amount": 1, "price": 77.95},
        {"date": "2021-12-10", "amount": 1, "price": 78.04},
        {"date": "2022-01-04", "amount": 1, "price": 79.80},
    ],
    "BTC-EUR": [
        {"date": "2019-07-17", "amount": 0.01155784, "price": 8480.82, "fee": 2.99},
        {"date": "2021-02-10", "amount": 0.00024730, "price": 36433.48, "fee": 0.99},
        {"date": "2021-02-22", "amount": 0.00020747, "price": 43427.97, "fee": 0.99},
        {"date": "2021-03-10", "amount": 0.00018712, "price": 48150.92, "fee": 0.99},
        {"date": "2021-05-16", "amount": 0.00022478, "price": 40083.64, "fee": 0.99},
        {"date": "2021-06-16", "amount": 0.00033190, "price": 27146.73, "fee": 0.99},
        {"date": "2021-07-16", "amount": 0.00028079, "price": 32088.04, "fee": 0.99},
        {"date": "2021-08-16", "amount": 0.00023069, "price": 39056.74, "fee": 0.99},
        {"date": "2021-11-20", "amount": 0.00017247, "price": 52240.97, "fee": 0.99},
        {"date": "2021-12-20", "amount": 0.00021969, "price": 41012.34, "fee": 0.99},
        {"date": "2022-01-20", "amount": 0.00024113, "price": 37365.74, "fee": 0.99},
        {"date": "2022-02-20", "amount": 0.00026589, "price": 33886.19, "fee": 0.99},
        {"date": "2022-03-20", "amount": 0.00023891, "price": 37712.95, "fee": 0.99},
        {"date": "2022-04-20", "amount": 0.00023278, "price": 38706.07, "fee": 0.99},
    ],
}


def get_prices(tickers: list) -> List[Asset]:
    yf_tickers: Tickers = Tickers(tickers=tickers)
    history: DataFrame = yf_tickers.history(period="90d", progress=False)["Close"]
    history = history.reset_index().rename(columns={"Date": "date"})
    history["date"] = to_datetime(history["date"])
    history["date"] = history["date"].dt.date.astype(str)

    assets: List[dict] = []

    for ticker in tickers:
        trans = transactions[ticker]

        if ticker == "VWRL.AS":
            total_dividend = 24.79 + 27.20 + 31.11 + 7.08 + 5.69
        else:
            total_dividend = 0

        if ticker in ["VWRL.AS", "IWDA.AS"]:
            ticker_type = "ETF"
        else:
            ticker_type = "Crypto" 
        
        assets.append(
            {
                "id": ticker,
                "symbol": ticker,
                "current_price": history[ticker].dropna().iloc[-1],
                "price_change_24h": history[ticker].dropna().iloc[-1] - history[ticker].dropna().iloc[-2],
                "total_dividend": total_dividend,
                "type": ticker_type,
                "transactions": trans,
                "history": history[["date",  ticker]].rename(columns={ticker: "value"}).dropna().to_dict(orient="records")
            }
        )

    return assets
