from imports import tk, ttk, tkFont, DateEntry


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
    search_by_body_no_button = tk.Button(main_frame, text="Search By Body No.", width=button_width, font=custom_font) #Search by Body Number
    search_by_body_no_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")

    # Delete Button (functionality not yet implemented)
    delete_button = tk.Button(main_frame, text="Delete", width=button_width, font=custom_font)
    delete_button.grid(row=2, column=4, padx=5, pady=5, sticky="e")

    # Data Table (Treeview)
    columns = ("Date", "Time", "BODY", "COVER", "12T NB", "12T WB", "26T", "28T", "LPM", "WP1", "BP1", "BP2", "Noise", "Box No")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col, anchor="center")  # Set column headings
        tree.column(col, anchor="center", width=60)   # Adjust column widths

    # Sample Data (Replace with actual data fetching and deletion logic)
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
