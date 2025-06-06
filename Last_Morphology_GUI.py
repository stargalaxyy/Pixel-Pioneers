import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2
import subprocess


# ---------- Morphological Operations (Manual) ----------
def get_mask():
    return np.ones((3, 3), dtype=np.uint8)

def dilate(image):
    padded = np.pad(image, 1, mode='constant', constant_values=0)
    output = np.zeros_like(image)
    mask = get_mask()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            neighbourhood = padded[i:i+3, j:j+3]
            output[i, j] = np.max(neighbourhood * mask)
    return output


def erode(image):
    padded = np.pad(image, 1, mode='constant', constant_values=0)
    output = np.zeros_like(image)
    mask = get_mask()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            neighbourhood = padded[i:i+3, j:j+3]
            output[i, j] = np.min(neighbourhood * mask)
    return output
     

def Sobel(image: np.ndarray) -> np.ndarray:
    sobel_x = np.array([[1, 0, -1],
                        [2, 0, -2],
                        [1, 0, -1]])
    sobel_y = np.array([[1, 2, 1],
                        [0, 0, 0],
                        [-1, -2, -1]])
    gradient_x = cv2.filter2D(image, cv2.CV_64F, sobel_x)
    gradient_y = cv2.filter2D(image, cv2.CV_64F, sobel_y)
    return np.sqrt(gradient_x**2 + gradient_y**2)


def opening(image):
    return dilate(erode(image))

def internal_boundary(image):
    return image - erode(image)

def external_boundary(image):
    return dilate(image) - image

def morphological_gradient(image):
    return dilate(image) - erode(image)

# ---------- GUI ----------
root = tk.Tk()
root.title("Morphological Operations")
root.geometry("1920x1080")
root.configure(bg="#0a2a2f")

original_image = None
result_image = None

# ---------- Layout ----------
main_frame = tk.Frame(root, bg="#0a2a2f")
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

buttons_frame = tk.Frame(main_frame, bg="#0a2a2f")
buttons_frame.pack(side="left", fill="y", padx=20)

scrollable_frame = tk.Frame(buttons_frame, bg="#0a2a2f")
scrollable_frame.pack(side="left", fill="y", expand=True)

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
# ---------- Title ----------
tk.Label(scrollable_frame, text="Morphological Operations", fg="white", bg="#0a2a2f",
         font=("Arial", 20, "bold")).pack(pady=(10, 20))
tk.Frame(scrollable_frame, height = 1, bg = "#2d6b74").pack(fill = "x", pady = (0, 10))

# ---------- Button Utility ----------
def create_button(text, command):
    btn = tk.Button(scrollable_frame, text=text, width=25, height=2, command=command,
                    bg="#123c42", fg="white", font=("Arial", 10, "bold"), bd=0, relief="flat")
    btn.bind("<Enter>", lambda e: btn.config(bg="lightblue", fg="black"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#123c42", fg="white"))
    btn.pack(pady=10)

def display_image(label, img_array):
    img = Image.fromarray(img_array)
    img = img.resize((500, 500))
    imgtk = ImageTk.PhotoImage(img)
    label.config(image=imgtk)
    label.image = imgtk

# ---------- Functionalities ----------
def load_image():
    global original_image, result_image
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (500, 500))
        original_image = img
        result_image = None
        display_image(original_label, original_image)

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
    display_image(result_label, result_image)

def clear_image():
    global original_image, result_image
    original_image = None
    result_image = None
    original_label.config(image='')
    result_label.config(image='')
    
    
def go_back():
    subprocess.Popen(["python", "main_gui" + ".py"])
    root.destroy()
    
def disable_close():
    pass  # Do nothing when "X" is clicked


# Override the close button behavior
root.protocol("WM_DELETE_WINDOW", disable_close)

# ---------- Buttons ----------
create_button("Load Image", load_image)
create_button("Dilation", lambda: apply_operation(dilate))
create_button("Erosion", lambda: apply_operation(erode))
create_button("Opening", lambda: apply_operation(opening))
create_button("Internal Boundary", lambda: apply_operation(internal_boundary))
create_button("External Boundary", lambda: apply_operation(external_boundary))
create_button("Morphological Gradient", lambda: apply_operation(morphological_gradient))
create_button("Sobel Edge Detection", lambda: apply_operation(Sobel))
create_button("Clear Image", clear_image)
create_button("Save Result", save_result)
create_button("Back", go_back)

root.mainloop()
