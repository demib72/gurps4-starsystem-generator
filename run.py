from stargen import StarSystem
from stargen.utils.latexout import LatexWriter
from stargen.utils.random_name import generate_random_name

def main():
    filename = f"{generate_random_name()}.tex"
    # testsystem = StarSystem()
    star = StarSystem()
    tex = LatexWriter(star, filename)

    star.print_info()
    tex.write()

    print(filename)


if __name__ == "__main__":
    main()
