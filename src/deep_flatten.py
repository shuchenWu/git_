from numbers import Integral


def deep_flatten(it):
    for item in it:
        if not isinstance(item, (Integral, str)):
            yield from deep_flatten(item)
        else:
            yield item


for i in deep_flatten([['apple', 'pickle'], ['pear', 'avocado']]):
    print(i, end=' ')
