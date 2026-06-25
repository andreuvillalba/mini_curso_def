import os
import re
from datetime import datetime, timedelta

from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

import config

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

SYMBOL = "AAPL"

UNIT_MAP = {
    "m": TimeFrameUnit.Minute,
    "h": TimeFrameUnit.Hour,
    "d": TimeFrameUnit.Day,
}


def parse_timeframe(timeframe_str):
    amount, unit = re.match(r"(\d+)([a-zA-Z]+)", timeframe_str).groups()
    return TimeFrame(int(amount), UNIT_MAP[unit.lower()])


def main():
    # El endpoint de datos de mercado de Alpaca es fijo (data.alpaca.markets),
    # distinto del endpoint de trading definido en config.ALPACA_ENDPOINT.
    client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

    request = StockBarsRequest(
        symbol_or_symbols=SYMBOL,
        timeframe=parse_timeframe(config.TIMEFRAME),
        start=datetime.now() - timedelta(days=30),
    )

    bars = client.get_stock_bars(request)
    df = bars.df

    output_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{SYMBOL}_{config.TIMEFRAME}.csv")
    df.to_csv(output_path)
    print(f"Datos guardados en {output_path}")


if __name__ == "__main__":
    main()
