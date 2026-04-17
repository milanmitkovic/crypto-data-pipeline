import pandas as pd
import sqlite3
import logging

logging.basicConfig(
    filename = "pipeline.log",
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)
#--------------------------------------------------------------------------------------

def analyze(conn):
    
    
    logging.info("Aggregation results:")
    query = """
        SELECT 
            c.coin_name,
            t.day_of_week,
            AVG(f.price_usd) AS avg_price
        FROM fact_crypto_prices f
        JOIN dim_coin c
            ON f.coin_id = c.coin_id
        JOIN dim_time t
            ON f.time_id = t.time_id
        GROUP BY c.coin_name, t.day_of_week
        ORDER BY avg_price DESC
            """
    try:
        result = pd.read_sql(query, conn)
        logging.info(result)
    
    except Exception as e:
        logging.error(f"Failed analyzing data: {e}")

#--------------------------------------------------------------------------------------
def analyze_pipeline_runs(conn):

    query = """
        SELECT
            status,
            COUNT(*) AS runs
        FROM pipeline_runs
        GROUP BY status
    """

    result = pd.read_sql(query, conn)

    logging.info("Pipeline run summary:")
    logging.info(result)
    
#--------------------------------------------------------------------------------------
def validate_data(df):

    if df is None:
        logging.error("Validation failed: dataframe is None")
        return False

    if df.empty:
        logging.error("Validation failed: dataframe is empty")
        return False

    if (df["price_usd"] <= 0).any():
        logging.error("Validation failed: negative or zero price detected")
        return False

    if df["coin"].isnull().any():
        logging.error("Validation failed: missing coin name")
        return False
        
    if len(df) != 5:
        logging.error("Validation failed: incorrect number of coins")
        return False     
    
    return True
        
