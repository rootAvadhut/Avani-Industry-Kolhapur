from imports import tk, ttk, tkFont, DateEntry, show_home_screen, show_delete_screen

# Create main window
root = tk.Tk()
root.title("Data Interface")
root.geometry("800x600")  # Set initial window size

# Define custom font for consistent styling
custom_font = tkFont.Font(family="Helvetica", size=10) 

# Create frame for left-side navigation buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Home button (display the home screen)
# Create the "Home" button. When clicked, it calls the show_home_screen function to display the home screen content within the main_frame.
report_button = tk.Button(button_frame, text="HOME", command=lambda: show_home_screen(main_frame), width=10, height=1, font=custom_font)
report_button.pack(pady=10, fill=tk.X)

# Delete button (display the delete screen)
delete_button = tk.Button(button_frame, text="DELETE", command=lambda: show_delete_screen(main_frame), width=10, height=1, font=custom_font)
delete_button.pack(pady=10, fill=tk.X)

# Main content area (where the screens will be displayed)
main_frame = tk.Frame(root)
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Start by displaying the home screen
show_home_screen(main_frame) 

# Start the Tkinter event loop
root.mainloop() 
