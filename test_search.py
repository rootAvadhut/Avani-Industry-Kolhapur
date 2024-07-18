import pandas as pd
import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient

# Define the path to the CSV file
csv_file_path = 'temp/gear_data.csv'

def read_csv(file_path):
    """
    Read data from CSV file and return as pandas DataFrame.
    """
    return pd.read_csv(file_path)

def fetch_all_data():
    """
    Fetch all data from MongoDB and return as pandas DataFrame.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['avani_test']
    collection = db['test']
    
    # Fetch all documents from the collection
    cursor = collection.find({})
    # Convert cursor to DataFrame
    df = pd.DataFrame(list(cursor))
    
    return df

def search_body(df, body_number):
    """
    Perform search based on the entered BODY number.
    """
    return df[df['BODY'] == body_number]

def display_results(search_result):
    """
    Display search results in a table format (Treeview widget).
    """
    # Clear previous search results
    for row in result_tree.get_children():
        result_tree.delete(row)

    # Display search result in the table (Treeview widget)
    for index, row in search_result.iterrows():
        result_tree.insert('', tk.END, values=list(row))

def search_body_number():
    """
    Handler for the Search button click event.
    """
    # Get the BODY number entered by the user
    body_number = body_entry.get()

    if not body_number:
        return

    # Read the CSV file into a pandas DataFrame
    df = read_csv(csv_file_path)

    if body_number == 'all':
        # Fetch all data from MongoDB
        df = fetch_all_data()
    else:
        # Perform search based on the entered BODY number
        df = search_body(df, body_number)

    # Display search result in the table (Treeview widget)
    display_results(df)

def create_gui():
    """
    Create the main GUI window and widgets.
    """
    # Create the main window
    root = tk.Tk()
    root.title("Search BODY Number")

    # Create and place widgets
    tk.Label(root, text="Enter BODY Number (or 'all' for all data):").pack(pady=10)
    global body_entry
    body_entry = tk.Entry(root, width=20)
    body_entry.pack()

    search_button = tk.Button(root, text="Search", command=search_body_number)
    search_button.pack(pady=10)

    # Create a Treeview widget with vertical and horizontal scrollbars
    columns = ['Date', 'Time', 'BODY', 'COVER', '12T NB', '12T WB', '26T', 
               '28T', 'LPM', 'WP1', 'BP1', 'BP2', 'Noise', 'Box No']
    global result_tree
    result_tree = ttk.Treeview(root, columns=columns, show='headings')

    # Configure vertical scrollbar
    vsb = ttk.Scrollbar(root, orient="vertical", command=result_tree.yview)
    vsb.pack(side='right', fill='y')
    result_tree.configure(yscrollcommand=vsb.set)

    # Configure horizontal scrollbar
    hsb = ttk.Scrollbar(root, orient="horizontal", command=result_tree.xview)
    hsb.pack(side='bottom', fill='x')
    result_tree.configure(xscrollcommand=hsb.set)

    # Configure column headings
    for col in columns:
        result_tree.heading(col, text=col)

    # Place the Treeview widget
    result_tree.pack(padx=10, pady=10, expand=tk.YES, fill=tk.BOTH)

    # Run the main loop
    root.mainloop()

# Entry point of the script
if __name__ == "__main__":
    create_gui()
