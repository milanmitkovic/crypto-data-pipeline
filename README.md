# crypto-data-pipeline
This project is a Python-based data engineering pipeline that extracts cryptocurrency prices from an external API, transforms the data, and loads it into a structured data warehouse using SQLite.
Crypto Data Pipeline
Overview

This project is a Python-based data engineering pipeline that extracts cryptocurrency prices from an external API, transforms the data, and loads it into a structured data warehouse using SQLite.

Architecture

API → Extract → Transform → Load → SQLite Data Warehouse → Analytics

Features
API data ingestion (CoinGecko)
Data validation and error handling
Retry logic for API failures
Slowly Changing Dimension (SCD Type 2) for historical tracking
Fact and dimension data modeling
Incremental and idempotent pipeline design
Logging and pipeline run tracking
Data Model
dim_coin (SCD Type 2)
dim_time
fact_crypto_prices
pipeline_runs
Technologies Used
Python
Pandas
SQLite
REST API
SQL
How to Run
python main.py
Example Analytics
Moving average of prices
Price trends over time
Volatility analysis
Future Improvements
Airflow orchestration
Cloud deployment (AWS/GCP)
Real-time streaming pipeline
