import cv2 
import numpy as np
from PIL import Image 
def Subtraction (path,constant):
    img = cv2.imread(path)
    if img is None:
        raise ValueError("Image not found or path is incorrect")
    
    img = img.astype(np.int32)  # prevent overflow
    add_img =np.clip( img - constant,0,255).astype(np.uint8)
    add_img_rgb = cv2.cvtColor(add_img,cv2.COLOR_BGR2RGB)

    return Image.fromarray(add_img_rgb)   
result = Subtraction("cameraman.PNG",80)
# result.show()


########### For gui members ##############

# from PIL import ImageTk
# tk_image = ImageTk.PhotoImage(result)  # You can use it in a Label or Canvas now
# label = tk.Label(root, image=tk_image)
# label.pack()