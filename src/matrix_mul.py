
# 没有必要，但是可以，just for practicing iterators
from operator import mul
from itertools import tee, islice


class Matrix(object):

    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return f'<Matrix values="{self.values}">'

    def __matmul__(self, other):
        x = zip(*(row for row in other.values))
        y = (sum(mul(*item) for item in zip(row, col)) for col in x for row in self.values)
        z = (islice(y_out, idx, None, len(self.values)) for idx, y_out in enumerate(tee(y, len(self.values))))
        return Matrix([list(i) for i in z])


if __name__ == '__main__':
    m1 = Matrix([[11, 12], [13, 14], [15, 16]])
    m2 = Matrix([[1, 2, 3], [4, 5, 6]])
    m3 = m1 @ m2
    assert m3.values == [[59, 82, 105], [69, 96, 123], [79, 110, 141]]