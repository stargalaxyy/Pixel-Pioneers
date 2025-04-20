import  cv2
import numpy as np
from PIL import Image 
def Basic_Thre(path):
    img = cv2.imread(path,0)
    image = (img > 130).astype(np.uint8) * 255  # Convert to 0 or 255
    return Image.fromarray(image)



############ for gui members ################
# from PIL import ImageTk

# result = Basic_Thre('segmentation.PNG')
# tk_image = ImageTk.PhotoImage(result)  # You can use it in a Label or Canvas now

# label = tk.Label(root, image=tk_image)
# label.pack()


# testing output of function

# thresholded_image = Basic_Thre('segmentation.PNG')
# thresholded_image.show()  # This will display the binary image using PIL

