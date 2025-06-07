import argparse
from stargen import StarSystem
from stargen.utils.latexout import LatexWriter
from stargen.utils.dokuwikiout import DokuwikiWriter
from stargen.utils.random_name import generate_random_name

def main(args=None):
    try:
        from stargen.utils.gifout import render_system_gif
    except ImportError:
        render_system_gif = None

    try:
        from stargen.utils.mapmaker import generate_world_map
    except ImportError:
        generate_world_map = None

    parser = argparse.ArgumentParser(description="Generate a random star system")
    parser.add_argument(
        "--format",
        choices=["latex", "dokuwiki"],
        default="latex",
        help="Output format",
    )
    if args is None:
        args = []
    parsed = parser.parse_args(args)

    name = generate_random_name()
    if parsed.format == "dokuwiki":
        filename = f"{name}.txt"
        writer_cls = DokuwikiWriter
    else:
        filename = f"{name}.tex"
        writer_cls = LatexWriter

    star_system = StarSystem()
    writer = writer_cls(star_system, filename)

    star_system.print_info()
    writer.write()

    system_gif = input("Do you want a gif of the system? [Y/N]: ")
    world_map = input("Do you want a map of the garden world(s)? [Y/N]: ")

    if system_gif.lower() == 'y' and render_system_gif:
        render_system_gif(star_system, f"gifs/{name}.gif")
    elif system_gif.lower() == 'y':
        print("GIF generation skipped: missing dependencies")

    if world_map.lower() == 'y' and generate_world_map:
        for star in star_system.stars:
            oc_dict = star.planetsystem.get_orbitcontents()
            for oc in oc_dict.values():
                if hasattr(oc, 'get_type') and oc.get_type() == 'Garden':
                    hydro = oc.get_hydrographic_cover()
                    generate_world_map(
                        f"maps/{name}_{oc.get_name()}.png",
                        hydro,
                    )
    elif world_map.lower() == 'y':
        print("Map generation skipped: missing dependencies")

    print(filename)


if __name__ == "__main__":
    main()
