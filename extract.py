import requests
import time
import logging
from config import CONFIG

def extract_price(retries=3):

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": ",".join(CONFIG["coins"]),
        "vs_currencies": CONFIG["vs_currency"]
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)
            return response.json()

        except Exception as e:
            logging.warning(f"API attempt {attempt+1} failed: {e}")
            time.sleep(1)

    logging.error("API failed after retries")
    return None
