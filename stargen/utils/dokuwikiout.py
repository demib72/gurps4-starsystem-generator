"""dokuwikiout.py

Module for saving a StarSystem to a Dokuwiki formatted text file.
"""

import os
from ..data.tables import AtmCompAbbr


class DokuwikiWriter:
    def __init__(self, starsystem, filename="starsystem.txt"):
        self.starsystem = starsystem
        self.filename = filename

    def write(self):
        os.makedirs("text", exist_ok=True)
        filepath = f"text/{self.filename}"
        with open(filepath, "w") as file:
            file.write(self.title())
            file.write(self.starsystemprop())
            file.write(self.starprop())
            file.write(self.overviews())
            for star in self.starsystem.stars:
                file.write(self.psdetails(star.planetsystem))

    def title(self):
        return (
            "====== Starsystem Title ======\n\n"
            "===== History =====\n"
            "=== Description ===\n\n"
        )

    def starsystemprop(self):
        lines = ["===== The Star System =====\n", "==== Star System Properties ====\n"]
        numstar = len(self.starsystem.stars)
        lines.append(f"* Number of stars: {numstar}\n")
        age = self.starsystem.get_age()
        lines.append(f"* Stellar age: {age} billion years\n\n")
        if numstar > 1:
            header = "|^Property^" + "^".join([f"Pair A--{chr(66+i)}" for i in range(numstar-1)]) + "^|\n"
            lines.append(header)
            orbits = self.starsystem.get_orbits()
            row = "|Orbital Separation [AU]"
            for o, _ in orbits:
                row += f"|{o:.2f}"
            lines.append(row + "|\n")
            row = "|Orbital Eccentricity"
            for _, e in orbits:
                row += f"|{e:.2f}"
            lines.append(row + "|\n")
            row = "|Orbital Period [d]"
            for p in self.starsystem.get_period():
                row += f"|{p:.1f}"
            lines.append(row + "|\n\n")
        return "".join(lines)

    def starprop(self):
        numstar = len(self.starsystem.stars)
        header = "|^Property^" + "^".join([f"Star {s.get_letter()}" for s in self.starsystem.stars]) + "^|\n"
        lines = ["==== Star Properties ====\n", header]
        props = {
            "Sequence": lambda s: s.get_sequence(),
            "Mass": lambda s: f"{s.get_mass():.2f}",
            "Temperature": lambda s: f"{s.get_temp():.0f}",
            "Luminosity": lambda s: f"{s.get_luminosity():.4f}",
            "Radius": lambda s: f"{s.get_radius():.5f}",
            "Inner Limit": lambda s: f"{s.get_orbit_limits()[0]:.2f}",
            "Outer Limit": lambda s: f"{s.get_orbit_limits()[1]:.1f}",
            "Snow line": lambda s: f"{s.get_snowline():.2f}",
        }
        if numstar > 1:
            props["FZ Inner"] = lambda s: f"{s.get_forbidden_zone()[0]:.1f}"
            props["FZ Outer"] = lambda s: f"{s.get_forbidden_zone()[1]:.1f}"
        for title, func in props.items():
            row = f"|{title}"
            for star in self.starsystem.stars:
                row += f"|{func(star)}"
            lines.append(row + "|\n")
        lines.append("\n")
        return "".join(lines)

    def overviews(self):
        lines = []
        for star in self.starsystem.stars:
            lettr = star.get_letter()
            ps = star.planetsystem
            oc = ps.get_orbitcontents()
            lines.append(f"==== Overview -- Planet System {lettr} ====\n")
            lines.append("=== Summary ===\n\n")
            lines.append("=== Description ===\n\n")
            lines.append("=== GM Notes ===\n\n")
            header = (
                "|^Name^Type^Size^World^R_orb [AU]^Period [yr]^Ecc.^R_min [AU]^R_max [AU]^Moons^Moonlets^T_BB [K]^|\n"
            )
            lines.append(header)
            for skey in sorted(oc):
                body = oc[skey]
                row = (
                    f"|{body.get_name()}|{body.type()}|{body.get_size()}|{getattr(body, 'get_type', lambda: '')()}"
                )
                row += f"|{body.get_orbit():.2f}|{body.get_period():.2f}|{body.get_eccentricity():.2f}"
                mn, mx = body.get_min_max()
                row += f"|{mn:.2f}|{mx:.2f}|"
                row += f"{body.num_moons() or ''}|{body.num_moonlets() or ''}|{body.get_blackbody_temp():.0f}|\n"
                lines.append(row)
            lines.append("\n")
        return "".join(lines)

    def psdetails(self, planetsystem):
        """Return formatted details of all bodies in a planet system."""
        lines = []
        oc = planetsystem.get_orbitcontents()
        for skey in sorted(oc):
            body = oc[skey]
            btype = body.type()
            if btype == "Terrestrial":
                lines.append(self.planetdetails(body))
            elif btype == "Gas Giant":
                lines.append(self.gasgiantdetails(body))
        return "".join(lines)

    def planetdetails(self, planet):
        """Return dokuwiki table with details about a terrestrial planet."""
        lines = [f"==== {planet.get_name()} ====\n"]
        lines.append("|^Property^Value^|\n")
        lines.append(f"|Type|{planet.get_type()}|\n")
        atkeys = [key for key in planet.atmcomp.keys() if planet.atmcomp[key]]
        abbr = ", ".join(AtmCompAbbr[k] for k in atkeys)
        if abbr:
            lines.append(f"|Atmospheric Composition|{abbr}|\n")
        if planet.get_pressure() == 0:
            lines.append("|Pressure|None|\n")
        else:
            lines.append(
                f"|Pressure|{planet.get_pressure():.2f} atm, {planet.get_pressure_category()}|\n"
            )
        lines.append(
            f"|Hydrographic Coverage|{planet.get_hydrographic_cover():.0f} %|\n"
        )
        lines.append(
            f"|Average Surface Temp|{planet.get_average_surface_temp():.1f} K|\n"
        )
        lines.append(f"|Climate Type|{planet.get_climate()}|\n")
        lines.append(
            f"|Diameter|{planet.get_diameter():.3f} Earth Diameters|\n"
        )
        lines.append(f"|Surface Gravity|{planet.get_gravity():.2f} G|\n")
        lines.append(f"|Affinity|{planet.get_affinity():+d}|\n")
        if planet.num_moons() > 0:
            lines.append(f"|Moons|{planet.num_moons()}|\n")
        if planet.num_moonlets() > 0:
            lines.append(f"|Moonlets|{planet.num_moonlets()}|\n")
        lines.append("\n")
        if planet.num_moons() > 0:
            for m in planet.get_satellites():
                lines.append(self.moondetails(m))
        return "".join(lines)

    def gasgiantdetails(self, gasgiant):
        """Return dokuwiki table with details about a gas giant."""
        lines = [f"==== {gasgiant.get_name()} ====\n"]
        lines.append("|^Property^Value^|\n")
        lines.append("|Type|Gas Giant|\n")
        lines.append(f"|Mass|{gasgiant.get_mass()} Earth Masses|\n")
        lines.append(f"|Density|{gasgiant.get_density()} Earth Densities|\n")
        lines.append(
            f"|Diameter|{gasgiant.get_diameter():.2f} Earth Diameters|\n"
        )
        lines.append(
            f"|Cloud-Top Gravity|{gasgiant.get_gravity():.2f} G|\n"
        )
        lines.append(
            f"|Satellites 1st Family|{len(gasgiant.get_first_family())}|\n"
        )
        lines.append(
            f"|Satellites 2nd Family|{len(gasgiant.get_moons())}|\n"
        )
        lines.append(
            f"|Satellites 3rd Family|{len(gasgiant.get_third_family())}|\n"
        )
        lines.append("\n")
        for m in gasgiant.get_moons():
            lines.append(self.moondetails(m))
        return "".join(lines)

    def moondetails(self, moon):
        """Return dokuwiki table with details about a moon."""
        lines = [f"=== Moon {moon.get_name()} ===\n"]
        lines.append("|^Property^Value^|\n")
        lines.append(f"|Type|{moon.get_size()} ({moon.get_type()})|\n")
        atkeys = [key for key in moon.atmcomp.keys() if moon.atmcomp[key]]
        abbr = ", ".join(AtmCompAbbr[k] for k in atkeys)
        if abbr:
            lines.append(f"|Atm. Comp.|{abbr}|\n")
        if moon.get_pressure() == 0:
            lines.append("|Pressure|None|\n")
        else:
            lines.append(
                f"|Pressure|{moon.get_pressure():.2f} atm, {moon.get_pressure_category()}|\n"
            )
        lines.append(
            f"|Hydrographic Coverage|{moon.get_hydrographic_cover():.0f} %|\n"
        )
        lines.append(
            f"|Average Surface Temp|{moon.get_average_surface_temp():.1f} K|\n"
        )
        lines.append(f"|Climate Type|{moon.get_climate()}|\n")
        lines.append(
            f"|Diameter|{moon.get_diameter():.3f} Earth Diameters|\n"
        )
        lines.append(f"|Surface Gravity|{moon.get_gravity():.2f} G|\n")
        lines.append(f"|Affinity|{moon.get_affinity():+d}|\n")
        lines.append("\n")
        return "".join(lines)
