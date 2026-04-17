CONFIG = {
    "coins": ["bitcoin", "ethereum", "solana", "dogecoin", "cardano"],
    "vs_currency": "usd",
    "sleep_seconds": 2,
    "num_runs": 3
}

ENV = "dev"

DB_NAME = "crypto_dev.db" if ENV == "dev" else "crypto_prod.db"
