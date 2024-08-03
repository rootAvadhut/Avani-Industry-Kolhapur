import tkinter as tk
from db import insert_into_db
from update_box import update_box_data

def show_import_screen(parent_frame):
    # Clear any existing widgets in the frame
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Create and pack the "GEAR IMPORT" button
    gear_import_button = tk.Button(parent_frame, text="GEAR IMPORT", width=20, height=2, command=insert_into_db)
    gear_import_button.pack(pady=10)

    # Create and pack the "BOX IMPORT" button
    box_import_button = tk.Button(parent_frame, text="BOX IMPORT", width=20, height=2,command=update_box_data)
    box_import_button.pack(pady=10)
