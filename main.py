import sqlite3
import time
import logging

from config import CONFIG, DB_NAME
from extract import extract_price
from transform import transform_price
from load import load_dim_coin, load_dim_time, load_fact

def run_pipeline(conn, run_id):

    data = extract_price()

    if data is None:
        return

    df = transform_price(data)

    with conn:
        load_dim_coin(df, conn)
        load_dim_time(df, conn)
        load_fact(df, conn)

def main():

    logging.basicConfig(level=logging.INFO)

    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")

    for run_id in range(CONFIG["num_runs"]):

        run_pipeline(conn, run_id)

        time.sleep(CONFIG["sleep_seconds"])

    conn.close()

if __name__ == "__main__":
    main()
