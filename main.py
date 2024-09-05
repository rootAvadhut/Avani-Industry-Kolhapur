import asyncio
import threading
import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from imports import show_home_screen, show_delete_screen, show_backup_screen
from db_and_update_box import monitor_files
import sys
from modbus import run_modbus_client
import logging
# logger = logging.getLogger('main')


# Configure logging for main.py
log_file_path = 'app_logs/main_app.log'
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')
# logger = logging.getLogger('main')
# logger.setLevel(logging.INFO)

# log_file_path = './app_logs/main_app.log'
# log_dir=os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# if log_dir:
#     os.makedirs(log_dir, exist_ok=True)

# handler = logging.FileHandler(log_file_path)
# formatter = logging.Formatter('%(asctime)s - %(message)s')
# handler.setFormatter(formatter)

# logger.addHandler(handler)

# Redirect stdout and stderr to the log file
class LogRedirector:
    def __init__(self, logger):
        self.logger = logger

    def write(self, message):
        if message.strip():
            self.logger.info(message.strip())

    def flush(self):
        pass

sys.stdout = LogRedirector(logging)
sys.stderr = LogRedirector(logging)

# Create an event to signal the background thread to stop
stop_event = threading.Event()

# def run_modbus_script():
#     try:
#         # Run the background script while checking for the stop event
#         run_modbus_client(stop_event)
#     except Exception as e:
#         logging.error(f"Error in run_modbus_client: {e}")
#         messagebox.showerror("Error", f"An error occurred in the background Modbus process: {str(e)}")
def run_modbus_script():
    try:
        # Use asyncio.run to execute the coroutine
        asyncio.run(run_modbus_client(stop_event))
    except Exception as e:
        logging.error(f"Error in run_modbus_client: {e}")
        messagebox.showerror("Error", f"An error occurred in the Modbus process: {str(e)}")


# def run_background_script():
#     try:
#         # Run the background script while checking for the stop event
#         monitor_files(stop_event)
#     except Exception as e:
#         logging.error(f"Error in background script: {e}")
#         messagebox.showerror("Error", f"An error occurred in the background process: {str(e)}")
def run_background_script():
    try:
        # Use asyncio.run to execute the coroutine
        asyncio.run(monitor_files(stop_event))
    except Exception as e:
        logging.error(f"Error in background script: {e}")
        messagebox.showerror("Error", f"An error occurred in the background process: {str(e)}")


# Start the background scripts in separate threads
try:
    modbus_thread = threading.Thread(target=run_modbus_script)
    modbus_thread.daemon = True
    modbus_thread.start()

    background_thread = threading.Thread(target=run_background_script)
    background_thread.daemon = True
    background_thread.start()
except Exception as e:
    logging.error(f"Failed to start background thread(s): {e}")
    messagebox.showerror("Error", f"Failed to start background process(es): {str(e)}")

# Function to handle closing the GUI
# def on_close():
#     stop_event.set()
#     modbus_thread.join()
#     background_thread.join()
#     root.destroy()
def on_close():
    logging.info("Closing application...")
    stop_event.set()
    modbus_thread.join(timeout=5)  # Allow 5 seconds to terminate
    background_thread.join(timeout=5)
    root.destroy()
    logging.info("Application closed successfully.")


# Initialize the main tkinter window
root = tk.Tk()
root.title("Data Interface")
root.geometry("800x600")
logging.info("the main.py file")

# Set custom font for buttons
custom_font = tkFont.Font(family="Helvetica", size=10)

# Create a frame on the left side for buttons
button_frame = tk.Frame(root, width=120)
button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

current_highlighted_button = None

# Function to switch between different screens in the main frame
def switch_screen(screen_function):
    for widget in main_frame.winfo_children():
        widget.destroy()
    try:
        screen_function(main_frame)
    except Exception as e:
        logging.error(f"Error while switching screen: {e}")
        messagebox.showerror("Error", f"An error occurred while switching screens: {str(e)}")

# Function to handle button clicks and switch screens
def handle_button_click(button, screen_function):
    global current_highlighted_button
    if current_highlighted_button:
        current_highlighted_button.config(bg="SystemButtonFace")
    button.config(bg="gray")
    current_highlighted_button = button
    switch_screen(screen_function)

try:
    report_button = tk.Button(button_frame, text="HOME", command=lambda: handle_button_click(report_button, show_home_screen), 
                             width=10, height=1, font=custom_font, bg="gray")
    report_button.pack(pady=10)

    current_highlighted_button = report_button

    delete_button = tk.Button(button_frame, text="DELETE", command=lambda: handle_button_click(delete_button, show_delete_screen), 
                             width=10, height=1, font=custom_font)
    delete_button.pack(pady=10)

    backup_button = tk.Button(button_frame, text="BACKUP", command=lambda: handle_button_click(backup_button, show_backup_screen), 
                             width=10, height=1, font=custom_font)
    backup_button.pack(pady=10)

    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    show_home_screen(main_frame)

