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
            # Get all values from the first column and strip whitespace
            tickers = [str(t).strip() for t in worksheet.col_values(1)[1:] if t]
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
            # Also strip any accidental whitespace
            tickers = [str(ticker).replace('.', '-').strip() for ticker in tickers]
            return tickers
        except Exception as e:
            print(f"Error fetching tickers from Wikipedia: {e}")
            return []

    def fetch_sp500_data(self) -> pd.DataFrame:
        if self.check_sheet_name():
            worksheet = self.workbook.worksheet(self.sheet_name)
            records = worksheet.get_all_records()
            self.df = pd.DataFrame(records)
            if not self.df.empty and 'Ticker' in self.df.columns:
                self.df['Ticker'] = self.df['Ticker'].astype(str).str.strip()
        else:
            self.df = pd.DataFrame()

        tickers = self.get_sp500_tickers()
        if not tickers:
            print("No tickers found to download.")
            return self.df

        print(f"Downloading closing prices for {len(tickers)} stocks...")
        # Fetch the most recent closing prices. Using 5d to ensure we get the latest data.
        data = yf.download(tickers, period="5d", interval="1d", progress=False)

        if data is not None and 'Close' in data.columns:
            # Get the last row that is not all NaN
            closing_prices_df = data['Close'].dropna(how='all')
            if closing_prices_df.empty:
                print("Error: All downloaded closing prices are NaN.")
                return self.df
            
            closing_prices = closing_prices_df.iloc[-1]
            # Strip index just in case yfinance returns them with spaces (unlikely but safe)
            closing_prices.index = closing_prices.index.str.strip()
            
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            if self.df.empty:
                self.df = pd.DataFrame({
                    'Ticker': closing_prices.index,
                    current_date: closing_prices.values
                })
            elif 'Ticker' in self.df.columns:
                if current_date not in self.df.columns:
                    print(f"Mapping new data for {current_date}...")
                    self.df[current_date] = self.df['Ticker'].map(closing_prices)
                    
                    # Log if we have a lot of NaNs after mapping
                    nan_count = self.df[current_date].isna().sum()
                    if nan_count > 0:
                        print(f"Warning: {nan_count} tickers could not be matched or have no data.")
                else:
                    print(f"No data update needed. Closing prices for {current_date} are already present.")
            else:
                print("Error: 'Ticker' column missing from existing data.")
            return self.df
        else:
            print("Error: Could not find 'Close' prices in Yahoo Finance data.")
            return self.df
        
    def update_google_sheet(self) -> None:
        if self.df.empty:
            print("No data to update.")
            return
        
        self.df = self.df.fillna('')  # Replace NaN with empty string for Google Sheets compatibility
        
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
