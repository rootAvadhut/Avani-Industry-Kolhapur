from imports import tk, ttk, tkFont, DateEntry,pd,datetime,messagebox
from create_treeview import create_treeview_frame
from search_body_no import search_by_body_no

def show_home_screen(main_frame):
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

    search_by_body_no_button = tk.Button(main_frame, text="Search By Body No.", width=button_width, font=custom_font,command=on_search_by_body_no_click)
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
    file_path = r'E:\project_3\16-07-2024\project\temp\home_default_data.csv'
    treeview_frame = create_treeview_frame(main_frame, file_path)

    # Configure grid layout for resizing
    main_frame.grid_rowconfigure(3, weight=1)
    main_frame.grid_columnconfigure(4, weight=1)

