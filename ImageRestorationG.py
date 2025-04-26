import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view

# --------------------------------------
# 1. Optimized Gaussian Noise Addition
# --------------------------------------
def add_gaussian_noise(image, mean=0, sigma=25):
    """Vectorized Gaussian noise addition"""
    noisy = image.astype(np.float32) + np.random.normal(mean, sigma, image.shape)
    return np.clip(noisy, 0, 255).astype(np.uint8)

# --------------------------------------
# 2. Optimized Image Averaging
# --------------------------------------
def image_averaging(image, num_images=5):
    """Vectorized image averaging using pre-allocation"""
    # Pre-allocate array for all noisy images
    noisy_stack = np.zeros((num_images, *image.shape), dtype=np.float32)
    
    # Generate all noisy images at once
    for i in range(num_images):
        noisy_stack[i] = add_gaussian_noise(image)
    
    # Compute mean along the stack axis
    return np.mean(noisy_stack, axis=0).astype(np.uint8)

# --------------------------------------
# 3. Optimized Average Filter
# --------------------------------------
def average_filter(image, k=3):
    """Vectorized average filter using sliding window"""
    if k % 2 == 0:
        raise ValueError("Kernel size must be odd")
    
    pad = k // 2
    padded = np.pad(image, pad, mode='reflect')  # Better than constant padding
    
    # Use sliding window view for vectorized operations
    windows = sliding_window_view(padded, (k, k))
    return np.mean(windows, axis=(2, 3)).astype(image.dtype)