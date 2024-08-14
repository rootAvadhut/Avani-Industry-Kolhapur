#update_box.py
import pandas as pd
from pymongo import MongoClient
from db_connection import get_db_collection

excel_file_path = r"E:\project_3\16-07-2024\project\import\import_box.xlsx"

def load_data():
    # Load the Excel file
    data = pd.read_excel(excel_file_path)
    return data
def update_box_data(data=None):
    if data is None:
        data = load_data()

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
    # # Show a popup message indicating successful import
    # root = tk.Tk()
    # root.withdraw()  # Hide the root window
    # messagebox.showinfo("Success", "Box No import successful")
    # root.destroy()  # Close the Tkinter root window
    print("Box data updated successfully.")

if __name__ == "__main__":
    update_box_data()