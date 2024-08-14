import threading  # Import threading to run background tasks
import os  # Import os to interact with the operating system
import tkinter as tk  # Import tkinter for GUI
import tkinter.font as tkFont  # Import tkinter font for custom fonts in GUI
from tkinter import messagebox  # Import messagebox to show error dialogs
from imports import show_home_screen, show_delete_screen, show_backup_screen  # Import custom functions for different screens

# Function to run the background script
def run_background_script():
    try:
        # Check if the background script exists
        if not os.path.exists('db_and_update_box.py'):
            raise FileNotFoundError("Background script 'db_and_update_box.py' not found.")
        
        # Run the background script using os.system
        os.system("python db_and_update_box.py")
    except Exception as e:
        # Print the error to console and show an error message in the GUI
        print(f"Error in background script: {e}")
        messagebox.showerror("Error", f"An error occurred in the background process: {str(e)}")

# Start the background script in a separate thread
try:
    # Create a thread to run the background script
    background_thread = threading.Thread(target=run_background_script)
    background_thread.daemon = True  # Daemon thread will close when the main program exits
    background_thread.start()
except Exception as e:
    # Print the error to console and show an error message if the thread fails to start
    print(f"Failed to start background thread: {e}")
    messagebox.showerror("Error", f"Failed to start background process: {str(e)}")

# Initialize the main tkinter window
root = tk.Tk()
root.title("Data Interface")
root.geometry("800x600")  # Set window size

# Set custom font for buttons
custom_font = tkFont.Font(family="Helvetica", size=10)  # Slightly larger font for better readability

# Create a frame on the left side for buttons
button_frame = tk.Frame(root, width=120)  # Fixed width for the button frame
button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Define a global variable to keep track of the currently highlighted button
current_highlighted_button = None

# Function to switch between different screens in the main frame
def switch_screen(screen_function):
    """Utility function to switch between screens smoothly"""
    # Destroy all existing widgets in the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    try:
        # Call the function to show the new screen
        screen_function(main_frame)
    except Exception as e:
        # Print the error and show an error message if screen switching fails
        print(f"Error while switching screen: {e}")
        messagebox.showerror("Error", f"An error occurred while switching screens: {str(e)}")

# Function to handle button clicks and switch screens
def handle_button_click(button, screen_function):
    global current_highlighted_button
    # Remove highlight from the previously clicked button
    if current_highlighted_button:
        current_highlighted_button.config(bg="SystemButtonFace")
    # Highlight the clicked button
    button.config(bg="gray")
    current_highlighted_button = button
    # Switch the screen to the one associated with the clicked button
    switch_screen(screen_function)

try:
    # Create the HOME button and set it as the default highlighted button
    report_button = tk.Button(button_frame, text="HOME", command=lambda: handle_button_click(report_button, show_home_screen), 
                             width=10, height=1, font=custom_font, bg="gray")  # Highlighted by default
    report_button.pack(pady=10)

    # Set the report_button as the current highlighted button by default
    current_highlighted_button = report_button

    # Create the DELETE button
    delete_button = tk.Button(button_frame, text="DELETE", command=lambda: handle_button_click(delete_button, show_delete_screen), 
                             width=10, height=1, font=custom_font)
    delete_button.pack(pady=10)

    # Create the BACKUP button
    backup_button = tk.Button(button_frame, text="BACKUP", command=lambda: handle_button_click(backup_button, show_backup_screen), 
                             width=10, height=1, font=custom_font)
    backup_button.pack(pady=10)

    # Create the main frame where different screens will be shown
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Show the initial HOME screen by default
    show_home_screen(main_frame)

except Exception as e:
    # Print the error and show an error message if GUI initialization fails
    print(f"Error initializing GUI: {e}")
    messagebox.showerror("Error", f"An error occurred while initializing the GUI: {str(e)}")

# Start the tkinter main loop to keep the GUI running
root.mainloop()
