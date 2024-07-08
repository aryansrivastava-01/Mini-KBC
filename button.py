import tkinter as tk
from tkinter import font as tkfont

# Create main application window
root = tk.Tk()
root.title("Who Wants to Be a Millionaire - Custom Button")
root.geometry("400x300")

# Function to create custom button
def create_custom_button():
    # Custom font
    custom_font = tkfont.Font(family="Helvetica", size=14, weight="bold")

    # Create a button with custom styles
    custom_button = tk.Button(root, text="Tinker", font=custom_font, bg="#4CAF50", fg="white",
                              activebackground="#45a049", activeforeground="white", 
                              padx=20, pady=10, borderwidth=3, relief="raised")

    custom_button.pack(pady=50)

create_custom_button()

# Run the application
root.mainloop()
