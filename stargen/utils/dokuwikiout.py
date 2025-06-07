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
            "====== CAS: Computer-Assisted Starsystem ======\n\n"
            "===== Summary =====\n"
            "=== General Description ===\n\n"
            "=== GM Notes ===\n\n"
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
        lines = []
        oc = planetsystem.get_orbitcontents()
        for skey in sorted(oc):
            body = oc[skey]
            if body.type() != "Terrestrial":
                continue
            lines.append(f"==== {body.get_name()} ====\n")
            lines.append(f"**Type:** {body.get_type()}\n\n")
            header = "|^Property^Value^|\n"
            lines.append(header)
            lines.append(f"|Pressure|{body.get_pressure():.2f} atm, {body.get_pressure_category()}|\n")
            lines.append(f"|Hydrographic Coverage|{body.get_hydrographic_cover()} %|\n")
            atcomp = body.atmcomp
            atkeys = [key for key in atcomp.keys() if atcomp[key] is True]
            abbr = ", ".join(AtmCompAbbr[k] for k in atkeys)
            lines.append(f"|Atmospheric Composition|{abbr}|\n")
            lines.append("\n")
        return "".join(lines)
