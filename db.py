import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Path to the uploaded Excel file
file_path = 'import/test_gear.xlsx'
output_file_path = 'temp/gear_data.csv'

# Expected columns based on the new specification
expected_columns = [
    'Date', 'Time', 'BODY', 'COVER', '12T NB', '12T WB', '26T', 
    '28T', 'LPM', 'WP1', 'BP1', 'BP2', 'Noise', 'Box No'
]

# Load the Excel file
data = pd.read_excel(file_path)

# Ensure all expected columns are present, add missing ones with "NA" as string
for column in expected_columns:
    if column not in data.columns:
        data[column] = "NA"

# Reorder the DataFrame to match the expected columns sequence
data = data[expected_columns]

def check_body_dup(data):
    """
    Check for duplicate BODY values in the data and against the MongoDB collection.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['avani_test']
    collection = db['test']

    # Check for duplicates within the new data
    duplicates_in_data = data.duplicated(subset=['BODY'], keep=False)
    duplicated_values_in_data = data[duplicates_in_data][['BODY']]

    # Check for duplicates against existing records in the database
    existing_records = list(collection.find({}, {'_id': 0, 'BODY': 1}))
    existing_df = pd.DataFrame(existing_records)

    # Ensure existing_df has the required columns
    if not existing_df.empty and 'BODY' in existing_df.columns:
        duplicates_in_db = data[data['BODY'].isin(existing_df['BODY'])]
    else:
        duplicates_in_db = pd.DataFrame()  # No duplicates in db if no matching columns

    # Collect all duplicated values for the message box
    duplicate_message = "Duplicate values found:\n"
    has_duplicates = False

    if duplicates_in_data.any():
        has_duplicates = True
        duplicate_message += "- Within the new data:\n"
        for index, row in duplicated_values_in_data.iterrows():
            duplicate_message += f"  BODY: {row['BODY']}\n"

    if not duplicates_in_db.empty:
        has_duplicates = True
        duplicate_message += "- Against existing records in the database:\n"
        for index, row in duplicates_in_db.iterrows():
            duplicate_message += f"  BODY: {row['BODY']}\n"

    if has_duplicates:
        # Initialize Tkinter root
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        messagebox.showerror("Duplicate Entries Found", duplicate_message)
        root.destroy()  # Close the Tkinter root window
        
        return False

    return True

def insert_into_db(data):
    """
    Insert data into MongoDB after checking for duplicates.
    """
    if not check_body_dup(data):
        return

    # Get the current date and time
    current_datetime = datetime.now()

    # Add 'Insertion Date' and 'Insertion Time' columns
    data['Insertion Date'] = current_datetime.date().isoformat()
    data['Insertion Time'] = current_datetime.time().isoformat()

    # Save the DataFrame to a CSV file
    data.to_csv(output_file_path, index=False)

    # Convert DataFrame to a list of dictionaries
    data_dict = data.to_dict(orient='records')

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['avani_test']
    collection = db['test']

    # Insert the data into the collection
    collection.insert_many(data_dict)
    # print(data_dict)

    print(f"Data inserted successfully into MongoDB and saved to {output_file_path}.")

# Run the insert function
insert_into_db(data)
