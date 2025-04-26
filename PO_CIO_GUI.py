import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np
import cv2
import subprocess

# Global variables
original_img = None
displayed_image = None
original_photo = None
result_photo = None

# Main GUI setup
root = tk.Tk()
root.title("Point & Color Image Operations")
root.geometry("1920x1080")
root.configure(bg="#0a2a2f")

# Hover functions
def on_enter(event):
    event.widget["background"] = "lightblue"
    event.widget["fg"] = "black"

def on_leave(event):
    event.widget["background"] = "#123c42"
    event.widget["fg"] = "white"

# Main frame
main_frame = tk.Frame(root, bg="#0a2a2f")
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Left panel for buttons
buttons_frame = tk.Frame(main_frame, bg="#0a2a2f")
buttons_frame.pack(side="left", fill="y", padx=20)

canvas = tk.Canvas(buttons_frame, bg="#0a2a2f", highlightthickness=0)
scrollbar = tk.Scrollbar(buttons_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#0a2a2f")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="y", expand=True)
scrollbar.pack(side="right", fill="y")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

# Image display frame
image_frame = tk.Frame(main_frame, bg="#0a2a2f", bd=2, relief="groove")
image_frame.pack(side="right", expand=True, fill="both", padx=20)

title_label = tk.Label(image_frame, text="Original Image                                         Result Image",
                       fg="white", bg="#0a2a2f", font=("Arial", 16, "bold"))
title_label.pack(pady=(10,20))

images_holder = tk.Frame(image_frame, bg="#0a2a2f")
images_holder.pack(expand=True, fill="both")

original_label = tk.Label(images_holder, bg="#0a2a2f")
original_label.pack(side="left", expand=True)

result_label = tk.Label(images_holder, bg="#0a2a2f")
result_label.pack(side="right", expand=True)

# UI functions
def create_section(title):
    tk.Label(scrollable_frame, text=title, fg="white", bg="#0a2a2f",
             font=("Arial", 18, "bold")).pack(pady=(10, 5))
    tk.Frame(scrollable_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))

def create_btn(text, command):
    btn = tk.Button(scrollable_frame, text=text, width=25, height=2, command=command,
                    bg="#123c42", fg="white", font=("Arial", 10, "bold"), bd=0, relief="flat")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def load_image():
    global original_img, original_photo
    path = filedialog.askopenfilename()
    if path:
        original_img = Image.open(path).convert("RGB")
        resized = original_img.resize((500, 500))
        original_photo = ImageTk.PhotoImage(resized)
        original_label.config(image=original_photo)
        original_label.image = original_photo

def show_image(img):
    global result_photo
    resized = img.resize((500, 500))
    result_photo = ImageTk.PhotoImage(resized)
    result_label.config(image=result_photo)
    result_label.image = result_photo
    result_label.image_pil = img

def show_original():
    if original_img:
        show_image(original_img)

def apply_complement():
    if original_img:
        inverted = ImageOps.invert(original_img)
        show_image(inverted)

