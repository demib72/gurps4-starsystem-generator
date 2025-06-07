import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def _prepare_draw_data(star):
    """Extract orbit information from a Star object."""
    data = []
    oc_dict = star.planetsystem.get_orbitcontents()
    for oc in oc_dict.values():
        min_r, max_r = oc.get_min_max()
        data.append({
            'min': min_r,
            'max': max_r,
            'orbital_period': oc.get_period(),
            'name': oc.get_name(),
            'velocity': 0,
            'position': 0,
            'rotation': np.random.uniform(0, 2 * np.pi),
        })
    return data


def render_star_gif(star, filepath, frames=360):
    """Render a simple planetary animation for a single star."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    bodies = _prepare_draw_data(star)

    max_size = max(body['max'] for body in bodies)
    scale = 600 / max_size if max_size else 1

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    orbits = []
    planets = []
    for body in bodies:
        semi_major = (body['max'] + body['min']) / 2 * scale
        ecc = (body['max'] - body['min']) / (body['max'] + body['min'])
        rot = body['rotation']
        th = np.linspace(0, 2 * np.pi, 361)
        x = semi_major * (np.cos(th) - ecc)
        y = semi_major * np.sqrt(1 - ecc ** 2) * np.sin(th)
        xr = x * np.cos(rot) - y * np.sin(rot)
        yr = y * np.cos(rot) + x * np.sin(rot)
        line, = ax.plot(xr, yr, lw=0.5, color='black')
        orbits.append(line)
        planet, = ax.plot([], [], 'bo', ms=3)
        planets.append(planet)
        body['semi_major'] = semi_major
        body['ecc'] = ecc

    star_plot, = ax.plot(0, 0, 'yo', ms=6)

    def update(_):
        artists = []
        for idx, body in enumerate(bodies):
            ecc = body['ecc']
            semi_major = body['semi_major']
            rot = body['rotation']
            # solve Kepler equation
            M = body['position']
            E = M + ecc * np.sin(M)
            while True:
                dE = (E - ecc * np.sin(E) - M) / (1 - ecc * np.cos(E))
                E -= dE
                if abs(dE) < 1e-6:
                    break
            xi = semi_major * (np.cos(E) - ecc)
            yi = semi_major * np.sqrt(1 - ecc ** 2) * np.sin(E)
            x = xi * np.cos(rot) - yi * np.sin(rot)
            y = yi * np.cos(rot) + xi * np.sin(rot)
            planets[idx].set_data([x], [y])
            artists.append(planets[idx])
            vel = (2 * np.pi) / body['orbital_period']
            if body['position'] < 2 * np.pi - vel:
                body['position'] += vel
            else:
                body['position'] = 0
        artists.extend(orbits)
        artists.append(star_plot)
        return artists

    ani = FuncAnimation(fig, update, frames=frames, interval=40, blit=True)
    writer = PillowWriter(fps=25)
    ani.save(filepath, writer=writer)
    plt.close(fig)


def render_system_gif(star_system, filepath='gifs/system.gif', frames=360):
    """Render GIFs for each star in the system.

    ``filepath`` acts as a base name; the star letter is appended before the
    file extension.
    """
    base, ext = os.path.splitext(filepath)
    for star in star_system.stars:
        letter = getattr(star, 'letter', 'A')
        star_path = f"{base}_{letter}{ext}"
        render_star_gif(star, star_path, frames=frames)


