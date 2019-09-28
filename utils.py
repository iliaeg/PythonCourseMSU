import sys
import math

def ceil_five(x):
    return 5 * math.ceil(int(x) / 5)

def trunc2(array):
        return\
            list(
                map(
                    lambda x: x - x % 0.01,
                    array
            ))

def percent_stat(series, size, percent):
    '''
    
    Args:
        series: ascending array or pd.series indexed by int from zero
        size (int): size of series
        percent (float): percentage in range [0, 1]

    Returns:
        value that greater than <percent> * <size> values
    '''

    return\
        series[
            min(
                math.ceil(percent * size),
                size - 1
            )]

# function printing to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)