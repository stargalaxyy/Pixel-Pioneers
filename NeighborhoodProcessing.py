import numpy as np

def average_filter(image, k=3):
    """Optimized average filter using vectorized operations"""
    kernel = np.ones((k, k), dtype=np.float32) / (k * k)
    pad = k // 2
    padded = np.pad(image, pad, mode='reflect')
    
    # Vectorized implementation
    output = np.zeros_like(image, dtype=np.float32)
    for i in range(k):
        for j in range(k):
            output += padded[i:i+image.shape[0], j:j+image.shape[1]] * kernel[i,j]
    
    return np.clip(output, 0, 255).astype(np.uint8)

def laplacian_filter(image):
    """Optimized Laplacian filter using vectorized operations"""
    kernel = np.array([[-1, -1, -1],
                      [-1, 8, -1],
                      [-1, -1, -1]], dtype=np.float32)
    
    pad = 1
    padded = np.pad(image, pad, mode='reflect')
    output = np.zeros_like(image, dtype=np.float32)
    
    # Vectorized implementation
    for i in range(3):
        for j in range(3):
            output += padded[i:i+image.shape[0], j:j+image.shape[1]] * kernel[i,j]
    
    # Normalize and clip
    output = np.clip(output + 128, 0, 255)
    return output.astype(np.uint8)

def min_filter(image, k=3):
    """Optimized minimum filter using sliding window view"""
    pad = k // 2
    padded = np.pad(image, pad, mode='reflect')
    
    # Create sliding window view
    shape = (image.shape[0], image.shape[1], k, k)
    strides = padded.strides + padded.strides
    windows = np.lib.stride_tricks.as_strided(padded, shape=shape, strides=strides)
    
    return np.min(windows, axis=(2,3)).astype(np.uint8)

def max_filter(image, k=3):
    """Optimized maximum filter using sliding window view"""
    pad = k // 2
    padded = np.pad(image, pad, mode='reflect')
    
    # Create sliding window view
    shape = (image.shape[0], image.shape[1], k, k)
    strides = padded.strides + padded.strides
    windows = np.lib.stride_tricks.as_strided(padded, shape=shape, strides=strides)
    
    return np.max(windows, axis=(2,3)).astype(np.uint8)

def median_filter(image, k=3):
    """Optimized median filter using sliding window view"""
    pad = k // 2
    padded = np.pad(image, pad, mode='reflect')
    
    # Create sliding window view
    shape = (image.shape[0], image.shape[1], k, k)
    strides = padded.strides + padded.strides
    windows = np.lib.stride_tricks.as_strided(padded, shape=shape, strides=strides)
    
    # Reshape for vectorized median calculation
    windows_flat = windows.reshape(-1, k*k)
    return np.median(windows_flat, axis=1).reshape(image.shape).astype(np.uint8)

def mode_filter(image, k=3):
    """Optimized mode filter using bincount"""
    pad = k // 2
    padded = np.pad(image, pad, mode='reflect')
    
    # Create sliding window view
    shape = (image.shape[0], image.shape[1], k, k)
    strides = padded.strides + padded.strides
    windows = np.lib.stride_tricks.as_strided(padded, shape=shape, strides=strides)
    
    # Reshape for vectorized mode calculation
    windows_flat = windows.reshape(-1, k*k)
    
    # Vectorized mode calculation using bincount
    output = np.zeros(windows_flat.shape[0], dtype=np.uint8)
    for i in range(windows_flat.shape[0]):
        counts = np.bincount(windows_flat[i])
        output[i] = np.argmax(counts)
    
    return output.reshape(image.shape)