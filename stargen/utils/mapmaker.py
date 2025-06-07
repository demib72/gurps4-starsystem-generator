import os
import numpy as np
import matplotlib.pyplot as plt
from opensimplex import OpenSimplex

def generate_world_map(filepath: str, hydrographic_cover: int) -> None:
    """Generate a procedural world map with given water coverage and save it as a PNG."""

    # === Settings ===
    width, height = 1024, 512
    scale = 150.0
    seed = 42
    tmp = OpenSimplex(seed)
    
    # === Create elevation map using OpenSimplex noise ===
    elevation = np.zeros((height, width), dtype=np.float32)

    for y in range(height):
        for x in range(width):
            nx = x / scale
            ny = y / scale
            elevation[y, x] = tmp.noise2(nx, ny)

    # Normalize elevation to 0.0–1.0
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())

    # === Apply hydrographic cover: determine sea level threshold ===
    sea_level = np.percentile(elevation, hydrographic_cover)
    land_mask = elevation > sea_level

    # === Create RGB image (blue ocean, terrain-colored land) ===
    color_map = np.zeros((height, width, 3), dtype=np.float32)

    # Ocean: blue
    color_map[~land_mask] = [0.2, 0.6, 1.0]

    # Land: use matplotlib terrain colormap
    terrain_colors = plt.get_cmap("terrain")(elevation)
    color_map[land_mask] = terrain_colors[land_mask, :3]

    # === Save image ===
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    plt.imsave(filepath, color_map)

