import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import ImageRestorationS as irs
import ImageRestorationG as irg
import subprocess

# Global image variables
original_image = None  # Stores the original loaded image (PIL Image object)
displayed_image = None  # Stores currently displayed image (PIL Image or PhotoImage)
noised_image = None

# Image Histogram & Neigborhood Processing Page
root = tk.Tk()
root.title("Image Restoration")
root.geometry("1920x1080")
root.configure(bg = "#0a2a2f")

# Hover Functions
def on_enter(button):
    button.widget["background"] = "lightblue"
    button.widget["fg"] = "black"

def on_leave(button):
    button.widget["background"] = "#123c42"
    button.widget["fg"] = "white"

# Main Frame
main_frame = tk.Frame(root, bg = "#0a2a2f")
main_frame.pack(expand = True, fill = "both", padx = 20, pady = 20)

# Buttons Frame (Left Side in Main Frame)
buttons_frame = tk.Frame(main_frame, bg = "#0a2a2f")
buttons_frame.pack(side = "left", fill = "y", padx = 20)

# Scroll Bar
canvas = tk.Canvas(buttons_frame, bg = "#0a2a2f", highlightthickness = 0)
scrollbar = tk.Scrollbar(buttons_frame, orient = "vertical", command = canvas.yview)
scrollable_frame = tk.Frame(canvas, bg = "#0a2a2f")

canvas.configure(yscrollcommand = scrollbar.set)
canvas.pack(side = "left", fill = "y", expand = True)
scrollbar.pack(side = "right", fill = "y")

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def configure_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scrollregion)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

# Create Button Function
def create_btn(text, command):
    btn = tk.Button(scrollable_frame, text = text, width = 25, height = 2, command = command, bg = "#123c42", fg = "white", font = ("Arial", 10, "bold"), bd = 0, relief = "flat")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

tk.Label(scrollable_frame, text = "Load & Show Image", fg = "white", bg = "#0a2a2f", font = ("Arial", 18, "bold")).pack(pady=(10, 10))
tk.Frame(scrollable_frame, height = 1, bg = "#2d6b74").pack(fill = "x", pady = (0, 10))

# Load Image from Files Function
def load_image():
    global original_image, displayed_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        original_image = Image.open(file_path).convert("L")
        original_image = original_image.resize((1100, 800))
        displayed_image = None
        show_image("original")

btn_load = create_btn("Load Image", load_image)
btn_load.pack(pady=10)

btn_show = create_btn("Show Original", lambda: show_image("original"))

btn_show.pack(pady=10)

tk.Label(scrollable_frame, text = "        Image Restoration        ", fg = "white", bg = "#0a2a2f", font = ("Arial", 18, "bold")).pack(pady=(20, 10))
tk.Frame(scrollable_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))
tk.Label(scrollable_frame, text = "Salt & Pepper Noise", fg = "white", bg = "#0a2a2f", font = ("Arial", 14, "bold")).pack(pady=(3, 10))

btn_add_sap_noise = create_btn("Add Noise", lambda: process_image("add noise sap"))
btn_average_filter_1 = create_btn("Average Filter", lambda: process_image("average filter 1"))
btn_median_filter = create_btn("Median Filter", lambda: process_image("median filter"))
btn_an_outlier_method = create_btn("An Outlier Method", lambda: process_image("an outlier method"))

btn_add_sap_noise.pack(pady = 10)
btn_average_filter_1.pack(pady = 10)
btn_median_filter.pack(pady = 10)
btn_an_outlier_method.pack(pady = 10)

tk.Label(scrollable_frame, text = "Gaussian Noise", fg = "white", bg = "#0a2a2f", font = ("Arial", 14, "bold")).pack(pady=(3, 10))

btn_add_noise_g = create_btn("Add Noise", lambda: process_image("add noise g"))
btn_image_averaging = create_btn("Image Averaging", lambda: process_image("image averaging"))
btn_average_filter_2 = create_btn("Average Filter", lambda: process_image("average filter 2"))

btn_add_noise_g.pack(pady = 10)
btn_image_averaging.pack(pady = 10)
btn_average_filter_2.pack(pady = 10)

