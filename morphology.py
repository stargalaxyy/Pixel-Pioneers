import numpy as np


# Morphology is a broad set of image processing operations that process binary (black and white) images based on shapes.


def get_mask():
    return np.ones((3, 3), dtype=np.uint8)


def dilate(image: np.ndarray) -> np.ndarray:
    """enlarge white parts of image"""
    # Apply zero padding to the edge pixels in picture
    padded = np.pad(image, 1, mode='constant', constant_values=0)
    print(image)
    
    # Return an array of zeros with the same shape and type as original image.
    output = np.zeros_like(image)
    mask = get_mask()

    # Loop pixel by pixel
    for i in range(image.shape[0]): # Loop over rows
        for j in range(image.shape[1]): # Loop over columns
            niegbourhood = padded[i:i + 3, j:j + 3] # Get the 3x3 niegbourhood around the pixel
            if np.any(niegbourhood * mask): # If any of the niegbourhood pixels are 1 set pixel to white
                output[i, j] = 255
    return output


def erode(image: np.ndarray) -> np.ndarray:
    """"shrink white parts of image"""
    # Very similar to dilate except that here we wet the pixel to 255 (white) only if all neighbourhood pixels are white.
    padded = np.pad(image, 1, mode='constant', constant_values=0)
 
    output = np.zeros_like(image)
    mask = get_mask()

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            niegbourhood = padded[i:i + 3, j:j + 3]
            if np.all(niegbourhood * mask == 255): # If all of the niegbourhood pixels are 1 set pixel to white
                output[i, j] = 255
    return output


def opening(image: np.ndarray) -> np.ndarray:
    # Erosion followed by dilation is called "opening". removes extra black noise after removing white noise.
    return dilate(erode(image))


def internal_boundary(image: np.ndarray) -> np.ndarray:
    # removes salt & pepper noise
    """    
            --consists of those pixel in img which are at its edge .
            --since erosion makes the white areas in an image smaller,
            subtracting the erosion from the original image will show the 
            pixels that were removed by erosion. (i-Erosion[i])
            
            --this is called the "internal boundary" of the image.
    """
    return image - erode(image)


def external_boundary(image: np.ndarray) -> np.ndarray:
    """ 
            -- consist of pixels outside img which are just next to it.
            --since dilation makes the white areas in an image larger,
            subtracting the original image from the dilation will show the
            pixels that were added by dilation. (i-Dilation[i, matrixof1s])
            --this is called the "external boundary" of the image.
    """
    return dilate(image) - image


def morphological_gradient(image: np.ndarray) -> np.ndarray:
    """combination of both the internal and external boundaries.  """
    return dilate(image) - erode(image)