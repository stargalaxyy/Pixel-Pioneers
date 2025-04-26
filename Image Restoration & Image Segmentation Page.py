import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import ImageRestorationS as irs
import ImageRestorationG as irg
import AutomaticThresholding as at1
import AdaptiveThresholding as at2
import BasicGlobalThresholding as bgt
import subprocess

# Global image variables
original_image = None
displayed_image = None
noised_image = None

root = tk.Tk()
root.title("Image Restoration")
root.geometry("1920x1080")
root.configure(bg="#0a2a2f")

def on_enter(button):
    button.widget["background"] = "lightblue"
    button.widget["fg"] = "black"

def on_leave(button):
    button.widget["background"] = "#123c42"
    button.widget["fg"] = "white"

main_frame = tk.Frame(root, bg="#0a2a2f")
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

buttons_frame = tk.Frame(main_frame, bg="#0a2a2f")
buttons_frame.pack(side="left", fill="y", padx=20)

canvas = tk.Canvas(buttons_frame, bg="#0a2a2f", highlightthickness=0)
scrollbar = tk.Scrollbar(buttons_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#0a2a2f")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="y", expand=True)
scrollbar.pack(side="right", fill="y")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def configure_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scrollregion)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

def create_btn(text, command):
    btn = tk.Button(scrollable_frame, text=text, width=25, height=2, command=command,
                    bg="#123c42", fg="white", font=("Arial", 10, "bold"), bd=0, relief="flat")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

tk.Label(scrollable_frame, text="Load & Show Image", fg="white", bg="#0a2a2f", font=("Arial", 18, "bold")).pack(pady=(10, 10))
tk.Frame(scrollable_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))

def load_image():
    global original_image, displayed_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        original_image = Image.open(file_path).convert("L")
        original_image = original_image.resize((500, 400))
        displayed_image = None
        show_image("original")

btn_load = create_btn("Load Image", load_image)
btn_load.pack(pady=10)

btn_show = create_btn("Show Original", lambda: show_image("original"))
btn_show.pack(pady=10)

tk.Label(scrollable_frame, text="        Image Restoration        ", fg="white", bg="#0a2a2f", font=("Arial", 18, "bold")).pack(pady=(20, 10))
tk.Frame(scrollable_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))
tk.Label(scrollable_frame, text="Salt & Pepper Noise", fg="white", bg="#0a2a2f", font=("Arial", 14, "bold")).pack(pady=(3, 10))

btn_add_sap_noise = create_btn("Add Noise", lambda: process_image("add noise sap"))
btn_average_filter_1 = create_btn("Average Filter", lambda: process_image("average filter 1"))
btn_median_filter = create_btn("Median Filter", lambda: process_image("median filter"))
btn_an_outlier_method = create_btn("An Outlier Method", lambda: process_image("an outlier method"))

btn_add_sap_noise.pack(pady=10)
btn_average_filter_1.pack(pady=10)
btn_median_filter.pack(pady=10)
btn_an_outlier_method.pack(pady=10)

tk.Label(scrollable_frame, text="Gaussian Noise", fg="white", bg="#0a2a2f", font=("Arial", 14, "bold")).pack(pady=(3, 10))

btn_add_noise_g = create_btn("Add Noise", lambda: process_image("add noise g"))
btn_image_averaging = create_btn("Image Averaging", lambda: process_image("image averaging"))
btn_average_filter_2 = create_btn("Average Filter", lambda: process_image("average filter 2"))

btn_add_noise_g.pack(pady=10)
btn_image_averaging.pack(pady=10)
btn_average_filter_2.pack(pady=10)

tk.Label(scrollable_frame, text="Image Segmentation", fg="white", bg="#0a2a2f", font=("Arial", 18, "bold")).pack(pady=(10, 10))
tk.Frame(scrollable_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))

btn_B_G_T = create_btn("Basic Global Thresholding", lambda: process_image("B G T"))
btn_A_T_1 = create_btn("Automatic thresholding", lambda: process_image("A T 1"))
btn_A_T_2 = create_btn("Adaptive thresholding", lambda: process_image("A T 2"))

btn_B_G_T.pack(pady=10)
btn_A_T_1.pack(pady=10)
btn_A_T_2.pack(pady=10)

tk.Label(scrollable_frame, text="More Options", fg="white", bg="#0a2a2f", font=("Arial", 14, "bold")).pack(pady=(10, 10))
tk.Frame(scrollable_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))

def clear_image():
    global original_image, displayed_image
    if original_image is None:
        messagebox.showerror("Error", "No image loaded! Please load an image first.")
        return
    original_image = None
    displayed_image = None
    original_label.config(image=None)
    original_label.image = None
    result_label.config(image=None)
    result_label.image = None

