# #delete_screen.py
# import tkinter.messagebox as messagebox
# from imports import tk, ttk, tkFont, DateEntry

# def show_delete_screen(main_frame):
#     """
#     This function creates and displays the "Delete" screen within the provided main_frame.
#     """
#     # Clear existing widgets in the main frame
#     for widget in main_frame.winfo_children():
#         widget.destroy()

#     button_width = 15  # Consistent button width for aesthetics
#     custom_font = tkFont.Font(family="Helvetica", size=10)  # Define custom font for visual consistency

#     # Body Number Search Section
#     tk.Label(main_frame, text="Body Number:", font=custom_font).grid(row=0, column=2, padx=5, pady=5, sticky="e")
#     body_no_entry = tk.Entry(main_frame, width=15, font=custom_font)  # Input field for body number
#     body_no_entry.grid(row=0, column=3, padx=5, pady=5)
#     search_by_body_no_button = tk.Button(main_frame, text="Search By Body No.", width=button_width, font=custom_font)  # Search by Body Number button
#     search_by_body_no_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")
    
#     # Data Table (Treeview)
#     columns = ("Date", "Time", "BODY", "COVER", "12T NB", "12T WB", "26T", "28T", "LPM", "WP1", "BP1", "BP2", "Noise", "Box No")
#     tree = ttk.Treeview(main_frame, columns=columns, show="headings")  # Create the Treeview widget
#     for col in columns:
#         tree.heading(col, text=col, anchor="center")  # Set column headings
#         tree.column(col, anchor="center", width=60)  # Adjust column widths

#     # Sample Data (Replace with actual data fetching and deletion logic)
#     example_data = [
#         ("06/07/23", "15:12", "2406127", "06042426", "2E24", "2E24", "2D24", "2E24", "66.61", "2.46", "2.37", "3.3", "82", "1")
#     ]
#     for data in example_data:
#         tree.insert("", tk.END, values=data)  # Insert data into the treeview

#     # Place the treeview and add a scrollbar
#     tree.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")  # Place the Treeview in the grid
#     vsb = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)  # Add a vertical scrollbar
#     vsb.grid(row=3, column=5, sticky='ns')  # Position the scrollbar
#     tree.configure(yscrollcommand=vsb.set)  # Link the scrollbar to the Treeview

#     # Configure grid layout for resizing
#     main_frame.grid_rowconfigure(3, weight=1)
#     main_frame.grid_columnconfigure(4, weight=1)
    
#     def on_delete_click():  # Define the on_delete_click function first
#         """
#         Handles the "Delete" button click.Prompts for a password and performs deletion if the password is correct.
#         """
#         import tkinter.simpledialog as simpledialog

#         # Popup to get password
#         password = simpledialog.askstring("Password", "Enter password:", show="*")  

#         if password is None:  # This checks if the user clicked Cancel
#             return  # Exit the function without any further action
#         if password == "avadhut9":  # Replace with the actual password
#             result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete?")
#             if result:
#                 messagebox.showinfo("Success", "Data deleted successfully!")
#                 # Here you would add your actual data deletion logic
#             else:
#                 return  # Do nothing if the user cancels
      
#         else:
#             messagebox.showerror("Error", "Incorrect password!")



#      # Delete Button (functionality implemented)
#     delete_button = tk.Button(main_frame, text="Delete", width=button_width, font=custom_font, command=on_delete_click)  # Create the "Delete" button
#     delete_button.grid(row=2, column=4, padx=5, pady=5, sticky="e")  # Position the button in the grid
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import pandas as pd
from imports import tk, ttk, tkFont, DateEntry

def create_treeview_frame(parent, file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    
    # Select the specified columns
    selected_columns = ["Date", "Time", "BODY", "COVER", "12T NB", "12T WB", "26T", "28T", "LPM", "WP1", "BP1", "BP2", "Noise", "Box No"]
    data = data[selected_columns]

    # Create a frame to hold the Treeview and scrollbars
    frame = ttk.Frame(parent)
    frame.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

    # Create a Treeview widget
    tree = ttk.Treeview(frame, columns=selected_columns, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    # Define the column headings and center the values
    for col in selected_columns:
        tree.heading(col, text=col, anchor=tk.CENTER)
        tree.column(col, width=100, anchor=tk.CENTER)

    # Insert the data into the Treeview
    for index, row in data.iterrows():
        tree.insert("", "end", values=list(row))

    # Create and pack the scrollbars
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    tree.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    hsb.grid(row=1, column=0, sticky='ew')
    tree.configure(xscrollcommand=hsb.set)

    # Configure grid layout for resizing
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    return frame

def show_delete_screen(main_frame):
    """
    This function creates and displays the "Delete" screen within the provided main_frame.
    """
    # Clear existing widgets in the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    button_width = 15  # Consistent button width for aesthetics
    custom_font = tkFont.Font(family="Helvetica", size=10)  # Define custom font for visual consistency

    # Body Number Search Section
    tk.Label(main_frame, text="Body Number:", font=custom_font).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    body_no_entry = tk.Entry(main_frame, width=15, font=custom_font)  # Input field for body number
    body_no_entry.grid(row=0, column=3, padx=5, pady=5)
    search_by_body_no_button = tk.Button(main_frame, text="Search By Body No.", width=button_width, font=custom_font)  # Search by Body Number button
    search_by_body_no_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")
    
    # Data Table (Treeview)
    file_path = r'E:\project_3\16-07-2024\project\temp\gear_data.csv'
    treeview_frame = create_treeview_frame(main_frame, file_path)

    # Configure grid layout for resizing
    main_frame.grid_rowconfigure(3, weight=1)
    main_frame.grid_columnconfigure(4, weight=1)
    
    def on_delete_click():  
        """
        Handles the "Delete" button click. Prompts for a password and performs deletion if the password is correct.
        """
        # Popup to get password
        password = simpledialog.askstring("Password", "Enter password:", show="*")  

        if password is None:  # This checks if the user clicked Cancel
            return  # Exit the function without any further action
        if password == "avadhut9":  # Replace with the actual password
            result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete?")
            if result:
                messagebox.showinfo("Success", "Data deleted successfully!")
                # Here you would add your actual data deletion logic
            else:
                return  # Do nothing if the user cancels
        else:
            messagebox.showerror("Error", "Incorrect password!")

    # Delete Button (functionality implemented)
    delete_button = tk.Button(main_frame, text="Delete", width=button_width, font=custom_font, command=on_delete_click)  # Create the "Delete" button
    delete_button.grid(row=2, column=4, padx=5, pady=5, sticky="e")  # Position the button in the grid
