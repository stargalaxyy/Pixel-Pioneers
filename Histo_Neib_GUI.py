import numpy as np
import tkinter as tk
import cv2  # Import OpenCV for image processing
import ImageHistogram as ih
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import NeighborhoodProcessing as ft
import subprocess
# Global image variables
result_image = None  # Placeholder for processed image result
# Global image variables
original_image = None  # Stores the original loaded image (PIL Image object)
displayed_image = None  # Stores currently displayed image (PIL Image or PhotoImage)

# Image Histogram & Neigborhood Processing Page
root = tk.Tk()
root.title("Histogram & Neigborhood Processing")
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


#__image display function

def display_image(label, img_array):
    img = Image.fromarray(img_array)
    img = img.resize((500, 500))
    imgtk = ImageTk.PhotoImage(img)
    label.config(image=imgtk)
    label.image = imgtk
    
# Load Image Function
def load_image():
    global original_image, displayed_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        original_image = Image.open(file_path).convert("L")
        original_image = original_image.resize((500, 500))
        displayed_image = None
        display_image(image_label, np.array(original_image))

#save result image
def save_result():
    if result_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            cv2.imwrite(file_path, result_image)
            messagebox.showinfo("Success", "Image saved successfully!")

def apply_operation(op):
    global result_image
    if original_image is None:
        messagebox.showerror("Error", "No image loaded!")
        return
    result_image = op(original_image)
    display_image(res_label, result_image)  


btn_load = create_btn("Load Image", load_image)
btn_load.pack(pady=10)

btn_show = create_btn("Show Original", lambda: show_image("original"))
btn_stretch = create_btn("Histogram Stretching", lambda: process_image("stretch"))
btn_equalize = create_btn("Histogram Equalization", lambda: process_image("equalize"))

btn_show.pack(pady=10)

tk.Label(scrollable_frame, text = "Image Histogram", fg = "white", bg = "#0a2a2f", font = ("Arial", 18, "bold")).pack(pady=(10, 5))
tk.Frame(scrollable_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))

btn_stretch.pack(pady=10)
btn_equalize.pack(pady=10)

tk.Label(scrollable_frame, text = "Neighborhood Processing", fg = "white", bg = "#0a2a2f", font = ("Arial", 18, "bold")).pack(pady=(20, 10))
tk.Frame(scrollable_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))
tk.Label(scrollable_frame, text = "Linear Filter", fg = "white", bg = "#0a2a2f", font = ("Arial", 14, "bold")).pack(pady=(3, 10))

btn_average_filter = create_btn("Average Filter", lambda: process_image("average filter"))
btn_laplacian_filter = create_btn("Laplacian Filter", lambda: process_image("laplacian filter"))

btn_average_filter.pack(pady = 10)
btn_laplacian_filter.pack(pady = 10)

tk.Label(scrollable_frame, text = "Non-Linear Filter", fg = "white", bg = "#0a2a2f", font = ("Arial", 14, "bold")).pack(pady=(3, 10))

btn_max = create_btn("Maximum", lambda: process_image("maximum"))
btn_min = create_btn("Minimum", lambda: process_image("minimum"))
btn_median = create_btn("Median", lambda: process_image("median"))
btn_mode = create_btn("Mode", lambda: process_image("mode"))

btn_max.pack(pady = 10)
btn_min.pack(pady = 10)
btn_median.pack(pady = 10)
btn_mode.pack(pady = 10)

tk.Label(scrollable_frame, text = "More Options", fg = "white", bg = "#0a2a2f", font = ("Arial", 14, "bold")).pack(pady=(10, 10))
tk.Frame(scrollable_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))

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
    res_label.config(image=None)
    res_label.image = None
    
def go_back():
    subprocess.Popen(["python", "main_gui" + ".py"])
    root.destroy()
    
def disable_close():
    pass  # Do nothing when "X" is clicked


# Override the close button behavior
root.protocol("WM_DELETE_WINDOW", disable_close)

btn_clear_image = create_btn("Clear Image", clear_image)
btn_back = create_btn("Back", go_back)

btn_clear_image.pack(pady = 10)
btn_back.pack(pady = 10)
# Image display frame
image_frame = tk.Frame(main_frame, bg="#0a2a2f", bd=2, relief="groove")
image_frame.pack(side="right", expand=True, fill="both", padx=20)

title_label = tk.Label(image_frame, text="Original Image                                         Result Image",
                       fg="white", bg="#0a2a2f", font=("Arial", 16, "bold"))
title_label.pack(pady=(10,20))

images_holder = tk.Frame(image_frame, bg="#0a2a2f")
images_holder.pack(expand=True, fill="both")

# Define image_label and res_label
image_label = tk.Label(images_holder, bg="#0a2a2f")
image_label.pack(side="left", expand=True)

res_label = tk.Label(images_holder, bg="#0a2a2f")
res_label.pack(side="right", expand=True)

# Show Image Function
def show_image(mode):
    global displayed_image
    if original_image is None:
        tk.messagebox.showerror("Error", "No image loaded! Please load an image first.")
        return
    if mode == "original" and original_image:
        img = original_image.copy()
        img = img.resize((600, 500))  # Resize to match the same size
        displayed_image = ImageTk.PhotoImage(img)
        image_label.config(image=displayed_image)
        image_label.image = displayed_image
    elif mode == "displayed" and displayed_image:
        if isinstance(displayed_image, Image.Image):
            img = displayed_image.copy()
            img = img.resize((600, 500))  # Resize to match the same size
            displayed_image = ImageTk.PhotoImage(img)
            res_label.config(image=displayed_image)
            res_label.image = displayed_image
        else:
            res_label.config(image=displayed_image)

# Adjust layout to place images side by side
image_label.pack(side="left", expand=True, padx=10, pady=10)
res_label.pack(side="left", expand=True, padx=10, pady=10)

# Process Image
def process_image(mode):
    global displayed_image
    if original_image is None:
        tk.messagebox.showerror("Error", "No image loaded! Please load an image first.")
        return
    
    histogram_actions = {
        "stretch": ih.histogram_stretching,
        "equalize": ih.histogram_equalization
    }

    filter_actions = {
        "average filter": ft.average_filter,
        "laplacian filter": ft.laplacian_filter,
        "maximum": ft.max_filter,
        "minimum": ft.min_filter,
        "median": ft.median_filter,
        "mode": ft.mode_filter
    }
    
    if mode in histogram_actions:
        img_array = np.array(original_image)
        histogram_array = histogram_actions[mode](img_array)
        histogram_img = Image.fromarray(histogram_array)
        displayed_image = histogram_img.copy()
        show_image("displayed")
    elif mode in filter_actions:
        img_array = np.array(original_image)
        filtered_array = filter_actions[mode](img_array)
        filtered_img = Image.fromarray(filtered_array)
        displayed_image = filtered_img.copy()
        show_image("displayed")
def save_image():
    global displayed_image
    if displayed_image is None:
        tk.messagebox.showerror("Error", "No image to save! Please process an image first.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("BMP files", "*.bmp")])
    if file_path:
        displayed_image.save(file_path)

btn_save_image = create_btn("Save Image", save_image)
btn_save_image.pack(pady=10)
btn_save_image.bind("<Enter>", on_enter)
root.mainloop()