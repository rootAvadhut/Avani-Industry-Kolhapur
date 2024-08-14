import pandas as pd
from datetime import datetime
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
        data = load_data()

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

    # # Show a popup message indicating successful import
    # root = tk.Tk()
    # root.withdraw()  # Hide the root window
    # messagebox.showinfo("Success", "New gear data imported successfully")
    # root.destroy()  # Close the Tkinter root window

    print(f"New data inserted successfully into MongoDB and saved to {output_file_path}.")

insert_into_db()
