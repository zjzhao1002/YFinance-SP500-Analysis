# S&P 500 Daily Data Tracker & Google Sheets Sync

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![yfinance](https://img.shields.io/badge/data-yfinance-green.svg)
![Google Sheets](https://img.shields.io/badge/sync-Google%20Sheets-yellow.svg)
![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub%20Actions-orange.svg)
![Looker Studio](https://img.shields.io/badge/Visualization-Looker%20Studio-blue.svg)

An automated Python utility designed to track and archive daily closing prices for all S&P 500 constituents. By leveraging `yfinance` for market data and `gspread` for seamless Google Sheets integration, it provides both standardized and transposed datasets optimized for downstream analysis and visualization.

### 📊 Visualization
The system is pre-configured for integration with Looker Studio, enabling automated dashboarding of market trends. 
**[View Live S&P 500 Analysis Dashboard](https://datastudio.google.com/reporting/5ce93221-90e9-45e8-80c5-d82dd081106f)**

## 🚀 Features

- **Automated Ticker Discovery:** Automatically retrieves the current S&P 500 constituent list from Wikipedia.
- **Daily Data Tracking:** Downloads daily closing prices using `yfinance`.
- **Google Sheets Integration:** Seamlessly syncs data to a specified Google Sheet, adding a new column for each day.
- **Transposed Data Sync:** Automatically maintains a separate "Transposed" sheet where dates are rows and tickers are columns, ideal for time-series analysis and charting.
- **Automated Execution:** Pre-configured GitHub Actions workflow to run the sync every day at 22:00 UTC.
- **Symbol Mapping:** Automatically handles symbol differences (e.g., converting `BRK.B` to `BRK-B` for Yahoo Finance compatibility).
- **Visual Analytics:** Seamlessly integrates with Looker Studio for real-time, interactive data visualization and trend analysis.

## 🛠️ Architecture

- `main.py`: The entry point that initializes the tracker using environment variables and executes the sync process.
- `sp500tracker.py`: The core class-based logic for fetching tickers, downloading prices, transposing data, and interacting with the Google Sheets API.
- `.github/workflows/daily_runner.yml`: GitHub Actions configuration for daily automated runs and manual triggers.

## 📋 Prerequisites

- **Python 3.13+**
- **Google Cloud Account:**
  - A project with the **Google Sheets API** and **Google Drive API** enabled.
  - A **Service Account** with a generated `credentials.json` key file.
  - A Google Sheet created and **shared** with the Service Account's email address (with "Editor" permissions).

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
   GCP_CREDENTIALS={"type": "service_account", ...}  # Full JSON content of your credentials.json
   SHEET_NAME=SP500 Closing Prices (Optional, defaults to this value)
   ```

### GitHub Actions Setup (For Daily Automation)
To enable daily updates, add the following **Secrets** to your repository (**Settings > Secrets and variables > Actions**):

1.  `GCP_SERVICE_ACCOUNT_FILE`: The **entire content** of your `credentials.json` file.
2.  `SHEET_ID`: Your Google Sheet ID (found in the URL: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`).

The workflow is scheduled to run daily at 22:00 UTC. You can modify this in `.github/workflows/daily_runner.yml`.

## 🚀 Usage

### Local Execution
To run the tracker manually from your terminal:
```bash
python main.py
```

### Manual Trigger on GitHub
1. Navigate to the **Actions** tab in your GitHub repository.
2. Select the **Daily Google Sheets Update** workflow.
3. Click **Run workflow**.

## 🛡️ Security Note

- **Never** commit `credentials.json` or `.env` to public repositories.
- These files are explicitly ignored by `.gitignore` to prevent accidental disclosure of sensitive credentials.

## ⚖️ Disclaimer

This tool is for educational and personal tracking purposes only. Financial data provided by Yahoo Finance is subject to their terms of service. Always verify data before making investment decisions.
