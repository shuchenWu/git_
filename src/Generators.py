# notes from James Powell's online course
# Python Advanced: Generators and Coroutines on O'Reilly


# utils been used
from contextlib import contextmanager
from time import time

class Timing:
    def __init__(self, start=None):
        if start is None:
            start = time()
        self.laps = [start]
    def __call__(self):
        self.laps.append(time())
    @property
    def elapsed(self):
        if len(self.laps) < 2:
            raise ValueError('too few timings')
        return self.laps[-1] - self.laps[0]

@contextmanager
def Timer():
    t = Timing()
    try:
        yield t
        t()
    finally:
        pass

@contextmanager
def timer():
    start = time()
    try:
        yield
        print(f'\N{greek capital letter delta}t → {time() - start:.4f}s')
    finally:
        pass

# simpler pumped
from functools import wraps
def pumped(gen):
    @wraps(gen)
    def inner(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g.send
    return inner




def fib(a=1, b=1):
    while True:
        yield a
        a, b = b, a + b

from time import time
from itertools import islice, takewhile

for x in islice(fib(), 10):
    print(x)

for x in takewhile(lambda x: x < 50, fib()):
    print(x)


def timeout(t, g):
    start = time()
    for x in g:
        if time() - start > t:
            break
        yield x


for x in timeout(0.00000001, islice(fib(), 200)):
    print(x)


# xs = list(islice(fib(), 100))
# for a, b in zip(xs, xs[1:]):
#     print(b/a)

from itertools import tee
#
# g1, g2 = tee(fib(), 2)
# next(g2)
# for a, b in zip(g1, g2):
#     print(b/a)

# a windows of size 3
nwise = lambda g, n=2: zip(*(islice(g, idx, None) for idx, g in enumerate(tee(g, n))))
for a, b, c in nwise(range(10), 3):
    print(a, b, c)


xs = [1, 2, 3, 4, 5, 6]
ys = (x ** 2 for x in xs)
zs = (y + 1 for y in ys)


from dis import dis
def f():
    yield 1
    yield 20
    yield 300

dis(f)
gi = f()
next(gi)
print(f'{gi.gi_frame.f_lasti}')


# $1.52
# -> 1 x $1.00
# -> 2 x $0.25
# -> 2 x $0.01


from itertools import repeat, chain, takewhile

greedy = lambda items, predicate: chain.from_iterable(takewhile(predicate, repeat(x)) for x in items)


@pumped
def predicate(target, state=0, constraint=lambda _, __:True):
    value = yield
    while True:
        if state + value <= target:
            state += value
            value = yield True
        else:
            value = yield False


denominations = [1, 5, 10, 25, 100, 500, 1000, 2000, 5000]
denominations = reversed(denominations)
from random import randrange
from itertools import groupby

amount = randrange(100, 1000)
pred = predicate(amount)
coins = greedy(denominations, pred)

print('-' * 15)
print(f'Change for: ${amount/100:.2f}')
for c, cs in groupby(coins):
    print(f'{sum(1 for _ in cs)} * {c/100:.2f}')

