import elevation
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os

# Define the area of interest (e.g., around Rome, Italy)
bounds = (12.35, 41.8, 12.65, 42.0)

# Download the DEM data
output_file = 'rome_dem.tif'
elevation.clip(bounds=bounds, output=output_file)
full_path = os.path.join(elevation.CACHE_DIR, 'STRM1', output_file)
print(f"DEM file was written to: {full_path}")

# Open the DEM file
with rasterio.open(full_path) as src:
    # Read the elevation data
    elevation_data = src.read(1)
    
    # Get the metadata
    meta = src.meta

exit(1)

# Visualize the DEM
fig, ax = plt.subplots(figsize=(10, 10))
im = ax.imshow(elevation_data, cmap='terrain')
plt.colorbar(im, label='Elevation (m)')
plt.title('DEM of Rome')
plt.show()

# Calculate and visualize the slope
from rasterio.enums import Resampling

with rasterio.open('rome_dem.tif') as src:
    elevation = src.read(1)
    
    # Calculate slope
    dx, dy = np.gradient(elevation)
    slope = np.degrees(np.arctan(np.sqrt(dx*dx + dy*dy)))

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(slope, cmap='viridis')
    plt.colorbar(im, label='Slope (degrees)')
    plt.title('Slope Map of Rome')
    plt.show()

