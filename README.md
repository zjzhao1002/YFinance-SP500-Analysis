# S&P 500 Daily Data Tracker & Google Sheets Sync

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![yfinance](https://img.shields.io/badge/data-yfinance-green.svg)
![Google Sheets](https://img.shields.io/badge/sync-Google%20Sheets-yellow.svg)
![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub%20Actions-orange.svg)

An automated Python utility that tracks daily closing prices for all S&P 500 companies. It fetches market data and synchronizes the results to a Google Sheet on a daily schedule using GitHub Actions.

## 🚀 Features

- **Automated Ticker Discovery:** Automatically retrieves the current S&P 500 constituent list from Wikipedia.
- **Daily Data Tracking:** Downloads daily closing prices using `yfinance`.
- **Google Sheets Integration:** Seamlessly syncs data to a specified Google Sheet, adding a new column for each day.
- **Automated Execution:** Pre-configured GitHub Actions workflow to run the sync every day at 17:00 UTC.
- **Symbol Mapping:** Automatically handles symbol differences (e.g., converting `BRK.B` to `BRK-B` for Yahoo Finance).

## 🛠️ Architecture

- `main.py`: The entry point that initializes the tracker using environment variables.
- `sp500tracker.py`: The core logic for fetching S&P 500 tickers, downloading prices, and updating Google Sheets.
- `.github/workflows/daily_runner.yml`: GitHub Actions configuration for daily automated runs.

## 📋 Prerequisites

- **Python 3.13+**
- **Google Cloud Account:**
  - A project with the **Google Sheets API** and **Google Drive API** enabled.
  - A **Service Account** with a generated `credentials.json` key file.
  - A Google Sheet shared with the Service Account's email address.

## ⚙️ Setup & Installation

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/zjzhao1002/YFinance-SP500-Analysis.git
   cd YFinance-SP500-Analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```env
   SHEET_ID=your_google_sheet_id
   GCP_CREDENTIALS={"type": "service_account", ...}  # Full JSON string of your credentials.json
   ```

### GitHub Actions Setup (For Daily Automation)
To enable daily updates, please fork this repository and add the following **Secrets** to your forked repository (**Settings > Secrets and variables > Actions**):

1.  `GCP_SERVICE_ACCOUNT_FILE`: The **entire content** of your `credentials.json` file.
2.  `SHEET_ID`: Your Google Sheet ID.

The workflow is set to run daily at 17:00 UTC. 
You can change it in the `.github/workflows/daily_runner.yml` file. 
Optionally, you can also change the `SHEET_NAME` in the workflow file.

## 🚀 Usage

### Local Execution
To run the tracker manually:
```bash
python main.py
```

### Manual Trigger on GitHub
You can also trigger the workflow manually from the **Actions** tab in your GitHub repository.

## 🛡️ Security Note

- **Never** commit `credentials.json` or `.env` to public repositories.
- These files are included in the `.gitignore` to prevent accidental uploads.

## ⚖️ Disclaimer

This tool is for educational and personal tracking purposes only. Financial data provided by Yahoo Finance is subject to their terms of service. Always verify data before making investment decisions.
