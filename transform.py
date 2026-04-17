import pandas as pd
from datetime import datetime

def categorize(price):
    if price > 10000:
        return "very_expensive"
    elif price >= 1000:
        return "expensive"
    return "cheap"

def transform_price(data):

    rows = []
    timestamp = datetime.now()

    for coin, values in data.items():

        price = values.get("usd")

        rows.append({
            "coin": coin.capitalize(),
            "price_usd": price,
            "category": categorize(price),
            "timestamp": timestamp
        })

    return pd.DataFrame(rows)
