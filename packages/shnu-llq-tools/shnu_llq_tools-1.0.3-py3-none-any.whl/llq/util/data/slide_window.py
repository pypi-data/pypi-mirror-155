from itertools import product

l1 = [1, 2, 3]
l2 = [4, 5, 6]
combinatios = product(l1, l2)
print(*combinatios)

from itertools import tee
from typing import Iterable


def slide_window(iterable: Iterable, window_size):
    hi = tee(iter(iterable), window_size)
    repeat = lambda x, y: [next(x) for _ in range(y)]
    [repeat(hi[i], i) for i in range(1, window_size)]
    return zip(*hi)




print(*slide_window(range(20), 5))



w=range(12)
b=[iter(w)]*2
print(next(b[0]),next(b[1]))
print('**3'*3)
print(*b[1])
print(*zip(*b))

x=range(12)
print(*zip(*[iter(x)]*4))

