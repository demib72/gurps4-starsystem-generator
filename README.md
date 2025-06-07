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

Run `run.py` to generate output for a random star system. By default the
information is written to a LaTeX file but a Dokuwiki formatted file can be
created with `--format dokuwiki`. During execution you will be asked whether to
create a system GIF or maps of any Garden worlds.
GIFs are saved in the `gifs/` directory and are named after the generated
random system name with the star letter appended when multiple stars are
present. World maps for any generated Garden worlds are saved as PNGs in the
`maps/` directory using the same system name and planet identifier.
