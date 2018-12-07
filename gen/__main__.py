# Generate all of the tables needed for front.html, in order
#
# Usage:
#   From cmd line in project root: (type in cmd after $)
#      For old_main:
#        > linguistics-db/ $ set PYTHONIOENCODING=utf-8
#        > linguistics-db/ $ python -m gen > gen/out.html

#      For main:
#        > linguistics-db/ $ python -m gen


from . import allgen, splice

# Prints autogen html to stdout, requires manually setting PYTHONIOENCODING
def old_main():
    allgen.main()

def main():
    allgen.main(output="gen/out.html")
    splice.main()

main()
