import cv2
import numpy as np
from PIL import Image 

def sobel_detector(path):
    img = cv2.imread(path, 0).astype(np.float32)
    rows,cols = img.shape  # rows(height)  cols(width)
    Gx = np.array([[-1, 0, 1],
               [-2, 0, 2],
               [-1, 0, 1]])

    Gy = np.array([[-1, -2, -1],
               [ 0,  0,  0],
               [ 1,  2,  1]])
    output = np.zeros_like(img)

    for i in range(1,rows-1):
        for j in range(1,cols-1):
            region = img[i-1:i+2,j-1:j+2]
            gx = np.sum(Gx * region)
            gy = np.sum(Gy * region)
            grad = np.sqrt(gx**2 + gy**2)
            output[i, j] = min(255, grad)  # Makes sure the pixel value doesn’t exceed 255

    return Image.fromarray(output)

############ for gui members ################
# from PIL import ImageTk

# result = sobel_detector('cameraman.PNG')
# tk_image = ImageTk.PhotoImage(result)  # You can use it in a Label or Canvas now


# testing output of function
# x=sobel_detector("cameraman.PNG")
# x.show()

