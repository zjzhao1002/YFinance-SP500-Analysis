import pandas as pd 
import yfinance as yf
import os
from datetime import datetime

def get_sp500_tickers(csv_file: str = "sp500_data.csv") -> list:
    if os.path.exists(csv_file):
        print(f"Loading tickers from {csv_file}...")
        try:
            df = pd.read_csv(csv_file)
            if 'Ticker' in df.columns:
                return df['Ticker'].tolist()
            else:
                print(f"Warning: 'Ticker' column not found in {csv_file}. Falling back to Wikipedia.")
        except Exception as e:
            print(f"Error reading {csv_file}: {e}. Falling back to Wikipedia.")

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
    
def retrieve_sp500_closing_prices(csv_file: str = "sp500_data.csv"):
    tickers = get_sp500_tickers(csv_file=csv_file)
    if not tickers:
        print("No tickers found. Exiting.")
        return
    
    print(f"Downloading closing prices for {len(tickers)} stocks...")
    # Fetch the most recent closing prices
    data = yf.download(tickers, period="1d", interval="1d")

    # Extract just the 'Close' prices
    if 'Close' in data.columns:
        closing_prices = data['Close'].iloc[-1]
        
        # Get current date for the column name
        current_date = datetime.now().strftime("%Y-%m-%d")
        column_name = f"{current_date} Close"
        
        # Create a dataframe for the new data
        new_df = pd.DataFrame({
            'Ticker': closing_prices.index,
            column_name: closing_prices.values
        })

        if os.path.exists(csv_file):
            print(f"File {csv_file} exists. Merging new data...")
            existing_df = pd.read_csv(csv_file)
            # Merge on Ticker. Outer join to handle any changes in tickers over time.
            updated_df = pd.merge(existing_df, new_df, on='Ticker', how='outer')
            updated_df.to_csv(csv_file, index=False)
            print(f"Successfully updated {csv_file} with {column_name}")
        else:
            print(f"File {csv_file} does not exist. Creating new file...")
            new_df.to_csv(csv_file, index=False)
            print(f"Successfully created {csv_file} with {column_name}")
    else:
        print("Could not retrieve closing prices.")

if __name__ == "__main__":
    retrieve_sp500_closing_prices()