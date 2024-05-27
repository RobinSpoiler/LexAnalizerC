from functools import reduce
def factorial_reduce(n):
    if n == 0:
        return 1
    return reduce(lambda x, y: x * y, range(1, n + 1))