#create_treeview.py
from imports import tk, ttk, tkFont,messagebox,simpledialog, pd

def create_treeview_frame(parent, file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    
    # Select the specified columns
    selected_columns = ["Date", "Time", "BODY", "COVER", "12T NB", "12T WB", "26T", "28T", "LPM", "WP1", "BP1", "BP2", "Noise", "Box No"]
    data = data[selected_columns]
        # Ensure specific columns are strings and handle scientific notation
    string_columns = ['12T NB', '12T WB', '26T', '28T']
    for col in string_columns:
        data[col] = data[col].apply(lambda x: "{:.0E}".format(x).replace("+", "") if isinstance(x, (int, float)) else str(x))
    # Ensure 'Box No' column is an integer
    data['Box No'] = pd.to_numeric(data['Box No'], errors='coerce').fillna(0).astype(int)


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
