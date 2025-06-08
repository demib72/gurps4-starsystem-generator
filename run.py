import sys
import argparse
from stargen import StarSystem
from stargen.utils.latexout import LatexWriter
from stargen.utils.dokuwikiout import DokuwikiWriter
from stargen.utils.random_name import generate_random_name
from stargen.utils.gifout import render_system_gif
from stargen.utils.mapmaker import generate_world_map
from stargen.utils.serializer import dump_json

def main(args=None):
    print(args)
    parser = argparse.ArgumentParser(description="Generate a random star system")
    parser.add_argument(
        "--format",
        choices=["latex", "dokuwiki"],
        default="latex",
        help="Output format",
    )
    parser.add_argument(
        "--json",
        metavar="FILE",
        help="Write JSON representation to FILE",
        default=None,
    )
    if args is None:
        args = []
    parsed = parser.parse_args(args)

    print(parsed.format)

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

    if parsed.json:
        dump_json(star_system, parsed.json)

    system_gif = input("Do you want a gif of the system? [Y/N]: ")
    world_map = input("Do you want a map of the garden world(s)? [Y/N]: ")

    if system_gif.lower() == 'y':
        render_system_gif(star_system, f"gifs/{name}.gif")

    if world_map.lower() == 'y':
        for star in star_system.stars:
            oc_dict = star.planetsystem.get_orbitcontents()
            for oc in oc_dict.values():
                if hasattr(oc, 'get_type') and oc.get_type() == 'Garden':
                    hydro = oc.get_hydrographic_cover()
                    generate_world_map(
                        f"maps/{name}_{oc.get_name()}.png",
                        hydro,
                    )

    print(filename)


if __name__ == "__main__":
    main(sys.argv[1:])
