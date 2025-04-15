# Pixel Pioneers
# Image Processing Toolbox with GUI

A Python-based GUI application for performing various image processing tasks using OpenCV, matplotlib, and Tkinter. The application allows users to apply different operations and visualize input/output results in subplots.

![GUI Demo](demo.png) <!-- Replace with actual screenshot if available -->

## Features

### 1. Point Operations
- Addition
- Subtraction
- Division

### 2. Color Image Operations
- Change lighting color (e.g., red channel adjustment)
- Swap color channels (e.g., R ↔ G)
- Eliminate color channels (e.g., remove red channel)

### 3. Image Histogram
- Histogram Stretching (grayscale images)
- Histogram Equalization (grayscale images)

### 4. Neighborhood Processing
- **Linear Filters**: Average, Laplacian
- **Non-Linear Filters**: Maximum, Minimum, Median, Mode

### 5. Image Restoration
- Salt-and-pepper noise removal using:
  - Average filter
  - Median filter
  - Outlier method

### 6. Image Segmentation
- Global Thresholding
- Automatic Thresholding
- Adaptive Thresholding

### 7. Edge Detection & Morphology
- Sobel edge detection
- Morphological operations: Dilation, Erosion, Opening
- Boundary Extraction: Internal, External, Morphological Gradient

## Requirements
- Python 3.6+
- OpenCV (`opencv-python`)
- matplotlib
- Tkinter (usually included with Python)

