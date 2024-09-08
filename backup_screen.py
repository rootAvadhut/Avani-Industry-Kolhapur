#backup_screen.py
from imports import tk, ttk, tkFont, DateEntry, pd, datetime, messagebox
from create_treeview import create_treeview_frame
# from search_body_no import search_by_body_no
from db_connection import get_backup_db_collection
import os
from relative_path import get_resource_path
def show_backup_screen(main_frame):
    """
    This function creates and displays the "Home" screen within the provided main_frame.
    """
    # Clear existing widgets from the main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    button_width = 15  # Set standard button width
    custom_font = tkFont.Font(family="Helvetica", size=10)  # Define a custom font

    def validate_integer(P):
        """
        Validates that the input is an integer.
        """
        if P.isdigit() or P == "":
            return True
        return False

    def on_body_no_entry_change(*args):
        """
        Prints the body number when it's changed and valid.
        """
        body_no = body_no_entry.get()
        if body_no.isdigit():
            return True

    # Register the validation command
    vcmd = (main_frame.register(validate_integer), '%P')

    # Body Number Search Section
    tk.Label(main_frame, text="Body Number:", font=custom_font).grid(row=0, column=1, padx=5, pady=5, sticky="e")
    body_no_entry = tk.Entry(main_frame, width=15, font=custom_font, validate="key", validatecommand=vcmd)  # Input field for body number
    body_no_entry.grid(row=0, column=2, padx=5, pady=5)
    body_no_entry.bind("<KeyRelease>", on_body_no_entry_change)
    
    def on_search_by_body_no_click():
        body_no = body_no_entry.get()
        if body_no:
            search_by_body_no(body_no, main_frame)
        else:
            messagebox.showerror("Error", "Please enter a Body Number")

    search_by_body_no_button = tk.Button(main_frame, text="Search By Body No.", width=button_width, font=custom_font, command=on_search_by_body_no_click)
    search_by_body_no_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")

    # Date Range Search Section
    tk.Label(main_frame, text="Start Date:", font=custom_font).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    start_date_entry = DateEntry(main_frame, width=15, font=custom_font, date_pattern='yyyy-mm-dd',
                                 background='darkblue', foreground='white', borderwidth=2, year=datetime.date.today().year)
    start_date_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(main_frame, text="End Date:", font=custom_font).grid(row=1, column=2, padx=5, pady=5, sticky="e")
    end_date_entry = DateEntry(main_frame, width=15, font=custom_font, date_pattern='yyyy-mm-dd',
                               background='darkblue', foreground='white', borderwidth=2, year=datetime.date.today().year)
    end_date_entry.grid(row=1, column=3, padx=5, pady=5)

    def search_date():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        print(start_date)
        # print(end_date)
        

        if not start_date or not end_date:
            messagebox.showerror("Error", "Please select both start and end dates")
            return

        try:
            # Get the MongoDB collection
            collection = get_backup_db_collection()

            # Query the database for records within the date range
            query = {"Insertion Date": {"$gte": start_date, "$lte": end_date}}
            cursor = collection.find(query)

            # Convert cursor to DataFrame
            df = pd.DataFrame(list(cursor))

            if df.empty:
                messagebox.showinfo("Info", "No records found for the selected date range")
                return
        
            # Save the DataFrame to a CSV file
            df.to_csv(get_resource_path('C:/project/temp/backup_date_data.csv'), index=False)

            # Update the treeview with the new data
            create_treeview_frame(main_frame, get_resource_path('C:/project/temp/backup_date_data.csv'))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    search_by_date_button = tk.Button(main_frame, text="Search By Date", width=button_width, font=custom_font, command=search_date)
    search_by_date_button.grid(row=1, column=4, padx=5, pady=5, sticky="e")

    def export_data():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        if not start_date or not end_date:
            messagebox.showerror("Error", "Please select both start and end dates")
            return

        try:
            # Get the MongoDB collection
            collection = get_backup_db_collection()

            # Query the database for records within the date range
            query = {"Insertion Date": {"$gte": start_date, "$lte": end_date}}
            cursor = collection.find(query)

            # Convert cursor to DataFrame
            df = pd.DataFrame(list(cursor))

            if df.empty:
                messagebox.showinfo("Info", "No records found for the selected date range")
                return

            # Filter the DataFrame to include only the specified columns
            columns_to_export = ["Date", "Time", "BODY", "COVER", "12T NB", "12T WB", "26T", "28T", "LPM", "WP1", "BP1", "BP2", "Noise", "Box No"]
            df = df[columns_to_export]

            # Ensure specific columns are strings and handle scientific notation
            string_columns = ['12T NB', '12T WB', '26T', '28T']
            for col in string_columns:
                df[col] = df[col].apply(lambda x: "{:.0E}".format(x).replace("+", "").replace(".0E", "E") if isinstance(x, (int, float)) else str(x))
            
            # Ensure 'Box No' column is an integer
            df['Box No'] = pd.to_numeric(df['Box No'], errors='coerce').fillna(0).astype(int)

            # Ensure the export directory exists
            export_dir = get_resource_path('D:/project/backup-export')
            os.makedirs(export_dir, exist_ok=True)

            # Create the file paths with the current date
            current_date = datetime.date.today().strftime('%Y-%m-%d')
            csv_file_path = os.path.join(export_dir, f'{current_date}.csv')
            excel_file_path = os.path.join(export_dir, f'{current_date}.xlsx')

            # Save the DataFrame to a CSV file
            df.to_csv(csv_file_path, index=False)
            
            # Save the DataFrame to an Excel file
            df.to_excel(excel_file_path, index=False)

            # Show success message
            messagebox.showinfo("Success", f"Files exported successfully to:\n{csv_file_path}\n{excel_file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    export_button = tk.Button(main_frame, text="Export", width=button_width, font=custom_font, command=export_data)
    export_button.grid(row=2, column=4, padx=5, pady=5, sticky="e")

    # Data Table (Treeview)
    file_path = get_resource_path('C:/project/config/backup_default_data.csv')
    treeview_frame = create_treeview_frame(main_frame, file_path)

    # Configure grid layout for resizing
    main_frame.grid_rowconfigure(3, weight=1)
    main_frame.grid_columnconfigure(4, weight=1)


def search_by_body_no(body_no, main_frame):
    # Get the MongoDB collection
    collection = get_backup_db_collection()
    
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
    file_path = get_resource_path('C:/project/temp/one_Search_data.csv')
    df.to_csv(file_path, index=False)

    # Clear existing treeview frame if it exists
    for widget in main_frame.grid_slaves(row=3, column=0):
        widget.destroy()

    # Create the treeview with the new data
    create_treeview_frame(main_frame, file_path)


