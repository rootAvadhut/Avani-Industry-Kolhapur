import asyncio
import threading
import pandas as pd
from datetime import datetime
import os
from db_connection import get_db_collection

# Paths to the uploaded Excel files
gear_file_path = 'import/import_gear.xlsx'
box_file_path = 'import/import_box.xlsx'
output_file_path = 'temp/gear_data.csv'

# Expected columns based on the new specification
expected_columns = [
    'Date', 'Time', 'BODY', 'COVER', '12T NB', '12T WB', '26T', 
    '28T', 'LPM', 'WP1', 'BP1', 'BP2', 'Noise', 'Box No'
]

def load_gear_data():
    """Loads gear data from the specified Excel file and checks for missing columns."""
    print("Loading gear data from Excel file.")
    data = pd.read_excel(gear_file_path)

    # Ensure all expected columns are present, fill missing ones with "NA"
    for column in expected_columns:
        if column not in data.columns:
            data[column] = "NA"

    data = data[expected_columns]  # Reorder the columns
    return data

def filter_new_rows(data):
    """Filters out rows that already exist in the MongoDB based on 'BODY' field."""
    print("Filtering new rows from the data.")
    collection = get_db_collection()

    # Find all existing records' 'BODY' field
    existing_records = list(collection.find({}, {'_id': 0, 'BODY': 1}))
    existing_df = pd.DataFrame(existing_records)

    if existing_df.empty:
        return data

    # Filter out rows where 'BODY' already exists in the database
    new_data = data[~data['BODY'].isin(existing_df['BODY'])]
    return new_data

def insert_into_db(data=None):
    """Inserts new gear data into MongoDB after filtering for unique entries."""
    if data is None:
        data = load_gear_data()

    data = filter_new_rows(data)

    if data.empty:
        print("No new data to insert.")
        return

    # Handle string formatting for specific columns
    string_columns = ['12T NB', '12T WB', '26T', '28T']
    for col in string_columns:
        data[col] = data[col].apply(lambda x: "{:.0E}".format(x).replace("+", "") if isinstance(x, (int, float)) else str(x))

    # Ensure 'Box No' is an integer
    data['Box No'] = pd.to_numeric(data['Box No'], errors='coerce').fillna(0).astype(int)

    # Add Insertion Date and Time
    current_datetime = datetime.now()
    data['Insertion Date'] = current_datetime.date().isoformat()
    data['Insertion Time'] = current_datetime.time().isoformat()

    # Save to CSV
    data.to_csv(output_file_path, index=False)

    # Insert new rows into MongoDB
    data_dict = data.to_dict(orient='records')
    collection = get_db_collection()
    collection.insert_many(data_dict)

    print(f"New data inserted successfully into MongoDB and saved to {output_file_path}.")

def load_box_data():
    """Loads box data from the specified Excel file."""
    print("Loading box data from Excel file.")
    data = pd.read_excel(box_file_path)
    return data

def update_box_data(data=None):
    """Updates 'Box No' in MongoDB for existing records based on 'BODY'."""
    if data is None:
        data = load_box_data()

    # Convert 'Box No' to an integer
    data['Box No'] = pd.to_numeric(data['Box No'], errors='coerce').fillna(0).astype(int)

    # Update MongoDB records
    collection = get_db_collection()
    for index, row in data.iterrows():
        body = row["BODY"]
        box_no = row["Box No"]
        collection.update_many({"BODY": body}, {"$set": {"Box No": box_no}})

    print("Box data updated successfully.")

async def monitor_files(stop_event):
    """Monitors the gear and box files for changes and triggers appropriate actions."""
    print("Starting to monitor files for changes.")
    gear_last_modified_time = None
    box_last_modified_time = None

    while not stop_event.is_set():
        try:
            # Monitor gear file for changes
            current_gear_modified_time = os.path.getmtime(gear_file_path)
            if gear_last_modified_time is None or current_gear_modified_time != gear_last_modified_time:
                print("Change detected in gear file.")
                insert_into_db()
                gear_last_modified_time = current_gear_modified_time

            # Monitor box file for changes
            current_box_modified_time = os.path.getmtime(box_file_path)
            if box_last_modified_time is None or current_box_modified_time != box_last_modified_time:
                print("Change detected in box file.")
                update_box_data()
                box_last_modified_time = current_box_modified_time

        except FileNotFoundError as e:
            print(f"File not found: {e}")

        # Sleep before checking the files again
        await asyncio.sleep(1)

