from datetime import date
from typing import Annotated, Dict

from fastapi import FastAPI, Path

from db import ExchangeRate, fetch_rates_from_db

app = FastAPI()


def fetch(date: str) -> ExchangeRate | str:
    rates = fetch_rates_from_db(date)

    if rates is None:
        return f"No exchange rates found for date: {date}"

    return rates


@app.get("/")
def fetch_for_today() -> ExchangeRate | str:
    """Fetch exchange rates for today."""
    today = date.today().isoformat()
    return fetch(today)


@app.get("/{date}")
def fetch_for_date(
    date: Annotated[
        date,
        Path(
            description="Date in ISO format (YYYY-MM-DD) to fetch exchange rates for.",
        ),
    ],
) -> ExchangeRate | str:
    """Fetch exchange rates for a specific date."""
    date_str = date.isoformat()
    return fetch(date_str)
