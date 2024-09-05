# Function to run the background script
from modbus import *
def run_modbus_script():
    try:
        # Run the background script while checking for the stop event
        run_modbus_client(stop_event)
    except Exception as e:
        logging.error(f"Error in run_modbus_client: {e}")
        messagebox.showerror("Error", f"An error occurred in the background modbus process: {str(e)}")

# Start the background script in a separate thread
try:
    # Create a thread to run the background script
    background_thread = threading.Thread(target=run_modbus_script)
    background_thread.daemon = True  # Daemon thread will close when the main program exits
    background_thread.start()
except Exception as e:
    logging.error(f"Failed to start background modbus thread: {e}")
    messagebox.showerror("Error", f"Failed to start background modbus process: {str(e)}")