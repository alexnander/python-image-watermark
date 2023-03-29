import tkinter as tk
import tkinter.filedialog as dlg
from PIL import ImageTk, Image
import datetime

text_widget = None
selected_options = ("horizontal", "30 degrees", "-30 degrees")
selected = "horizontal"


def open_image():
    filename = dlg.askopenfilename(filetypes=[("Image file...", ".jpg .jpeg .png .gif .bmp")])

    # Check if file is selected
    if filename == '':
        return
    # print(f"{filename}")
    image1 = ImageTk.PhotoImage(Image.open(filename))
    watermark_text = text_widget.get()


def set_selected(text):
    global selected
    # print(text)
    selected = text


# Setup TK window and widgets
window = tk.Tk()
window.title("Image Watermark Maker")
window.config(padx=50, pady=20)

# Setup watermark label and text entry
label_1 = tk.Label(text="1. Enter text you want as your\n"
                        "watermark in the field below.")
label_1.pack()

text_widget = tk.Entry()
text_widget.insert(0, f"Watermark © {datetime.date.today().year}")
text_widget.pack()

# Setup watermark orientation dropdown options
label_2 = tk.Label(text="2. Choose the orientation of\n"
                        "your watermark.")
label_2.pack()

menu = tk.StringVar()
menu.set("horizontal")
drop = tk.OptionMenu(window, menu, *selected_options, command=set_selected)
drop.pack()

# Setup filename dialog button
label_3 = tk.Label(text="3. Open the image file you want\n"
                        "to apply the watermark.")
label_3.pack()

open_button = tk.Button()
open_button.config(text="Open Image...", command=open_image)
open_button.pack()

# TK window mainloop to display and interpret inputs
window.mainloop()
