#from stargen import StarSystem
from worldpremade import WorldPremade
from star import Star
from tables import StEvoTable
from stargen import StarSystem

#testsystem = StarSystem()
star = StarSystem()

star.print_info()

#print(testsystem.open_cluster)
#print(testsystem.num_stars)
#print(testsystem.age)

def new_func():
    for i in range(1,19):
        if i <= 7:
            print(f"{i} is hostile")

        if 7 < i <= 13:
            print(f"{i} is barren")
            
        if 13 < i <= 18:
            print(f"{i} is garden")