import tkinter as tk
import pandas as pd
from datetime import datetime
from tkinter import messagebox
from db_connection import get_db_collection

# Path to the uploaded Excel file
file_path = 'import/import_gear.xlsx'
output_file_path = 'temp/gear_data.csv'

# Expected columns based on the new specification
expected_columns = [
    'Date', 'Time', 'BODY', 'COVER', '12T NB', '12T WB', '26T', 
    '28T', 'LPM', 'WP1', 'BP1', 'BP2', 'Noise', 'Box No'
]

def load_data():
    # Load the Excel file
    data = pd.read_excel(file_path)

    # Ensure all expected columns are present, add missing ones with "NA" as string
    for column in expected_columns:
        if column not in data.columns:
            data[column] = "NA"

    # Reorder the DataFrame to match the expected columns sequence
    data = data[expected_columns]
    return data

def check_body_dup(data):
    """
    Check for duplicate BODY values in the data and against the MongoDB collection.
    """
    # Get the MongoDB collection
    collection = get_db_collection()

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

def insert_into_db(data=None):
    """
    Insert data into MongoDB after checking for duplicates.
    """
    if data is None:
        data = load_data()

    if not check_body_dup(data):
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

    # Show a popup message indicating successful import
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Success", "Gear import successful")
    root.destroy()  # Close the Tkinter root window

    print(f"Data inserted successfully into MongoDB and saved to {output_file_path}.")
# insert_into_db()