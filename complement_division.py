import numpy as np

def img_complement(image: np.ndarray) -> np.ndarray:
    height, width = image.shape
    complemented_img = np.zeros((height,width), dtype=np.uint8)
    
    for i in range(height):
        for j in range(width):
            val = 255 - image[i,j]
            if val > 255:
                complemented_img[i,j] = 255
            elif val < 0:
                complemented_img[i,j] = 0
            else:
                complemented_img[i,j] = val

    
    return complemented_img


def img_divide(image: np.ndarray, n:float) -> np.ndarray:
    height, width = image.shape
    divided_img = np.zeros((height,width), dtype=np.uint8)
    
    for i in range(height):
        for j in range(width):
            val = int(image[i,j] / n)
            if val > 255:
                divided_img[i,j] = 255
            elif val < 0:
                divided_img[i,j] = 0
            else:
                divided_img[i,j] = val
            