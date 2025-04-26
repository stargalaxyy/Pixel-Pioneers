import numpy as np
import matplotlib.pyplot as plt

def histogram_stretching(image):
    """Optimized histogram stretching using vectorized operations"""
    # Calculate min and max in one pass
    min_val = image.min()
    max_val = image.max()
    
    # Avoid division by zero for uniform images
    if min_val == max_val:
        return np.zeros_like(image, dtype=np.uint8)
    
    # Vectorized stretching operation
    stretched = np.empty_like(image, dtype=np.float32)
    np.subtract(image, min_val, out=stretched)
    np.divide(stretched, (max_val - min_val), out=stretched)
    np.multiply(stretched, 255, out=stretched)
    
    return stretched.astype(np.uint8)

def histogram_equalization(image):
    """Optimized histogram equalization without cv2.equalizeHist"""
    # Calculate histogram (vectorized)
    hist = np.bincount(image.ravel(), minlength=256)
    
    # Calculate CDF
    cdf = hist.cumsum()
    cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
    
    # Handle case where all pixels have same value
    if cdf.max() == cdf.min():
        return image.copy()
    
    # Vectorized mapping using lookup
    equalized = np.interp(image.ravel(), np.arange(256), cdf_normalized)
    return equalized.reshape(image.shape).astype(np.uint8)

# Processing pipeline
def process_image(method="equalization", img_path="Ronaldo.jpeg"):
    # Read and convert image
    img = plt.imread(img_path)
    if img.ndim == 3:
        gray = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
    else:
        gray = img.astype(np.uint8)
    
    # Apply selected method
    if method == "stretching":
        result = histogram_stretching(gray)
    elif method == "equalization":
        result = histogram_equalization(gray)
    else:
        print("⚠ Unknown method! Showing original.")
        result = gray
    
    # Visualization
    fig, ax = plt.subplots(2, 2, figsize=(12, 8))
    titles = ["Original Image", "Original Histogram", 
              f"After {method}", "Processed Histogram"]
    
    for i, (data, cmap) in enumerate(zip(
        [gray, gray.ravel(), result, result.ravel()],
        ['gray', None, 'gray', None]
    )):
        ax.flat[i].set_title(titles[i])
        if i % 2 == 0:
            ax.flat[i].imshow(data, cmap=cmap)
            ax.flat[i].axis('off')
        else:
            ax.flat[i].hist(data, bins=256, range=(0, 256))