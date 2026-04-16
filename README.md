# S&P 500 Daily Data Tracker & Google Sheets Sync

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![yfinance](https://img.shields.io/badge/data-yfinance-green.svg)
![Google Sheets](https://img.shields.io/badge/sync-Google%20Sheets-yellow.svg)

An automated Python utility that tracks daily closing prices for all S&P 500 companies. It fetches real-time market data, maintains a historical CSV record, and synchronizes the results to a Google Sheet on a daily schedule.

## 🚀 Features

- **Automated Ticker Discovery:** Automatically retrieves the current S&P 500 constituent list from Wikipedia.
- **Historical Data Tracking:** Downloads daily closing prices using `yfinance` and appends them to a local `sp500_data.csv`.
- **Google Sheets Integration:** Seamlessly syncs your local data to a specified Google Sheet for easy access and visualization.
- **Daily Scheduler:** Built-in scheduler to run the data collection and sync process at a specific time every day.
- **Robust Merging:** Uses outer joins to handle additions and removals from the S&P 500 index over time.

## 🛠️ Architecture

- `main.py`: The control center that manages the daily scheduling logic.
- `get_sp500_data.py`: Handles fetching tickers and downloading market data.
- `update_google_sheet.py`: Manages authentication and data upload to Google Sheets.
- `user_input.json`: Centralized configuration for IDs, paths, and schedules.

## 📋 Prerequisites

- **Python 3.13+**
- **Google Cloud Account:**
  - A project with the **Google Sheets API** and **Google Drive API** enabled.
  - A **Service Account** with a generated `credentials.json` key file. An example is (taken from [gspread documentation](https://docs.gspread.org/en/latest/oauth2.html))
  ```json
  {
    "type": "service_account",
    "project_id": "api-project-XXX",
    "private_key_id": "2cd … ba4",
    "private_key": "-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n",
    "client_email": "473000000000-yoursisdifferent@developer.gserviceaccount.com",
    "client_id": "473 … hd.apps.googleusercontent.com",
    ...
  }
  ```
  - A Google Sheet shared with the Service Account's email address.

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/yahoo-finance-sp500.git
   cd yahoo-finance-sp500
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment:**
   - Place your Google Service Account key as `credentials.json` in the root directory.
   - Update `user_input.json` with your specific configuration:
     ```json
     {
         "sheet_id": "YOUR_GOOGLE_SHEET_ID",
         "csv_file": "sp500_data.csv",
         "credentials_file": "credentials.json",
         "sheet_name": "SP500",
         "schedule_time": "17:00"
     }
     ```

## 🚀 Usage

To start the automated daily tracker:

```bash
python main.py
```

The script will calculate the time remaining until the next scheduled run and wait. When triggered, it will:
1. Fetch the latest S&P 500 tickers.
2. Download closing prices for the day.
3. Update `sp500_data.csv`.
4. Sync the entire CSV content to your Google Sheet.

To run a one-off update of the data and Google Sheet:
- Run `get_sp500_data.py` to fetch data.
- Run `update_google_sheet.py` to sync to Google Sheets.

## 📊 Data Structure

The generated `sp500_data.csv` uses the following format:

| Ticker | YYYY-MM-DD Close | YYYY-MM-DD Close | ... |
| :--- | :--- | :--- | :--- |
| AAPL | 150.25 | 152.10 | ... |
| MSFT | 280.10 | 282.45 | ... |

## 🛡️ Security Note

- **Never** commit `credentials.json` or `user_input.json` (if it contains your sheet ID) to public repositories. 
- Ensure these files are listed in your `.gitignore`.

## ⚖️ Disclaimer

This tool is for educational and personal tracking purposes only. Financial data provided by Yahoo Finance is subject to their terms of service. Always verify data before making investment decisions.
