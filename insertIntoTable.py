import pandas as pd
import tkinter as tk
from tkinter import ttk

def create_treeview_frame(parent, file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    
    # Select the specified columns
    selected_columns = ["Date", "Time", "BODY", "COVER", "12T NB", "12T WB", "26T", "28T", "LPM", "WP1", "BP1", "BP2", "Noise", "Box No"]
    data = data[selected_columns]

    # Create a frame to hold the Treeview and scrollbars
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a Treeview widget
    tree = ttk.Treeview(frame)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Define the columns
    tree["columns"] = selected_columns
    tree["show"] = "headings"

    # Define the column headings and center the values
    for col in selected_columns:
        tree.heading(col, text=col, anchor=tk.CENTER)
        tree.column(col, width=100, anchor=tk.CENTER)

    # Insert the data into the Treeview
    for index, row in data.iterrows():
        tree.insert("", "end", values=list(row))

    # Create and pack the scrollbars
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    hsb.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=hsb.set)

    return frame

# Main function to create the window and display the Treeview
def main():
    # File path to the CSV file
    file_path = r'E:\project_3\16-07-2024\project\temp\gear_data.csv'

    # Create the main window
    root = tk.Tk()
    root.title("Gear Data")

    # Create and pack the Treeview frame
    create_treeview_frame(root, file_path)

    # Start the Tkinter event loop
    root.mainloop()

# Call the main function
if __name__ == "__main__":
    main()
