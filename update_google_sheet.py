import gspread
import pandas as pd
import json
import os

def update_google_sheet(input_file: str = 'user_input.json'):
    # Load user input
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return
    
    try:
        with open(input_file, 'r') as f:
            user_input = json.load(f)
        sheet_id = user_input.get('sheet_id')
        csv_file = user_input.get('csv_file')
        credentials_file = user_input.get('credentials_file')
        sheet_name = user_input.get('sheet_name')
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return

    if not csv_file or not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        return
    
    # Load CSV data
    try:
        df = pd.read_csv(csv_file)
        df = df.fillna('')
        data = [df.columns.values.tolist()] + df.values.tolist()
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        return

    # Load credentials
    try:
        gc = gspread.service_account(filename=credentials_file)
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return

    # Try to find the sheet named 'SP500'
    try:
        workbook = gc.open_by_key(sheet_id)
        print(f"Opened existing sheet by ID: {sheet_id}")
    except Exception as e:
        print(f"Could not open sheet by ID {sheet_id}: {e}")
        sheet = None

    worksheet_list = map(lambda x: x.title, workbook.worksheets())
    sheet = None

    if sheet_name in worksheet_list:
        sheet = workbook.worksheet(sheet_name)
        print(f"Found existing sheet: {sheet_name}")
    else:
        try:
            sheet = workbook.add_worksheet(title=sheet_name, rows=len(data), cols="2")
            print(f"Created new sheet: {sheet_name}")
        except Exception as e:
            print(f"Error creating new sheet: {e}")
            return

    # Update the SP500 sheet with the data from the CSV file
    try:
        worksheet = workbook.worksheet(sheet_name)
        worksheet.clear()
        worksheet.update('A1', data)
        print(f"Successfully updated the sheet '{sheet.title}' with data from {csv_file}.")
    except Exception as e:
        print(f"Error updating worksheet: {e}")

if __name__ == "__main__":
    update_google_sheet()
