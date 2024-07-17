#home_screen.py
from imports import tk, ttk, tkFont, DateEntry
import datetime

def show_home_screen(main_frame):
    """
    This function creates and displays the "Home" screen within the provided main_frame.
    """
    # Clear existing widgets from the main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    button_width = 15  # Set standard button width
    custom_font = tkFont.Font(family="Helvetica", size=10)  # Define a custom font


    # Body Number Search Section
    tk.Label(main_frame, text="Body Number:", font=custom_font).grid(row=0, column=1, padx=5, pady=5, sticky="e")
    body_no_entry = tk.Entry(main_frame, width=15, font=custom_font)  # Input field for body number
    body_no_entry.grid(row=0, column=2, padx=5, pady=5)
    search_by_body_no_button = tk.Button(main_frame, text="Search By Body No.", width=button_width, font=custom_font)
    search_by_body_no_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")

    # Date Range Search Section
    tk.Label(main_frame, text="Start Date:", font=custom_font).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    start_date_entry = DateEntry(main_frame, width=15, font=custom_font, date_pattern='dd/mm/yy',
                                background='darkblue', foreground='white', borderwidth=2, year=datetime.date.today().year)
    start_date_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(main_frame, text="End Date:", font=custom_font).grid(row=1, column=2, padx=5, pady=5, sticky="e")
    end_date_entry = DateEntry(main_frame, width=15, font=custom_font, date_pattern='dd/mm/yy',
                              background='darkblue', foreground='white', borderwidth=2, year=datetime.date.today().year)
    end_date_entry.grid(row=1, column=3, padx=5, pady=5)
    search_by_date_button = tk.Button(main_frame, text="Search By Date", width=button_width, font=custom_font)
    search_by_date_button.grid(row=1, column=4, padx=5, pady=5, sticky="e")

    # Export Button (functionality not yet implemented)
    export_button = tk.Button(main_frame, text="Export", width=button_width, font=custom_font)
    export_button.grid(row=2, column=4, padx=5, pady=5, sticky="e")

    # Data Table (Treeview)
    columns = ("Date", "Time", "BODY", "COVER", "12T NB", "12T WB", "26T", "28T", "LPM", "WP1", "BP1", "BP2", "Noise", "Box No")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col, anchor="center")  # Set column headings
        tree.column(col, anchor="center", width=60)   # Adjust column widths

    # Sample Data (Replace with actual data fetching logic)
    example_data = [
        ("06/07/23", "15:12", "2406127", "06042426", "2E24", "2E24", "2D24", "2E24", "66.61", "2.46", "2.37", "3.3", "82", "1")
    ]
    for data in example_data:
        tree.insert("", tk.END, values=data)  # Insert data into the treeview

    # Place the treeview and add a scrollbar
    tree.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")
    vsb = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    vsb.grid(row=3, column=5, sticky='ns')
    tree.configure(yscrollcommand=vsb.set)

    # Configure grid layout for resizing
    main_frame.grid_rowconfigure(3, weight=1)
    main_frame.grid_columnconfigure(4, weight=1)
