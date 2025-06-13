import json
import os
import sqlite3
from typing import Dict, Optional

from pydantic import BaseModel

DB_PATH = os.getenv("DB_PATH", "exchange_rates.db")


class ExchangeRate(BaseModel):
    date: str
    rates: Dict[str, float]

    model_config = {
        "json_schema_extra": {
            "example": {
                "date": "2023-10-01",
                "rates": {
                    "USD": 280.50,
                    "EUR": 300.75,
                    "GBP": 350.00,
                    "JPY": 2.50,
                    "CNY": 40.00,
                    "AUD": 200.00,
                    "CAD": 210.00,
                    "CHF": 320.00,
                    "AED": 75.00,
                    "SAR": 75.50,
                },
            }
        }
    }


def create_db():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS exchange_rates (
                date TEXT PRIMARY KEY,
                rates_json TEXT
            )
        """
        )


def save_rates_to_db(date: str, rates: Dict[str, float]) -> None:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        json_data = json.dumps(rates)
        cursor.execute(
            """
            INSERT OR REPLACE INTO exchange_rates (date, rates_json)
            VALUES (?, ?)
        """,
            (date, json_data),
        )


def fetch_rates_from_db(date: str) -> Optional[ExchangeRate]:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT date, rates_json FROM exchange_rates WHERE date = ?
        """,
            (date,),
        )
        row = cursor.fetchone()

        if row:
            return {"date": row[0], "rates": json.loads(row[1])}
        return None
