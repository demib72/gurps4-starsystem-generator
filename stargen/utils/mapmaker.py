"""Simple procedural world map generator."""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import cartopy.crs as ccrs
from matplotlib.colors import ListedColormap


def generate_world_map(filepath: str) -> None:
    """Generate a random world map and save it as ``filepath``.

    Parameters
    ----------
    filepath:
        Path of the PNG file to create.
    """

    # Create output directory if needed
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Set up a grid in latitude and longitude. Mercator projection typically
    # excludes the poles, so we limit latitude to about ±85°.
    n_lon = 720   # resolution in longitude
    n_lat = 340   # resolution in latitude
    lon = np.linspace(-180, 180, n_lon)
    lat = np.linspace(-85, 85, n_lat)

    # Create a random noise field and smooth it to simulate realistic continent
    # shapes.
    noise = np.random.rand(n_lat, n_lon)
    smooth_noise = gaussian_filter(noise, sigma=10)

    # Determine a threshold that yields ~55% land
    threshold = np.percentile(smooth_noise, 45)
    land_mask = smooth_noise > threshold

    # Define a custom colormap: water in blue, land in green.
    cmap = ListedColormap(['deepskyblue', 'forestgreen'])

    # Plot the world map using a Mercator projection.
    fig = plt.figure(figsize=(12, 6))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_global()
    ax.coastlines(linewidth=1)

    # Plot the land/water mask. The image is plotted in PlateCarree coordinate
    # space.
    ax.imshow(land_mask, origin='upper', extent=[-180, 180, -85, 85],
              transform=ccrs.PlateCarree(), cmap=cmap)

    ax.set_title("Example World Map (45% Water, 55% Land)")
    plt.savefig(filepath, bbox_inches="tight")
    plt.close(fig)

