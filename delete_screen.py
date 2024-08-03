import pandas as pd
from imports import tk, ttk, tkFont, messagebox, simpledialog
from create_treeview import create_treeview_frame
# from search_body_no import search_by_body_no
from db_connection import get_db_collection,get_backup_db_collection


def backup_and_delete_body_no(body_no):
    """
    Deletes the document with the specified body number from the main collection,
    and then backs it up to a backup collection if the deletion is successful.
    """
    # Get the main MongoDB collection (assumed to default to avani_test and test)
    main_collection = get_db_collection()
    backup_collection=get_backup_db_collection()
    
    # # Manually get the backup collection using a separate connection
    # from pymongo import MongoClient
    # client = MongoClient("mongodb://localhost:27017/")
    # backup_collection = client["avani_backup"]["backup"]
    
    try:
        body_no_int = int(body_no)  # Convert body_no to integer
    except ValueError:
        messagebox.showerror("Error", "Body Number must be a number")
        return

    # Search for the document with the given body number
    query = {"BODY": body_no_int}
    document = main_collection.find_one(query)

    if not document:
        messagebox.showerror("Error", "No data found for the given Body Number")
        return

    try:
        # Delete the document from the main collection
        result = main_collection.delete_one(query)

        if result.deleted_count > 0:
            # Insert the document into the backup collection after successful deletion
            backup_collection.insert_one(document)
            messagebox.showinfo("Success", "Data deleted and backed up successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete the document.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_delete_screen(main_frame):
    """
    This function creates and displays the "Delete" screen within the provided main_frame.
    """
    # Clear existing widgets in the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    button_width = 15  # Consistent button width for aesthetics
    custom_font = tkFont.Font(family="Helvetica", size=10)  # Define custom font for visual consistency

    # Validate function to ensure only numbers are entered
    def validate_number(P):
        if P.isdigit() or P == "":
            return True
        return False

    # Register validate_number with Tkinter
    validate_cmd = main_frame.register(validate_number)

    # Body Number Search Section
    tk.Label(main_frame, text="Body Number:", font=custom_font).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    body_no_entry = tk.Entry(main_frame, width=15, font=custom_font, validate="key", validatecommand=(validate_cmd, '%P'))
    body_no_entry.grid(row=0, column=3, padx=5, pady=5)
    
    def on_search_by_body_no_click():
        body_no = body_no_entry.get()
        if body_no:
            search_by_body_no(body_no, main_frame)
        else:
            messagebox.showerror("Error", "Please enter a Body Number")

    search_by_body_no_button = tk.Button(main_frame, text="Search By Body No.", width=button_width, font=custom_font, command=on_search_by_body_no_click)
    search_by_body_no_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")
    
    # Data Table (Treeview)
    file_path = r'E:\project_3\16-07-2024\project\temp\delete_default_data.csv'
    treeview_frame = create_treeview_frame(main_frame, file_path)

    # Configure grid layout for resizing
    main_frame.grid_rowconfigure(3, weight=1)
    main_frame.grid_columnconfigure(4, weight=1)
    
    def on_delete_click():  
        """
        Handles the "Delete" button click. Prompts for a password and performs deletion if the password is correct.
        """
        body_no = body_no_entry.get()
        if not body_no:
            messagebox.showerror("Error", "Please enter a Body Number")
            return

        # Popup to get password
        password = simpledialog.askstring("Password", "Enter password:", show="*")  

        if password is None:  # This checks if the user clicked Cancel
            return  # Exit the function without any further action
        if password == "avadhut9":  # Replace with the actual password
            result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete?")
            if result:
                backup_and_delete_body_no(body_no)
            else:
                return  # Do nothing if the user cancels
        else:
            messagebox.showerror("Error", "Incorrect password!")

    # Delete Button (functionality implemented)
    delete_button = tk.Button(main_frame, text="Delete", width=button_width, font=custom_font, command=on_delete_click)  # Create the "Delete" button
    delete_button.grid(row=2, column=4, padx=5, pady=5, sticky="e")  # Position the button in the grid layout

def search_by_body_no(body_no, main_frame):
    # Get the MongoDB collection
    collection = get_db_collection()
    
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