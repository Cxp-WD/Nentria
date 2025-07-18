# Alpha Version! Not for production use!

import tkinter as tk
import keyboard

# Correct PIN code
CORRECT_PIN = "190211"
entered_pin = [""] * 6

# Variable to track if the user is signed in
is_signed_in = False

# Function to handle PIN code entry and automatically move to the next field
def on_key_press(event):
    global entered_pin, is_signed_in
    if is_signed_in:
        return  # Ignore key presses if signed in
    key = event.name
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
                print(f"Entered PIN: {pin_code}")
                on_successful_sign_in()
            else:
                # Display "Wrong code" message
                error_label.config(text="Wrong code", fg="red", font=("Arial", 12, "bold"))
                root.after(5000, lambda: error_label.config(text=""))
                # Clear the fields
                entered_pin = [""] * 6
                for label in pin_labels:
                    label.config(text="")
    elif key == "backspace":
        for i in range(5, -1, -1):
            if entered_pin[i] != "":
                entered_pin[i] = ""
                pin_labels[i].config(text="")
                break

# Function to handle sign out
def sign_out():
    global is_signed_in, entered_pin
    is_signed_in = False
    entered_pin = [""] * 6
    for label in pin_labels:
        label.config(text="")
    frame.pack(pady=20)
    dashboard_frame.pack_forget()
    root.geometry("400x250")
    root.title("Nentria Sign-In")
    root.configure(bg="#5a908c")

# Create the main application window
root = tk.Tk()
root.title("Nentria Sign-In")
<<<<<<< HEAD:Archine/Nentria.py
root.geometry("400x250")  # Set a larger window size
root.configure(bg="#5a908c")
=======
root.geometry("450x250")  # Set a larger window size
root.configure(bg="#0153FF")
>>>>>>> 22bc3b7380b6d189832c4495ce3428150b96b772:Nentria.py

# Center the window on the screen
root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())

# Create a frame to center the PIN input
frame = tk.Frame(root, bg="#5a908c")
frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=150)

# Product Name Label
product_label = tk.Label(frame, text="Nentria", font=("Arial", 24, "bold"), fg="#000000", bg="#5a908c")
product_label.grid(row=0, column=0, columnspan=6, pady=10)

# PIN Code Label
pin_label = tk.Label(frame, text="Enter PIN:", font=("Arial", 14), fg="#000000", bg="#5a908c")
pin_label.grid(row=1, column=0, columnspan=6, pady=5)

# Create 6 separate Label widgets for PIN code display
pin_labels = []
for i in range(6):
    label = tk.Label(frame, text="", font=("Arial", 18), justify="center", width=2, bg="#ffffff", fg="#000000")
    label.grid(row=2, column=i, padx=10, pady=10)
    pin_labels.append(label)

# Error message label
error_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="red", bg="#5a908c")
error_label.place(relx=0.5, rely=0.9, anchor="center")

# Create a frame for the dashboard
dashboard_frame = tk.Frame(root, bg="#5a908c")
sign_out_button = tk.Button(dashboard_frame, text="Sign Out", command=sign_out, font=("Arial", 14), bg="#ffffff", fg="#000000")
sign_out_button.pack(pady=20)

# Function to handle successful sign in
def on_successful_sign_in():
    global is_signed_in
    is_signed_in = True
    frame.pack_forget()
    dashboard_frame.pack(expand=True, fill="both")
    root.geometry("1200x1000")
    root.title("Nentria Dashboard")

# Bind the keyboard events to detect changes
keyboard.on_press(on_key_press)

# Run the application
root.mainloop()
