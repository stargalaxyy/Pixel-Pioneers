import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def add_salt_pepper_noise(image, amount=0.1):
    """Add salt and pepper noise to an image with optimized implementation"""
    noisy = image.copy()
    total_pixels = image.size
    num_salt_pepper = int(np.ceil(amount * total_pixels))
    
    # Generate random coordinates
    coords = np.random.choice(total_pixels, num_salt_pepper * 2, replace=False)
    salt_coords = coords[:num_salt_pepper]
    pepper_coords = coords[num_salt_pepper:]
    
    # Apply salt and pepper using flat indices
    noisy.flat[salt_coords] = 255
    noisy.flat[pepper_coords] = 0
    
    return noisy

def average_filter(image, k=3):
    """Optimized average filter using sliding window view"""
    if k % 2 == 0:
        raise ValueError("Kernel size k must be odd")
    
    pad = k // 2
    padded = np.pad(image, pad, mode='edge')  # Edge padding works better than zero padding
    
    # Create sliding window view
    windows = sliding_window_view(padded, (k, k))
    
    # Calculate mean along last two axes
    return np.mean(windows, axis=(2, 3)).astype(image.dtype)

def median_filter(image, k=3):
    """Optimized median filter using sliding window view"""
    if k % 2 == 0:
        raise ValueError("Kernel size k must be odd")
    
    pad = k // 2
    padded = np.pad(image, pad, mode='edge')
    
    # Create sliding window view
    windows = sliding_window_view(padded, (k, k))
    
    # Calculate median along last two axes
    return np.median(windows, axis=(2, 3)).astype(image.dtype)

def outlier_filter(image, k=3, threshold=40):
    """Optimized outlier filter with distinct implementation"""
    if k % 2 == 0:
        raise ValueError("Kernel size k must be odd")
    
    pad = k // 2
    padded = np.pad(image, pad, mode='edge')
    output = image.copy()
    
    # Create sliding window view
    windows = sliding_window_view(padded, (k, k))
    
    # Reshape to separate center pixel from neighbors
    windows_reshaped = windows.reshape(*image.shape, k*k)
    centers = windows_reshaped[..., k*k//2]
    neighbors = np.delete(windows_reshaped, k*k//2, axis=-1)
    
    # Calculate median of neighbors
    neighbor_medians = np.median(neighbors, axis=-1)
    
    # Apply replacement condition
    mask = np.abs(centers - neighbor_medians) > threshold
    output[mask] = neighbor_medians[mask]
    
    return output