import json


def serialize_orbit_content(oc):
    data = {
        "class": oc.__class__.__name__,
        "name": getattr(oc, "name", ""),
        "orbit": oc.get_orbit() if hasattr(oc, "get_orbit") else None,
        "period": oc.get_period() if hasattr(oc, "get_period") else None,
        "eccentricity": oc.get_eccentricity() if hasattr(oc, "get_eccentricity") else None,
    }
    if hasattr(oc, "get_type"):
        data["type"] = oc.get_type()
    elif hasattr(oc, "type"):
        data["type"] = oc.type()
    if hasattr(oc, "get_size"):
        data["size"] = oc.get_size()
    if hasattr(oc, "get_mass"):
        try:
            data["mass"] = oc.get_mass()
        except Exception:
            pass
    if hasattr(oc, "num_moons"):
        data["moons"] = oc.num_moons()
    if hasattr(oc, "num_moonlets"):
        data["moonlets"] = oc.num_moonlets()
    if hasattr(oc, "get_hydrographic_cover"):
        data["hydrographic_cover"] = oc.get_hydrographic_cover()
    return data


def serialize_planet_system(ps):
    return {
        "gasarrangement": getattr(ps, "gasarrangement", None),
        "first_gas_orbit": getattr(ps, "firstgasorbit", None),
        "orbits": getattr(ps, "orbitarray", []),
        "orbitcontents": {str(k): serialize_orbit_content(v) for k, v in getattr(ps, "orbitcontents", {}).items()},
    }


def serialize_star(star):
    data = {
        "letter": star.get_letter() if hasattr(star, "get_letter") else None,
        "mass": star.get_mass() if hasattr(star, "get_mass") else None,
        "sequence": star.get_sequence() if hasattr(star, "get_sequence") else None,
        "temperature": star.get_temp() if hasattr(star, "get_temp") else None,
        "luminosity": star.get_luminosity() if hasattr(star, "get_luminosity") else None,
        "radius": star.get_radius() if hasattr(star, "get_radius") else None,
        "age": star.get_age() if hasattr(star, "get_age") else None,
        "orbit_limits": star.get_orbit_limits() if hasattr(star, "get_orbit_limits") else None,
        "snowline": star.get_snowline() if hasattr(star, "get_snowline") else None,
    }
    if hasattr(star, "has_forbidden_zone") and star.has_forbidden_zone():
        data["forbidden_zone"] = star.get_forbidden_zone()
    if hasattr(star, "planetsystem") and star.planetsystem is not None:
        data["planetsystem"] = serialize_planet_system(star.planetsystem)
    return data


def serialize_star_system(system):
    return {
        "age": system.get_age() if hasattr(system, "get_age") else None,
        "open_cluster": system.is_open_cluster() if hasattr(system, "is_open_cluster") else None,
        "orbits": system.get_orbits() if hasattr(system, "get_orbits") else None,
        "periods": system.get_period() if hasattr(system, "get_period") else None,
        "stars": [serialize_star(s) for s in getattr(system, "stars", [])],
    }


def dump_json(system, path):
    with open(path, "w") as f:
        json.dump(serialize_star_system(system), f, indent=2)

