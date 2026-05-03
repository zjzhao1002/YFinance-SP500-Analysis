from sp500tracker import SP500Tracker
import json
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    # Load configuration from user_input.json
    sheet_id = os.getenv("SHEET_ID")
    credentials_dict = os.getenv("GCP_CREDENTIALS")

    if not sheet_id or not credentials_dict:
        print("Error: Missing SHEET_ID or GCP_CREDENTIALS in environment variables.")
        exit(1)

    credentials_dict = json.loads(credentials_dict)
    sheet_name = os.getenv("SHEET_NAME", "SP500 Closing Prices")

    tracker = SP500Tracker(sheet_id=sheet_id, credentials_dict=credentials_dict, sheet_name=sheet_name)
    df = tracker.fetch_sp500_data()
    tracker.update_google_sheet()