tk.Label(scrollable_frame, text = "More Options", fg = "white", bg = "#0a2a2f", font = ("Arial", 14, "bold")).pack(pady=(10, 10))
tk.Frame(scrollable_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))

def go_back():
    subprocess.Popen(["python", "main_gui" + ".py"])
    root.destroy()

def disable_close():
    pass  # Do nothing when "X" is clicked


# Override the close button behavior
root.protocol("WM_DELETE_WINDOW", disable_close)

# Clear Image Function
def clear_image():
    global original_image, displayed_image
    if original_image is None:
        tk.messagebox.showerror("Error", "No image loaded! Please load an image first.")
        return
    original_image = None
    displayed_image = None
    image_label.config(image=None)
    image_label.image = None

btn_clear_image = create_btn("Clear Image", clear_image)
btn_back = create_btn("Back", go_back)

btn_clear_image.pack(pady = 10)
btn_back.pack(pady = 10)

image_frame = tk.Frame(main_frame, bg="#0a2a2f", bd=2, relief="groove")
image_frame.pack(side="right", expand=True, fill="both", padx=20)

image_label = tk.Label(image_frame, bg="#0a2a2f")
image_label.pack(expand=True)

# Show Image Function
def show_image(mode):
    global displayed_image
    if original_image is None:
        tk.messagebox.showerror("Error", "No image loaded! Please load an image first.")
        return
    
    if mode == "original":
        # Store the original image reference
        img = original_image.copy()
        img = img.resize((1100, 800))
        displayed_image = original_image  # Store reference to original
        photo_image = ImageTk.PhotoImage(img)
        image_label.config(image=photo_image)
        image_label.image = photo_image
    elif mode == "displayed":
        if displayed_image is None:
            return
        if isinstance(displayed_image, Image.Image):
            img = displayed_image.copy()
            img = img.resize((1100, 800))
            photo_image = ImageTk.PhotoImage(img)
            image_label.config(image=photo_image)
            image_label.image = photo_image

# Process Image
def process_image(mode):
    global displayed_image, noised_image
    if original_image is None:
        tk.messagebox.showerror("Error", "No image loaded! Please load an image first.")
        return
    
    # Noise addition operations
    add_salt_and_pepper_noise = {
        "add noise sap": irs.add_salt_pepper_noise,
    }
    
    add_gaussian_noise = {
        "add noise g": irg.add_gaussian_noise,
    }

    # Filter operations (require noise to be added first)
    salt_and_pepper_filters = {
        "average filter 1": irs.average_filter,
        "median filter": irs.median_filter,
        "an outlier method": irs.outlier_filter
    }

    gaussian_filters = {
        "image averaging": irg.image_averaging,
        "average filter 2": irg.average_filter
    }
    
    # Handle noise addition
    if mode in add_salt_and_pepper_noise:
        img_array = np.array(original_image)
        noised_array = add_salt_and_pepper_noise[mode](img_array)
        noised_image = Image.fromarray(noised_array)
        displayed_image = noised_image  # Store as PIL Image
        show_image("displayed")
        return
    
    if mode in add_gaussian_noise:
        img_array = np.array(original_image)
        noised_array = add_gaussian_noise[mode](img_array)
        noised_image = Image.fromarray(noised_array)
        displayed_image = noised_image  # Store as PIL Image
        show_image("displayed")
        return
    
    # Handle filters - they should only work on noised images
    if mode in salt_and_pepper_filters:
        if noised_image is None or displayed_image == original_image:
            tk.messagebox.showerror("Error", "Please add salt & pepper noise AND don't show original image before applying filters!")
            return
        img_array = np.array(noised_image)
        filtered_array = salt_and_pepper_filters[mode](img_array)
        filtered_image = Image.fromarray(filtered_array)
        displayed_image = filtered_image  # Store as PIL Image
        show_image("displayed")
        return
    
    if mode in gaussian_filters:
        if noised_image is None or displayed_image == original_image:
            tk.messagebox.showerror("Error", "Please add Gaussian noise AND don't show original image before applying filters!")
            return
        img_array = np.array(noised_image)
        filtered_array = gaussian_filters[mode](img_array)
        filtered_image = Image.fromarray(filtered_array)
        displayed_image = filtered_image  # Store as PIL Image
        show_image("displayed")
        return

root.mainloop()