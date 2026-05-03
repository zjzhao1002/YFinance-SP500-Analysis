import yfinance as yf
import pandas as pd 
import gspread
from datetime import datetime

class SP500Tracker:
    def __init__(self, sheet_id: str, credentials_dict: dict, sheet_name: str="SP500 Closing Prices"):
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        self.credentials_dict = credentials_dict
        try:
            self.gc = gspread.service_account_from_dict(self.credentials_dict)
            self.workbook = self.gc.open_by_key(self.sheet_id)
        except Exception as e:
            print(f"Error initializing Google Sheets connection: {e}")

    def check_sheet_name(self) -> bool:
        worksheet_list = map(lambda x: x.title, self.workbook.worksheets())
        if self.sheet_name in worksheet_list: # type: ignore
            return True
        return False

    def get_sp500_tickers(self) -> list:
        if self.check_sheet_name():
            worksheet = self.workbook.worksheet(self.sheet_name) 
            tickers = worksheet.col_values(1)[1:]  # Skip header
            return tickers

        print("Sheet not found. Fetching tickers from Wikipedia...")
        # Fetch S&P 500 tickers from Wikipedia
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        storage_options = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"}
        try:
            tables = pd.read_html(url, storage_options=storage_options)
            df = tables[0]
            tickers = df['Symbol'].tolist()
            # Yahoo Finance uses '-' instead of '.' in symbols (e.g., BRK.B -> BRK-B)
            tickers = [ticker.replace('.', '-') for ticker in tickers]
            return tickers
        except Exception as e:
            print(f"Error fetching tickers: {e}")
            return []

    def fetch_sp500_data(self) -> pd.DataFrame:
        if self.check_sheet_name():
            worksheet = self.workbook.worksheet(self.sheet_name)
            self.df = pd.DataFrame(worksheet.get_all_records())
        else:
            self.df = pd.DataFrame()

        tickers = self.get_sp500_tickers()

        print(f"Downloading closing prices for {len(tickers)} stocks...")
        # Fetch the most recent closing prices
        data = yf.download(tickers, period="1d", interval="1d")

        if data is not None and 'Close' in data.columns:
            closing_prices = data['Close'].iloc[-1]
            current_date = datetime.now().strftime("%Y-%m-%d")
            if self.df.empty:
                self.df = pd.DataFrame({
                    'Ticker': closing_prices.index,
                    current_date: closing_prices.values
                })
            elif current_date not in self.df.columns:
                self.df[current_date] = self.df['Ticker'].map(closing_prices)
            else:
                print("No data update needed. Closing prices for today are already present.")
            return self.df
        else:
            print("Error fetching new data from Yahoo Finance.")
            return self.df
        
    def update_google_sheet(self) -> None:
        if self.df.empty:
            print("No data to update.")
            return
        
        current_date = datetime.now().strftime("%Y-%m-%d")

        try:
            if self.check_sheet_name():
                sheet = self.workbook.worksheet(self.sheet_name)
                # Compare data: check if today's date is already in the sheet headers
                existing_headers = sheet.row_values(1)
                
                if current_date in existing_headers:
                    print(f"Data for {current_date} already exists in the sheet. No update needed.")
                    return

                print(f"Today's data ({current_date}) not found in sheet. Adding new column...")
                
                if current_date not in self.df.columns:
                    print(f"Error: Today's data ({current_date}) is not in the local DataFrame.")
                    return

                # Calculate new column index (1-based)
                new_col_idx = len(existing_headers) + 1
                
                # Ensure the sheet has enough columns
                if new_col_idx > sheet.col_count:
                    sheet.add_cols(1)

                # Prepare the column data: header followed by values
                # We assume self.df rows match the sheet rows because self.df was loaded from it.
                column_values = [[current_date]] + [[val] for val in self.df[current_date]]
                
                # Update the specific column
                from gspread.utils import rowcol_to_a1
                start_cell = rowcol_to_a1(1, new_col_idx)
                end_cell = rowcol_to_a1(len(column_values), new_col_idx)
                range_name = f"{start_cell}:{end_cell}"
                
                sheet.update(range_name, column_values) # type: ignore
                print(f"Successfully added column for {current_date} to {self.sheet_name}.")
            else:
                # Sheet doesn't exist, create it and upload everything
                data = [self.df.columns.values.tolist()] + self.df.values.tolist()
                sheet = self.workbook.add_worksheet(title=self.sheet_name, rows=len(data), cols=len(data[0]))
                sheet.update('A1', data) # type: ignore
                print(f"Created and updated new sheet: {self.sheet_name}")
        except Exception as e:
            print(f"Error updating Google Sheet: {e}")
