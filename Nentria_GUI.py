# Alpha Version! Not for production use!

import tkinter as tk
from tkinter import PhotoImage
import pyotp
import os
from PIL import Image, ImageTk

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Correct PIN code
CORRECT_PIN = "190211"
entered_pin = [""] * 6

# Function to handle PIN code entry and automatically move to the next field
def on_key_press(event):
    global entered_pin
    key = event.char
    if key.isdigit():
        for i in range(6):
            if entered_pin[i] == "":
                entered_pin[i] = key
                pin_labels[i].config(text="*")
                break
        # Collect all the entered characters from the 6 labels
        pin_code = ''.join(entered_pin)
        # If all fields are filled (i.e., 6 digits), process the PIN
        if len(pin_code) == 6:
            if pin_code == CORRECT_PIN:
                cls()
                print(f"Entered PIN: {pin_code}")
                # Clear the screen and make the window larger
                root.minsize(780,600)
                root.maxsize(780,600)
                root.title("Nentria Dashboard")
                create_totp_label()
                display_totp_code()
                update_totp_code()
                show_dashboard()
            else:
                # Display "Wrong code" message
                error_label.config(text="Wrong code", fg="red", font=("Arial", 12, "bold"))
                root.after(5000, lambda: error_label.config(text=""))
                # Clear the fields
                entered_pin = [""] * 6
                for label in pin_labels:
                    label.config(text="")
    elif key == "\b":
        for i in range(5, -1, -1):
            if entered_pin[i] != "":
                entered_pin[i] = ""
                pin_labels[i].config(text="")
                break

# Function to display the current TOTP code
def display_totp_code():
    with open(os.path.join(script_dir, 'example-key.totp'), 'r') as file:
        totp_key = file.read().strip()
    global totp
    totp = pyotp.TOTP(totp_key)
    current_code = totp.now()
    totp_label.config(text=f"Current TOTP Code: {current_code}")

# Function to update the TOTP code every second
def update_totp_code():
    current_code = totp.now()
    totp_label.config(text=f"Current TOTP Code: {current_code}")
    root.after(1000, update_totp_code)

# Function to create the TOTP label
def create_totp_label():
    global totp_label
    totp_label = tk.Label(root, text="", font=("Arial", 20), fg="#000000", bg="#0153FF")
    totp_label.place(relx=0.5, rely=0.1, anchor="center")

# Function to show the dashboard with buttons
def show_dashboard():
    # Create a frame for the left-side buttons
    left_frame = tk.Frame(root, bg="#0153FF")
    left_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)

    # Create a frame for the bottom buttons
    bottom_frame = tk.Frame(root, bg="#0153FF")
    bottom_frame.place(relx=0.2, rely=0.7, relwidth=0.8, relheight=0.2)

    # Add buttons to the left frame
    btn1 = tk.Button(left_frame, bg="#0153FF", fg="#0153FF", image=home_icon, compound="left", activebackground="#0153FF", highlightbackground="#0153FF")
    btn1.pack(pady=10, padx=35, fill='x')

    btn2 = tk.Button(left_frame, bg="#0153FF", fg="#0153FF", image=passwords_icon, compound="left", activebackground="#0153FF", highlightbackground="#0153FF")
    btn2.pack(pady=10, padx=35, fill='x')

    btn3 = tk.Button(left_frame, bg="#0153FF", fg="#0153FF", image=totp_icon, compound="left", activebackground="#0153FF", highlightbackground="#0153FF")
    btn3.pack(pady=10, padx=35, fill='x')

    btn4 = tk.Button(left_frame, bg="#0153FF", fg="#0153FF", image=generator_icon, compound="left", activebackground="#0153FF", highlightbackground="#0153FF")
    btn4.pack(pady=10, padx=35, fill='x')

    btn5 = tk.Button(left_frame, bg="#0153FF", fg="#0153FF", image=safe_icon, compound="left", activebackground="#0153FF", highlightbackground="#0153FF")
    btn5.pack(pady=10, padx=35, fill='x')

    btn6 = tk.Button(left_frame, bg="#0153FF", fg="#0153FF", image=settings_icon, compound="left", activebackground="#0153FF", highlightbackground="#0153FF")
    btn6.pack(pady=10, padx=35, fill='x')
    
# Function to clear all tkinter widgets
def cls():
    for widget in root.winfo_children():
        widget.destroy()

# Create the main application window
root = tk.Tk()
root.title("Nentria Sign-In")
root.minsize(475,250)
root.maxsize(475,250)
root.configure(bg="#0153FF")

# Load and resize icons
icon_size = (70, 70)
home_icon = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "icons/home.png")).resize(icon_size, Image.LANCZOS))
passwords_icon = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "icons/passwords.png")).resize(icon_size, Image.LANCZOS))
totp_icon = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "icons/totp.png")).resize(icon_size, Image.LANCZOS))
generator_icon = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "icons/generator.png")).resize(icon_size, Image.LANCZOS))
safe_icon = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "icons/safe.png")).resize(icon_size, Image.LANCZOS))
settings_icon = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "icons/settings.png")).resize(icon_size, Image.LANCZOS))

# Center the window on the screen
root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())

# Create a frame to center the PIN input
frame = tk.Frame(root, bg="#0153FF")
frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=150)

# Product Name Label
product_label = tk.Label(frame, text="Nentria", font=("Arial", 24, "bold"), fg="#000000", bg="#0153FF")
product_label.grid(row=0, column=0, columnspan=6, pady=10)

# PIN Code Label
pin_label = tk.Label(frame, text="Enter PIN:", font=("Arial", 14), fg="#000000", bg="#0153FF")
pin_label.grid(row=1, column=0, columnspan=6, pady=5)

# Create 6 separate Label widgets for PIN code display
pin_labels = []
for i in range(6):
    label = tk.Label(frame, text="", font=("Arial", 18), justify="center", width=2, bg="#ffffff", fg="#000000")
    label.grid(row=2, column=i, padx=10, pady=10)
    pin_labels.append(label)

# Error message label
error_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="red", bg="#0153FF")
error_label.place(relx=0.5, rely=0.9, anchor="center")

# TOTP code label
totp_label = tk.Label(root, text="", font=("Arial", 20), fg="#000000", bg="#0153FF")
totp_label.place(relx=0.5, rely=0.1, anchor="center")

# Bind the keyboard events to detect changes
root.bind("<Key>", on_key_press)

# Run the application
root.mainloop()
