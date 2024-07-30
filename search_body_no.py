from pymongo import MongoClient
from imports import messagebox, pd
from create_treeview import create_treeview_frame



def search_by_body_no(body_no, main_frame):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['avani_test']
    collection = db['test']
    
    try:
        body_no_int = int(body_no)  # Convert body_no to integer
    except ValueError:
        messagebox.showerror("Error", "Body Number must be a number")
        return

    # Search for the body number
    query = {"BODY": body_no_int}
    results = list(collection.find(query))

    if not results:
        messagebox.showerror("Error", "No data found for the given Body Number")
        return

    # Save the results to a CSV file
    df = pd.DataFrame(results)
    file_path = r'E:\project_3\16-07-2024\project\temp\one_Search_data.csv'
    df.to_csv(file_path, index=False)

    # Clear existing treeview frame if it exists
    for widget in main_frame.grid_slaves(row=3, column=0):
        widget.destroy()

    # Create the treeview with the new data
    create_treeview_frame(main_frame, file_path)