except Exception as e:
    logging.error(f"Error initializing GUI: {e}")
    messagebox.showerror("Error", f"An error occurred while initializing the GUI: {str(e)}")

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()



# import threading  # Import threading to run background tasks
# import os  # Import os to interact with the operating system
# import tkinter as tk  # Import tkinter for GUI
# import tkinter.font as tkFont  # Import tkinter font for custom fonts in GUI
# from tkinter import messagebox  # Import messagebox to show error dialogs
# from imports import show_home_screen, show_delete_screen, show_backup_screen  # Import custom functions for different screens
# from db_and_update_box import monitor_files  # Import monitor_files from db_and_update_box

# # Create an event to signal the background thread to stop
# stop_event = threading.Event()

# # Function to run the background script
# def run_background_script():
#     try:
#         # Run the background script while checking for the stop event
#         monitor_files(stop_event)
#     except Exception as e:
#         # Print the error to console and show an error message in the GUI
#         print(f"Error in background script: {e}")
#         messagebox.showerror("Error", f"An error occurred in the background process: {str(e)}")

# # Start the background script in a separate thread
# try:
#     # Create a thread to run the background script
#     background_thread = threading.Thread(target=run_background_script)
#     background_thread.daemon = True  # Daemon thread will close when the main program exits
#     background_thread.start()
# except Exception as e:
#     # Print the error to console and show an error message if the thread fails to start
#     print(f"Failed to start background thread: {e}")
#     messagebox.showerror("Error", f"Failed to start background process: {str(e)}")

# # Function to handle closing the GUI
# def on_close():
#     # Set the stop event to signal the thread to stop
#     stop_event.set()
#     # Wait for the thread to finish
#     background_thread.join()
#     # Destroy the GUI window
#     root.destroy()

# # Initialize the main tkinter window
# root = tk.Tk()
# root.title("Data Interface")
# root.geometry("800x600")  # Set window size

# # Set custom font for buttons
# custom_font = tkFont.Font(family="Helvetica", size=10)  # Slightly larger font for better readability

# # Create a frame on the left side for buttons
# button_frame = tk.Frame(root, width=120)  # Fixed width for the button frame
# button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# # Define a global variable to keep track of the currently highlighted button
# current_highlighted_button = None

# # Function to switch between different screens in the main frame
# def switch_screen(screen_function):
#     """Utility function to switch between screens smoothly"""
#     # Destroy all existing widgets in the main frame
#     for widget in main_frame.winfo_children():
#         widget.destroy()
#     try:
#         # Call the function to show the new screen
#         screen_function(main_frame)
#     except Exception as e:
#         # Print the error and show an error message if screen switching fails
#         print(f"Error while switching screen: {e}")
#         messagebox.showerror("Error", f"An error occurred while switching screens: {str(e)}")

# # Function to handle button clicks and switch screens
# def handle_button_click(button, screen_function):
#     global current_highlighted_button
#     # Remove highlight from the previously clicked button
#     if current_highlighted_button:
#         current_highlighted_button.config(bg="SystemButtonFace")
#     # Highlight the clicked button
#     button.config(bg="gray")
#     current_highlighted_button = button
#     # Switch the screen to the one associated with the clicked button
#     switch_screen(screen_function)

# try:
#     # Create the HOME button and set it as the default highlighted button
#     report_button = tk.Button(button_frame, text="HOME", command=lambda: handle_button_click(report_button, show_home_screen), 
#                              width=10, height=1, font=custom_font, bg="gray")  # Highlighted by default
#     report_button.pack(pady=10)

#     # Set the report_button as the current highlighted button by default
#     current_highlighted_button = report_button

#     # Create the DELETE button
#     delete_button = tk.Button(button_frame, text="DELETE", command=lambda: handle_button_click(delete_button, show_delete_screen), 
#                              width=10, height=1, font=custom_font)
#     delete_button.pack(pady=10)

#     # Create the BACKUP button
#     backup_button = tk.Button(button_frame, text="BACKUP", command=lambda: handle_button_click(backup_button, show_backup_screen), 
#                              width=10, height=1, font=custom_font)
#     backup_button.pack(pady=10)

#     # Create the main frame where different screens will be shown
#     main_frame = tk.Frame(root)
#     main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

#     # Show the initial HOME screen by default
#     show_home_screen(main_frame)

# except Exception as e:
#     # Print the error and show an error message if GUI initialization fails
#     print(f"Error initializing GUI: {e}")
#     messagebox.showerror("Error", f"An error occurred while initializing the GUI: {str(e)}")

# # Bind the on_close function to the window close event
# root.protocol("WM_DELETE_WINDOW", on_close)

# # Start the tkinter main loop to keep the GUI running
# root.mainloop()
