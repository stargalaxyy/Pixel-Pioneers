import cv2
import numpy as np
from PIL import Image

def Adaptive_Thre(path):
    img= cv2.imread(path,0) 
    p1=img[:,1:64]
    p2=img[:,65:128]
    p3=img[:,129:192]
    p4=img[:,193:256]
    [T1 ,im_th1] = cv2.threshold(p1,0,255,cv2.THRESH_OTSU)
    [T2 ,im_th2] = cv2.threshold(p2,0,255,cv2.THRESH_OTSU)
    [T3 ,im_th3] = cv2.threshold(p3,0,255,cv2.THRESH_OTSU)
    [T4 ,im_th4] = cv2.threshold(p4,0,255,cv2.THRESH_OTSU)
    image=np.concatenate((im_th1,im_th2,im_th3,im_th4) ,axis=1)
    return Image.fromarray(image)

############ for gui members ################
# from PIL import ImageTk

# result = Adaptive_Thre('segmentation.PNG')
# tk_image = ImageTk.PhotoImage(result)  # You can use it in a Label or Canvas now

# label = tk.Label(root, image=tk_image)
# label.pack()


# testing output of function

# thresholded_image=Adaptive_Thre("segmentation.PNG")
# thresholded_image.show()  # This will display the binary image using PIL
