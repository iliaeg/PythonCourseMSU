import math

def ceil5(x, base=5):
    return base * math.ceil(x/base)

print(int(ceil5(16)))