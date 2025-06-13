# SBP WAR API

This is an API that returns weighted average buying and selling rates of major foreign currencies
against the Pakistani Rupee (provided by State Bank of Pakistan).

## Installation

To install the SBP WAR API, you can clone the repository and install the required packages using pip.
Here are the steps:

```bash
git clone https://github.com/muhammadk1607/sbp-war-api.git
cd sbp-war-api
pip install requests pdfplumber "fastapi[standard]"
```

## Fetching Data

To fetch the latest weighted average rates, you can use the `fetch.py` script. This is a simple
script that retrieves the data from the State Bank of Pakistan's website and saves it in
an sqlite database.

```bash
python fetch.py
```

This script is supposed to run daily, so you can set up a cron job or a scheduled task to run it
automatically. Ideally it should be run at 4:00 PM PKT (UTC+5) every day.

Here is the crontab entry to run the script daily at 4:00 PM PKT:

```cron
0 11 * * * /usr/bin/python3 /sbp-war-api/fetch.py >> /sbp-war-api/fetch.log 2>&1
```

## Running the API

To run the API, you can use the `main.py` script. This script uses FastAPI to create a simple API
that returns the latest weighted average rates in JSON format.

### Dev Mode

```bash
fastapi dev main.py
```

## Documentation

You can access the API documentation at `https://sbp-war-api.muhammadkhan.dev/docs`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
