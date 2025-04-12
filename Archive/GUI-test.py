from tkinter import Tk, Label
from PIL import Image, ImageTk

def create_diagonal_gradient(width, height, start_color, end_color):
    """Create a subtle diagonal gradient."""
    image = Image.new("RGB", (width, height))
    
    for y in range(height):
        for x in range(width):
            ratio = (x + y) / (width + height)  # Normalize between 0-1
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            image.putpixel((x, y), (r, g, b))

    return ImageTk.PhotoImage(image)

# Tkinter Setup
root = Tk()
root.geometry("500x400")

# More Subtle Cyan to Blue Gradient
gradient = create_diagonal_gradient(500, 400, (0, 255, 255), (0, 80, 160))  

label = Label(root, image=gradient)
label.place(x=0, y=0, relwidth=1, relheight=1)  # Stretch image to fit window

root.mainloop()
