# gurps4-starsystem-generator

Modified code from https://github.com/tschoppi/starsystem-gen. Adds ability to create garden worlds and choose world types instead of just random selection. No web interface.

To Start, add the following to a python file:

from stargen import StarSystem

star = StarSystem()

## Installation

```
pip install -r requirements.txt
```

## Usage

Run `run.py` to generate LaTeX and GIF outputs for a random star system. GIFs
are saved in the `gifs/` directory and are named after the generated random
system name with the star letter appended when multiple stars are present.
World maps for any generated Garden worlds are saved as PNGs in the `maps/`
directory using the same system name and planet identifier.
