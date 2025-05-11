# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 01:11:33 2025

@author: natha
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Define file paths
file_paths = [
    r"filepath"
]

dataset_labels = [
    "Niobium 150ss - piece 1",
    "Niobium 150ss - piece 2",
    "Niobium 150ss - piece 3",
    "Niobium 150ss - piece 4",
    "Niobium 150ss - piece 5"
]

# Function to read and clean data
def read_data(file_path):
    numeric_data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 2:  # Ensure two columns
                try:
                    numeric_data.append([float(parts[0]), float(parts[1])])
                except ValueError:
                    continue
    numeric_data = np.array(numeric_data)
    return numeric_data

# Read all datasets
all_numeric_data = [read_data(path) for path in file_paths]
all_numeric_data = [data for data in all_numeric_data if data.size > 0]

if not all_numeric_data:
    print("No valid datasets found!")
    exit()

# Plotting
plt.figure(figsize=(10, 6))

for idx, data in enumerate(all_numeric_data):
    x, y = data[:, 0], data[:, 1]
    
    # Remove zero or negative values (avoid log errors)
    y = np.where(y > 0, y, np.min(y[y > 0]) * 1e-3)

    # Apply Savitzky-Golay filter for smoothing (window=15, polyorder=2)
    y_smooth = savgol_filter(y, window_length=15, polyorder=2, mode='interp')

    # Apply logarithmic offset
    y_offset = y_smooth * (100 ** idx)  

    plt.plot(x, y_offset, label=dataset_labels[idx], alpha=0.8)

plt.xlabel("Incident Angle (°)")
plt.ylabel("Intensity (a.u.)")
plt.title("XRR Data - Niobium Uniformity (Cleaned)")
plt.yscale("log")
plt.xscale("linear")

plt.legend()
plt.grid(True)
plt.show()
