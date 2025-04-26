import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

root = tk.Tk()
root.title("Main Image Processing GUI")
root.geometry("1280x800")
root.configure(bg="#0a2a2f")

image_label = None
process = None

# --- Status Bar ---
status_var = tk.StringVar()
status_bar = tk.Label(root, textvariable=status_var, bg="#123c42", fg="white", anchor="w", height=2, font=("Arial", 10))
status_bar.pack(side="bottom", fill="x")
status_var.set("Welcome to the Image Processing GUI!")

# --- Header Bar ---
header = tk.Frame(root, bg="#123c42", height=50)
header.pack(side="top", fill="x")
tk.Label(header, text="🖼️  Main Image Processing GUI", bg="#123c42", fg="white", font=("Arial", 23, "bold")).pack(padx=10, pady=5, anchor="w")

# ---About us ---
def show_about():
    about_win = tk.Toplevel(root)
    about_win.title("About")
    tk.Label(about_win, text="This application was developed as part of an\n"
        "academic project focused on advanced\n"
        "image processing techniques\nDeveloped by: Omar, Zaid, MenaAllah, Malak, Aliaa", font=("Arial", 12)).pack(padx=28, pady=25)
    tk.Button(about_win, text="Close", command=about_win.destroy).pack(pady=10)
    about_win.configure(bg="#0a2a2f")
    about_win.geometry("410x180")
    about_win.resizable(False, False)

# --- External Modules ---
def open_page(module_name):
    global process
    process = subprocess.Popen(["python", module_name + ".py"])
    root.withdraw()

# --- Exit Confirmation ---
def confirm_exit():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        if process is not None and process.poll() is None:  # Only try to terminate if process exists
            process.terminate()
        root.destroy()

# --- Button Panel ---
buttons_frame = tk.Frame(root, bg="#0a2a2f")
buttons_frame.pack(side="left", fill="y", padx=20, pady=10)

def create_button(text, command, tooltip=""):
    btn = tk.Button(buttons_frame, text=text, width=25, height=2, command=command,
                    bg="#123c42", fg="white", font=("Arial", 10, "bold"), bd=0)
    btn.pack(pady=8)
    btn.bind("<Enter>", lambda e: [btn.config(bg="lightblue", fg="black"), status_var.set(tooltip)])
    btn.bind("<Leave>", lambda e: [btn.config(bg="#123c42", fg="white"), status_var.set("Ready")])
    return btn

tk.Label(buttons_frame, text="Main Menu", fg="white", bg="#0a2a2f", font=("Arial", 18, "bold")).pack(pady=(10, 20))
tk.Frame(buttons_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))

create_button("About Us", show_about, "Learn about the developers")

tk.Label(buttons_frame, text="Filters & Operations", fg="white", bg="#0a2a2f", font=("Arial", 14, "bold")).pack(pady=(20, 10))
tk.Frame(buttons_frame, height=1, bg="#2d6b74").pack(fill="x", pady=(0, 10))

create_button("Histogram & Neighborhood", lambda: open_page("Histo_Neib_GUI"))
create_button("Restoration & Segmentation", lambda: open_page("Image Restoration & Image Segmentation Page"))
create_button("Morphology & Edge Detection", lambda: open_page("Last_Morphology_GUI"))
create_button("Point & Color Operations", lambda: open_page("PO_CIO_GUI"))

create_button("Exit", confirm_exit, "Close the application")

# --- Image Display ---
right_frame = tk.Frame(root, bg="#0a2a2f")
right_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

image_label = tk.Label(right_frame, bg="#0a2a2f")
image_label.pack(expand=True)

footer_label = tk.Label(
    root,
    text="⭐ Developed by Omar , Zaid , MenatAllah , Malak , Alyaa ⭐",  
    bg="#0a2a2f",
    fg="#b5d6d6",
    font=("Segoe UI", 11, "italic") 
)
footer_label.place(relx=0.5, rely=0.98, anchor='center')
    
# --- Placeholder image ---
try:
    icon_image = Image.open("ImageProcessing.jpg").resize((1100, 900))
    icon_photo = ImageTk.PhotoImage(icon_image)
    icon_label = tk.Label(right_frame, image=icon_photo, bg="#0a2a2f")
    icon_label.pack(pady=20)
except Exception as e:
    print("Image not found:", e)
  
root.bind("<Control-q>", lambda e: confirm_exit())
status_var = tk.StringVar()
#status_bar = tk.Label(right_frame, textvariable=status_var, bg="#123c42", fg="white", anchor="w", height=2, font=("Arial", 9))
status_bar.pack(side="bottom", fill="x")
status_bar.config(text="Welcome to the Image Processing GUI!")
root.mainloop()