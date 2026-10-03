# Generate all of the tables needed for front.html, in order
#
# Usage:
#   From cmd line in project root: (type in cmd after $)
#      For old_main:
#        > linguistics-db/ $ set PYTHONIOENCODING=utf-8
#        > linguistics-db/ $ python -m gen > gen/out.html

#      For main:
#        > linguistics-db/ $ python -m gen

from pathlib import Path

from . import splice
from . import allgen

# Prints autogen html to stdout, requires manually setting PYTHONIOENCODING
def old_main():
    allgen.main()

def main():
    output_path = Path(__file__).parent / "out.html"

    allgen.main(output=output_path)
    splice.main()
