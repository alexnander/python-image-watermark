import tkinter as tk
import tkinter.filedialog as dlg
from PIL import Image, UnidentifiedImageError, ImageDraw
import datetime
import math

# global declarations
text_widget = None
selected_options = ("horizontal", "45 degrees", "-45 degrees")
selected = "horizontal"


def open_image():
    filename = dlg.askopenfilename(filetypes=[("Image file...", ".jpg .jpeg .png .gif .bmp")])

    # Check if file is selected
    if filename == '':
        return
    try:
        image = Image.open(filename)
        watermark_text = text_widget.get()
        image_watermarked = draw_watermark(image, watermark_text)
        # save watermarked file
        save_filename = dlg.asksaveasfilename(confirmoverwrite=True,
                                              filetypes=[("Image file...", ".png")],
                                              defaultextension=[("Image file...", ".png")],
                                              initialfile=filename)
        print(save_filename)
        image_watermarked.save(save_filename)

    except UnidentifiedImageError:
        print(f"{filename} has unrecognized format.")


def set_selected(text):
    global selected
    # print(text)
    selected = text


def draw_watermark(image, text):
    # calculate the diagonal for rotations cropping (so tiling covers all corners)
    cropping_oversize = math.floor(math.sqrt(image.size[0] ** 2 + image.size[1] ** 2))
    # make sure cropping_oversize divides by 2
    cropping_oversize = cropping_oversize + 1 if cropping_oversize % 2 else cropping_oversize

    watermark_text = Image.new("RGBA",
                               (image.size[0] + cropping_oversize, image.size[1] + cropping_oversize),
                               (255, 255, 255, 0))
    draw_ctx = ImageDraw.Draw(watermark_text)

    # draw down column every 100 px to bottom of context
    # shift right by 50 and down 50 and repeat down column
    # repeat until draw location is outside of
    x_offset = 10
    y_offset = 10
    count = 0  # number of columns drawn so far
    while x_offset < watermark_text.size[0]:
        while y_offset < watermark_text.size[1]:
            draw_ctx.text((x_offset, y_offset), text, fill=(255, 255, 255, 85))
            y_offset += 150
        count += 1
        y_offset = count % 2 * 50 + 10
        x_offset += 150

    angle = 0
    if selected != "horizontal":
        if '-' in selected:
            angle = -45
        else:
            angle = 45

    watermark_text = watermark_text.rotate(angle, resample=Image.BICUBIC)

    crop = cropping_oversize / 2
    watermark_text = watermark_text.crop((crop, crop,
                                          watermark_text.size[0] - crop, watermark_text.size[1] - crop))
    out = Image.alpha_composite(image.convert("RGBA"), watermark_text)

    out.show()

    return out


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
