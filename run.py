from stargen import StarSystem
from stargen.utils.latexout import LatexWriter
from stargen.utils.random_name import generate_random_name

def main():
    try:
        from stargen.utils.gifout import render_system_gif
    except ImportError:
        render_system_gif = None

    name = generate_random_name()
    filename = f"{name}.tex"
    # testsystem = StarSystem()
    star_system = StarSystem()
    tex = LatexWriter(star_system, filename)

    star_system.print_info()
    tex.write()

    if render_system_gif:
        render_system_gif(star_system, f"gifs/{name}.gif")
    else:
        print("GIF generation skipped: missing dependencies")

    print(filename)


if __name__ == "__main__":
    main()
