# S&P 500 Daily Data Tracker & Google Sheets Sync - Project Context

## Project Overview
This project is an automated Python utility designed to track the daily closing prices of all S&P 500 constituent stocks and synchronize this data with a Google Sheet. It uses `yfinance` to fetch market data and `gspread` to interact with the Google Sheets API.

### Main Technologies
- **Language:** Python 3.13+
- **Data Processing:** `pandas`, `numpy`
- **Financial Data:** `yfinance`
- **Google Sheets Integration:** `gspread`, `google-auth`
- **Ticker Discovery:** `beautifulsoup4`, `lxml` (via `pandas.read_html` from Wikipedia)
- **Environment Management:** `python-dotenv`

### Core Architecture
- `main.py`: The main entry point that loads configuration from environment variables and triggers the tracker.
- `sp500tracker.py`: Contains the `SP500Tracker` class which handles:
    - Retrieving the current S&P 500 ticker list from Wikipedia (if not already in the sheet).
    - Downloading the latest closing prices for all tickers.
    - Merging new data with existing historical data.
    - Updating the specified Google Sheet by adding a new column for the current day.
    - Providing a transposed version of the data (dates as rows) and updating a separate transposed Google Sheet.
- `.github/workflows/daily_runner.yml`: GitHub Actions workflow that runs the tracker daily at 22:00 UTC.

---

## Building and Running

### Prerequisites
- Python 3.13 or higher.
- A Google Cloud Project with Google Sheets and Drive APIs enabled.
- A Service Account key (`credentials.json`) for local development.
- A Google Sheet shared with the Service Account email.

### Local Configuration
The application uses environment variables for configuration. Create a `.env` file in the root directory:
```env
SHEET_ID=your_google_sheet_id
GCP_CREDENTIALS={"type": "service_account", ...}  # Full JSON content of credentials.json
SHEET_NAME=SP500 Closing Prices (Optional)
```

### Commands
- **Install Dependencies:**
  ```bash
  pip install .
  ```
- **Run the Tracker:**
  ```bash
  python main.py
  ```

---

## Development Conventions

### Code Style
- **Type Hinting:** The project uses Python type hints for better code clarity and IDE support.
- **Error Handling:** Basic try-except blocks are used around network and API calls (Yahoo Finance, Google Sheets).
- **Class-Based Design:** Core logic is encapsulated within the `SP500Tracker` class in `sp500tracker.py`.

### Data Management
- The tracker fetches S&P 500 tickers from Wikipedia if they aren't already present in the Google Sheet.
- It maps Wikipedia symbols (like `BRK.B`) to Yahoo Finance compatible symbols (like `BRK-B`).
- Data is updated by adding a new column to the Google Sheet for each day's closing prices.

### Testing
- No automated test suite (e.g., `pytest`, `unittest`) was identified in the project root. Testing is currently performed by running `main.py`.

### Security
- **Sensitive Files:** `credentials.json` and `.env` should be handled with care and excluded from version control.
- **Ignore Patterns:** A virtual environment is typically maintained in `bin/`, `lib/`, etc., which are ignored by search tools.