def change_brightness(val):
    if original_img:
        hsv = cv2.cvtColor(np.array(original_img), cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(hsv)
        v = np.clip(v + val, 0, 255).astype(np.uint8)
        result = cv2.merge((h, s, v))
        result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
        show_image(Image.fromarray(result))

def add_const():
    if original_img:
        x = int(entry_add.get())
        img = np.clip(np.array(original_img).astype(np.int32) + x, 0, 255).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        show_image(Image.fromarray(img))

def sub_const():
    if original_img:
        x = int(entry_sub.get())
        img = np.clip(np.array(original_img).astype(np.int32) - x, 0, 255).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        show_image(Image.fromarray(img))

def mul_const():
    if original_img:
        x = int(entry_mult.get())
        img = np.clip(np.array(original_img).astype(np.int32) * x, 0, 255).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        show_image(Image.fromarray(img))

def div_const():
    if original_img:
        x = int(entry_div.get())
        img = np.clip(np.array(original_img).astype(np.int32) // x, 0, 255).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        show_image(Image.fromarray(img))
# Change lighting color (e.g., red channel adjustment) using OpenCV
def change_color_channel(channel, value):
	if original_img:
		img = cv2.cvtColor(np.array(original_img), cv2.COLOR_RGB2BGR)
		if channel == 'R':
			img[:, :, 2] = np.clip(img[:, :, 2] + value, 0, 255)
		elif channel == 'G':
			img[:, :, 1] = np.clip(img[:, :, 1] + value, 0, 255)
		elif channel == 'B':
			img[:, :, 0] = np.clip(img[:, :, 0] + value, 0, 255)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		show_image(Image.fromarray(img))

# Swap color channels (e.g., R ↔ G)
def swap_color_channels(channel1, channel2):
	if original_img:
		img = np.array(original_img).astype(np.uint8)
		if channel1 == 'R' and channel2 == 'G':
			img[:, :, 2], img[:, :, 1] = img[:, :, 1], img[:, :, 2]
		elif channel1 == 'G' and channel2 == 'B':
			img[:, :, 1], img[:, :, 0] = img[:, :, 0], img[:, :, 1]
		elif channel1 == 'B' and channel2 == 'R':
			img[:, :, 0], img[:, :, 2] = img[:, :, 2], img[:, :, 0]
		show_image(Image.fromarray(img))

# Eliminate color channels (e.g., remove red channel)
def eliminate_color_channel(channel):
	"""Eliminate a specific color channel (e.g., remove red channel)."""
	if original_img:
		img = np.array(original_img).astype(np.uint8)
		if channel == 'R':
			img[:, :, 2] = 0
		elif channel == 'G':
			img[:, :, 1] = 0
		elif channel == 'B':
			img[:, :, 0] = 0
		show_image(Image.fromarray(img))
def save_image():
    if hasattr(result_label, 'image_pil') and result_label.image_pil:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All", "*.*")])
        if save_path:
            result_label.image_pil.save(save_path)

def clear_image():
    global original_img, displayed_image
    original_img = None
    displayed_image = None
    original_label.config(image=None)
    result_label.config(image=None)

def go_back():
    root.destroy()
    subprocess.Popen(["python", "main_gui.py"])

# Layout buttons
create_section("Load & Show Image")
create_btn("Load Image", load_image).pack(pady=5)
create_btn("Show Original", show_original).pack(pady=5)

create_section("Point Operations")
create_btn("Complement", apply_complement).pack(pady=5)
create_btn("Increase Brightness", lambda: change_brightness(30)).pack(pady=5)
create_btn("Decrease Brightness", lambda: change_brightness(-80)).pack(pady=5)

create_btn("Add By", add_const).pack(pady=5)
entry_add = tk.Entry(scrollable_frame, fg="#0a2a2f", bg="white", font=("Arial", 10, "bold"),
                     bd=0, relief="flat", width=30, justify='center')
entry_add.pack()
create_btn("Subtract By", sub_const).pack(pady=5)
entry_sub = tk.Entry(scrollable_frame, fg="#0a2a2f", bg="white", font=("Arial", 10, "bold"),
                     bd=0, relief="flat", width=30, justify='center')
entry_sub.pack()
create_btn("Multiply By", mul_const).pack(pady=5)
entry_mult = tk.Entry(scrollable_frame, fg="#0a2a2f", bg="white", font=("Arial", 10, "bold"),
                      bd=0, relief="flat", width=30, justify='center')
entry_mult.pack()
create_btn("Divide By", div_const).pack(pady=5)
entry_div = tk.Entry(scrollable_frame, fg="#0a2a2f", bg="white", font=("Arial", 10, "bold"),
                     bd=0, relief="flat", width=30, justify='center')
entry_div.pack()
create_section("Color Image Operations")
create_btn("Change Color Channel", lambda: change_color_channel('B', 50)).pack(pady=5)
create_btn("Swap Color Channels", lambda: swap_color_channels('R', 'G')).pack(pady=5)	
create_btn("Eliminate Color Channel", lambda: eliminate_color_channel('R')).pack(pady=5)
create_section("More Options")
create_btn("Save Image", save_image).pack(pady=5)
create_btn("Clear Image", clear_image).pack(pady=5)
create_btn("Back", go_back).pack(pady=5)

root.mainloop()
