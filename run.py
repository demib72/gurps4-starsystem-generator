from stargen import StarSystem
from stargen.utils.latexout import LatexWriter
from stargen.utils.random_name import generate_random_name

filename = f"{generate_random_name()}.tex"
#testsystem = StarSystem()
star = StarSystem()
tex = LatexWriter(star, filename)

star.print_info()
tex.write()

print(filename)
