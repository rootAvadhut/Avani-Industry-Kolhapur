import threading  # Import threading to run background tasks
import tkinter as tk  # Import tkinter for GUI
import tkinter.font as tkFont  # Import tkinter font for custom fonts in GUI
from tkinter import messagebox  # Import messagebox to show error dialogs
import asyncio  # Import asyncio to run async functions
from imports import show_home_screen, show_delete_screen, show_backup_screen  # Import custom functions for different screens
from db_and_update_box import monitor_files  # Import monitor_files from db_and_update_box
from modbus import run_modbus_client  # Import run_modbus_client from modbus


# Create an event to signal the background threads to stop
stop_event = threading.Event()

async def run_background_tasks():
    try:
        # Run the file monitoring and Modbus client tasks
        task1 = asyncio.create_task(monitor_files(stop_event))
        task2 = asyncio.create_task(run_modbus_client(stop_event))
        await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)
    except Exception as e:
        # Print the error to console and show an error message in the GUI
        print(f"Error in background tasks: {e}")
        messagebox.showerror("Error", f"An error occurred in the background process: {str(e)}")

# Wrapper to run the async function in a thread
def run_background_thread():
    asyncio.run(run_background_tasks())

# Start the background script in a separate thread
try:
    # Create a thread to run the background tasks
    background_thread = threading.Thread(target=run_background_thread)
    background_thread.daemon = True  # Daemon thread will close when the main program exits
    background_thread.start()
except Exception as e:
    # Print the error to console and show an error message if the thread fails to start
    print(f"Failed to start background thread: {e}")
    messagebox.showerror("Error", f"Failed to start background process: {str(e)}")

# Function to handle closing the GUI
def on_close():
    # Set the stop event to signal the threads to stop
    stop_event.set()
    # Wait for the threads to finish
    background_thread.join()
    # Destroy the GUI window
    root.destroy()

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

# Bind the on_close function to the window close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the tkinter main loop to keep the GUI running
root.mainloop()
