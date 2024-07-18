from imports import tk, ttk, tkFont, DateEntry, show_home_screen, show_delete_screen

root = tk.Tk()
root.title("Data Interface")
root.geometry("800x600")

custom_font = tkFont.Font(family="Helvetica", size
                          =10)  # Slightly larger font for better readability

button_frame = tk.Frame(root, width=120)  # Fixed width for the button frame
button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

def switch_screen(screen_function):
    """Utility function to switch between screens smoothly"""
    for widget in main_frame.winfo_children():
        widget.destroy()
    screen_function(main_frame)

report_button = tk.Button(button_frame, text="HOME", command=lambda: switch_screen(show_home_screen), 
                         width=10, height=1, font=custom_font)  # Increased height for the buttons
report_button.pack(pady=10)

delete_button = tk.Button(button_frame, text="DELETE", command=lambda: switch_screen(show_delete_screen), 
                         width=10, height=1, font=custom_font)
delete_button.pack(pady=10)

main_frame = tk.Frame(root)
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Initial screen:
show_home_screen(main_frame) 

root.mainloop() 
