import time
import json
import os
from datetime import datetime, timedelta
from get_sp500_data import retrieve_sp500_closing_prices
from update_google_sheet import update_google_sheet

def start_scheduler(hour: int = 17, minute: int = 0, csv_file: str = "sp500_data.csv"):
    print(f"S&P 500 Data Tracker Scheduler started. Scheduled for {hour:02d}:{minute:02d} daily.")
    while True:
        now = datetime.now()

        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if now >= target_time:
            target_time += timedelta(days=1)

        wait_seconds = (target_time - now).total_seconds()

        hours = int(wait_seconds // 3600)
        minutes = int((wait_seconds % 3600) // 60)
        print(f"Next run scheduled for {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Waiting {hours}h {minutes}m...")

        # Sleep until the target time
        time.sleep(wait_seconds)

        print(f"Executing scheduled task at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
        try:
            retrieve_sp500_closing_prices(csv_file=csv_file)
            update_google_sheet()
        except Exception as e:
            print(f"Error during scheduled execution: {e}")

if __name__ == "__main__":
    # Load configuration from user_input.json
    config_file = 'user_input.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            user_input = json.load(f)
        schedule_time = user_input.get('schedule_time')
        csv_file = user_input.get('csv_file')
    else:
        schedule_time = '17:00'
        csv_file = 'sp500_data.csv'

    try:
        hour, minute = map(int, schedule_time.split(':'))
    except (ValueError, AttributeError):
        print(f"Invalid schedule_time format: {schedule_time}. Defaulting to 17:00.")
        hour, minute = 17, 0

    start_scheduler(hour=hour, minute=minute, csv_file=csv_file)