# Alpha Version! Not for production use!

import tkinter as tk
import keyboard

# Correct PIN code
CORRECT_PIN = "190211"
entered_pin = [""] * 6

# Function to handle PIN code entry and automatically move to the next field
def on_key_press(event):
    global entered_pin
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
                # Clear the screen and make the window larger
                frame.destroy()
                root.geometry("600x400")
                root.title("Nentria Dashboard")
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

# Create the main application window
root = tk.Tk()
root.title("Nentria Sign-In")
root.geometry("450x250")  # Set a larger window size
root.configure(bg="#0153FF")

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

# Bind the keyboard events to detect changes
keyboard.on_press(on_key_press)

# Run the application
root.mainloop()
