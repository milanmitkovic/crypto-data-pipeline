import pyodbc
import time
import pandas as pd
from datetime import datetime
print("Izmena")
def load_dim_coin(df, conn):

    for _, row in df.iterrows():


        coin = row["coin"]
        category = row["category"]
        now = datetime.now().isoformat()

        #Checking current value
        current = conn.execute("""
            SELECT coin_id, category
            FROM dim_coin
            WHERE coin_name = ? AND is_current = 1
        """, (coin,)).fetchone()

        #Coin doesn't exist, insert
        if current is None:
            
            conn.execute("""
                INSERT INTO dim_coin(coin_name, category, valid_from, valid_to, is_current)
                VALUES(?, ?, ?, NULL, 1)
                        """,
                            (coin, 
                             category,
                             now
                            )
                        )
            
        #Category changed
        elif current[1] != category:
            
            #Update old record
            conn.execute("""
                UPDATE dim_coin
                SET valid_to = ?, is_current = 0
                WHERE coin_id = ?
            """, (now, current[0]))

            #Inserting new value
            conn.execute("""
                INSERT INTO dim_coin(coin_name, category, valid_from, valid_to, is_current)
                VALUES(?, ?, ?, NULL, 1)
                        """,
                            (coin, 
                             category,
                             now
                            )
                        )


def load_dim_time(df, conn):

    for _, row in df.iterrows():

        ts = row["timestamp"]
        ts_str = ts.isoformat()

        conn.execute("""
            INSERT OR IGNORE INTO dim_time(timestamp, date, hour, day_of_week)
            VALUES(?,?,?,?)
        """,(
            ts_str,
            ts.date().isoformat(),
            ts.hour,
            ts.strftime("%A")
        )
            )

def load_fact(df, conn):

    for _, row in df.iterrows():

        coin_id = conn.execute("""
            SELECT coin_id 
            FROM dim_coin 
            WHERE coin_name = ? AND is_current = 1
        """, (row["coin"],)).fetchone()[0]

        time_id = conn.execute("""
            SELECT time_id 
            FROM dim_time 
            WHERE timestamp = ?
        """, (row["timestamp"].isoformat(),)).fetchone()[0]

        conn.execute("""
            INSERT OR IGNORE INTO fact_crypto_prices(coin_id, time_id, price_usd)
            VALUES(?, ?, ?)
        """,(
            coin_id,
            time_id,
            row["price_usd"]
        ))
