import asyncio
import threading
import pandas as pd
from datetime import datetime
import os
from db_connection import get_db_collection
import logging
# logger = logging.getLogger('db_and_update_box')


# Configure logging for db_and_update_box.py
log_file_path = 'app_logs/db_and_update_box.log'
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
# logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')
# logger = logging.getLogger('db_and_update_box')
# logger.setLevel(logging.INFO)

# log_file_path = './app_logs/db_and_update_box.log'
# log_dir=os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# if log_dir:
#     os.makedirs(log_dir, exist_ok=True)

# handler = logging.FileHandler(log_file_path)
# formatter = logging.Formatter('%(asctime)s - %(message)s')
# handler.setFormatter(formatter)

# logger.addHandler(handler)

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
    # Load the Excel file for gear data
    data = pd.read_excel(gear_file_path)

    # Ensure all expected columns are present, add missing ones with "NA" as string
    for column in expected_columns:
        if column not in data.columns:
            data[column] = "NA"

    # Reorder the DataFrame to match the expected columns sequence
    data = data[expected_columns]
    return data

def filter_new_rows(data):
    """
    Filter out rows where the 'BODY' value already exists in MongoDB.
    """
    # Get the MongoDB collection
    collection = get_db_collection()

    # Fetch existing 'BODY' values from the database
    existing_records = list(collection.find({}, {'_id': 0, 'BODY': 1}))
    existing_df = pd.DataFrame(existing_records)

    # If there are no existing records, all rows are new
    if existing_df.empty:
        return data

    # Filter out rows where 'BODY' is already in the database
    new_data = data[~data['BODY'].isin(existing_df['BODY'])]

    return new_data

def insert_into_db(data=None):
    """
    Insert only new data into MongoDB.
    """
    if data is None:
        data = load_gear_data()

    # Filter out rows that already exist in the database
    data = filter_new_rows(data)
    
    # If there are no new rows to insert, exit the function
    if data.empty:
        print("No new data to insert.")
        return

    string_columns = ['12T NB', '12T WB', '26T', '28T']
    for col in string_columns:
        data[col] = data[col].apply(lambda x: "{:.0E}".format(x).replace("+", "") if isinstance(x, (int, float)) else str(x))
    
    # Ensure 'Box No' column is an integer
    data['Box No'] = pd.to_numeric(data['Box No'], errors='coerce').fillna(0).astype(int)

    # Get the current date and time
    current_datetime = datetime.now()

    # Add 'Insertion Date' and 'Insertion Time' columns
    data['Insertion Date'] = current_datetime.date().isoformat()
    data['Insertion Time'] = current_datetime.time().isoformat()

    # Save the DataFrame to a CSV file
    data.to_csv(output_file_path, index=False)

    # Convert DataFrame to a list of dictionaries
    data_dict = data.to_dict(orient='records')

    # Get the MongoDB collection
    collection = get_db_collection()

    # Insert the data into the collection
    collection.insert_many(data_dict)

    print(f"New data inserted successfully into MongoDB and saved to {output_file_path}.")

def load_box_data():
    # Load the Excel file for box data
    data = pd.read_excel(box_file_path)
    return data

def update_box_data(data=None):
    if data is None:
        data = load_box_data()

    # Convert 'Box No' column to numeric, coerce errors to NaN, and fill NaN with 0
    data['Box No'] = pd.to_numeric(data['Box No'], errors='coerce').fillna(0).astype(int)

    # Get the MongoDB collection
    collection = get_db_collection()

    # Iterate over the DataFrame rows and update the MongoDB collection
    for index, row in data.iterrows():
        body = row["BODY"]
        box_no = row["Box No"]  # Box No is already an integer

        # Update all documents in the collection where BODY matches
        collection.update_many(
            {"BODY": body},
            {"$set": {"Box No": box_no}}
        )
    print("Box data updated successfully.")

async def monitor_files(stop_event):
    """
    Monitor the Excel files for changes and process new data if the files change.
    """
    gear_last_modified_time = None
    box_last_modified_time = None

    while not stop_event.is_set():
        try:
            # Check if the gear file has been modified
            current_gear_modified_time = os.path.getmtime(gear_file_path)
            if gear_last_modified_time is None or current_gear_modified_time != gear_last_modified_time:
                logging.info("Detected change in gear data, processing new data...")
                gear_data = load_gear_data()
                insert_into_db(gear_data)
                gear_last_modified_time = current_gear_modified_time
            # else:
            #     print("No change detected in gear data.")

            # Check if the box file has been modified
            current_box_modified_time = os.path.getmtime(box_file_path)
            if box_last_modified_time is None or current_box_modified_time != box_last_modified_time:
                logging.info("Detected change in box data, updating box numbers...")
                box_data = load_box_data()
                update_box_data(box_data)
                box_last_modified_time = current_box_modified_time
            # else:
            #     print("No change detected in box data.")

            await asyncio.sleep(5) 
        
        except Exception as e:
            logging.error(f"Error monitoring files: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    stop_event = threading.Event()
    monitor_files(stop_event)
