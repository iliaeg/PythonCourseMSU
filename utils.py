import sys


# function printing to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)