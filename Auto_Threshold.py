import cv2
import numpy as np
from PIL import Image

def Auto_Thre(path):
    img = cv2.imread(path, 0)  # Read the image in grayscale
    Theta = np.mean(img)
    done = False  
    while not done:
        p1_mask = img >= Theta
        p2_mask = ~p1_mask
        # Get the foreground and background pixel values
        p1 = img[p1_mask]
        p2 = img[p2_mask]
        m1 = np.mean(p1)
        m2 = np.mean(p2)
        Th_next = 0.5 * (m1 + m2)
        done = abs(Theta - Th_next) < 0.5  # Check for convergence
        Theta = Th_next
    im_thr = np.where(img >= Theta, 255, 0).astype(np.uint8)
    return Image.fromarray(im_thr)

############ for gui members ################
# from PIL import ImageTk

# result = Auto_Thre('segmentation.PNG')
# tk_image = ImageTk.PhotoImage(result)  # You can use it in a Label or Canvas now

# label = tk.Label(root, image=tk_image)
# label.pack()




# testing output of function

# thresholded_image = Auto_Thre('segmentation.PNG')
# thresholded_image.show()  # This will display the binary image using PIL