def go_back():
    subprocess.Popen(["python", "main_gui.py"])
    root.destroy()

def disable_close():
    pass

root.protocol("WM_DELETE_WINDOW", disable_close)

btn_clear_image = create_btn("Clear Image", clear_image)
btn_back = create_btn("Back", go_back)

btn_clear_image.pack(pady=10)
btn_back.pack(pady=10)
# IMAGE FRAME DISPLAY AREA
image_frame = tk.Frame(main_frame, bg="#0a2a2f", bd=2, relief="groove")
image_frame.pack(side="right", expand=True, fill="both", padx=20)


label_frame = tk.Frame(image_frame, bg="#0a2a2f")
label_frame.pack(pady=10)

title_label = tk.Label(image_frame, text="Original Image                                         Result Image",
                       fg="white", bg="#0a2a2f", font=("Arial", 16, "bold"))
title_label.pack(pady=(10,20))

images_holder = tk.Frame(image_frame, bg="#0a2a2f")
images_holder.pack(expand=True, fill="both")

images_row = tk.Frame(image_frame, bg="#0a2a2f")
images_row.pack()

original_label = tk.Label(images_holder, bg="#0a2a2f")
original_label.pack(side="left", expand=True)

result_label = tk.Label(images_holder, bg="#0a2a2f")
result_label.pack(side="left", expand=True)

def show_image(mode):
    global displayed_image
    if original_image is None:
        messagebox.showerror("Error", "No image loaded! Please load an image first.")
        return

    if mode == "original":
        img = original_image.copy().resize((500, 400))
        photo = ImageTk.PhotoImage(img)
        original_label.config(image=photo)
        original_label.image = photo
        result_label.config(image="")
        result_label.image = None

    elif mode == "displayed":
        if displayed_image is None:
            return
        img = displayed_image.copy().resize((500, 400))
        photo = ImageTk.PhotoImage(img)
        result_label.config(image=photo)
        result_label.image = photo

def process_image(mode):
    global displayed_image, noised_image

    if original_image is None:
        messagebox.showerror("Error", "No image loaded! Please load an image first.")
        return

    add_salt_and_pepper_noise = {
        "add noise sap": irs.add_salt_pepper_noise,
    }

    add_gaussian_noise = {
        "add noise g": irg.add_gaussian_noise,
    }

    salt_and_pepper_filters = {
        "average filter 1": irs.average_filter,
        "median filter": irs.median_filter,
        "an outlier method": irs.outlier_filter
    }

    gaussian_filters = {
        "image averaging": irg.image_averaging,
        "average filter 2": irg.average_filter
    }

    Segmentation = {
        "B G T": bgt.Basic_Thre,
        "A T 1": at1.Auto_Thre,
        "A T 2": at2.Adaptive_Thre
    }

    if mode in add_salt_and_pepper_noise:
        img_array = np.array(original_image)
        noised_array = add_salt_and_pepper_noise[mode](img_array)
        noised_image = Image.fromarray(noised_array)
        displayed_image = noised_image
        show_image("original")
        show_image("displayed")
        return

    if mode in add_gaussian_noise:
        img_array = np.array(original_image)
        noised_array = add_gaussian_noise[mode](img_array)
        noised_image = Image.fromarray(noised_array)
        displayed_image = noised_image
        show_image("original")
        show_image("displayed")
        return

    if mode in salt_and_pepper_filters:
        if noised_image is None or displayed_image == original_image:
            messagebox.showerror("Error", "Please add salt & pepper noise AND don't show original image before applying filters!")
            return
        img_array = np.array(noised_image)
        filtered_array = salt_and_pepper_filters[mode](img_array)
        displayed_image = Image.fromarray(filtered_array)
        show_image("original")
        show_image("displayed")
        return

    if mode in gaussian_filters:
        if noised_image is None or displayed_image == original_image:
            messagebox.showerror("Error", "Please add Gaussian noise AND don't show original image before applying filters!")
            return
        img_array = np.array(noised_image)
        filtered_array = gaussian_filters[mode](img_array)
        displayed_image = Image.fromarray(filtered_array)
        show_image("original")
        show_image("displayed")
        return

    if mode in Segmentation:
        img_array = np.array(original_image)
        filtered_array = Segmentation[mode](img_array)
        if filtered_array.dtype != np.uint8:
            filtered_array = filtered_array.astype(np.uint8)
        displayed_image = Image.fromarray(filtered_array)
        show_image("original")
        show_image("displayed")

root.mainloop()
