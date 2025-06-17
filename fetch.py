import datetime
import sys
from io import BytesIO

import pdfplumber
import requests

from db import create_db, save_rates_to_db


def update_exchange_rate(date: datetime.date = datetime.date.today()) -> None:
    currencies = ["AED", "AUD", "CAD", "CHF", "CNY", "EUR", "GBP", "JPY", "SAR", "USD"]

    date_str = date.isoformat()
    url = f"https://www.sbp.org.pk/ecodata/rates/war/{date.strftime('%Y/%b/%d-%b-%y')}.pdf"

    try:
        response = requests.get(url)
        if response.status_code == 404:
            print(f"{date_str} PDF file couldn't be found")
            return
        response.raise_for_status()

        rates = {}

        # Use pdfplumber to extract text from the PDF
        with pdfplumber.open(BytesIO(response.content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                lines = text.split("\n")
                for line in lines:
                    for currency in currencies:
                        if currency in line:
                            parts = line.split()
                            try:
                                idx = parts.index(currency)
                                rate_str = parts[idx + 1]  # typically Buying Rate
                                rate = round(float(rate_str), 2)
                                rates[currency] = rate
                                print(f"{currency}_TO_PKR: {rate}")
                            except (IndexError, ValueError):
                                print(f"Failed to extract rate from: {line}")
                            break

        if rates:
            save_rates_to_db(date_str, rates)
            print("Exchange rates saved to the database")
        else:
            print("No exchange rates found in the PDF")
    except requests.exceptions.RequestException as e:
        print("Script update_exchange_rate failed in execution")
        print(e)


if __name__ == "__main__":
    now = datetime.datetime.now()
    print(f"update_exchange_rate has been run at {now}")

    create_db()  # Ensure the database is created before saving rates

    # Read the date from the command line argument or use today's date
    date = datetime.date.today()
    if len(sys.argv) > 1:
        try:
            date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Using today's date instead.")

    # Run the task
    update_exchange_rate(date)
