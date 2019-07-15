# excierse from pythonmorsels~
# This class should work like a set, but it should also maintain the insertion order of the items added to it
# This set should be relatively memory efficient and containment checks should be relatively time efficient
# For the first bonus, make sure your set works with the add and discard methods
# For the second bonus, make your OrderedSet class support equality.
#       If an OrderedSet is compared to another OrderedSet, they'll only be seen as equal if the order is the same.
#       If an OrderedSet is compared to an unordered set, the order is ignored during the comparison.
#       If an OrderedSet is compared to a non-set, the comparison should evaluate as False
from collections.abc import MutableSet, Sequence
from collections.abc import MutableSet


class OrderedSet(MutableSet):

    """Set-like object that maintains insertion order of items."""

    def __init__(self, itr):
        self._set = dict.fromkeys(itr, None)

    def __contains__(self, item):
        return item in self._set

    def __str__(self):
        return ' '.join(self._set.keys())

    def __iter__(self):
        return iter(self._set.keys())

    def __len__(self):
        return len(self._set)

    def add(self, item):
        self._set[item] = None

    def discard(self, item):
        self._set.pop(item, None)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (
                len(self) == len(other) and
                all(x == y for x, y in zip(self, other))
            )
        return super().__eq__(other)


# For the third bonus, make OrderedSet class to support indexing


class OrderedSetWithIdx(Sequence, MutableSet):

    """Set-like object that maintains insertion order of items."""

    def __init__(self, iterable):
        self.items = set()
        self.order = []
        self |= iterable

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.order[index]

    def add(self, item):
        if item not in self.items:
            self.order.append(item)
        self.items.add(item)

    def discard(self, item):
        if item in self.items:
            self.order.remove(item)
            self.items.remove(item)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (
                len(self) == len(other) and
                all(x == y for x, y in zip(self, other))
            )
        return super().__eq__(other)


if __name__ == "__main__":
    words = OrderedSetWithIdx(['hello', 'hello', 'how', 'are', 'you'])
    print(words[1])
    ordered_words = ['these', 'are', 'words', 'in', 'an', 'order']
    print(*OrderedSet(ordered_words))
    print(OrderedSet(['how', 'are', 'you']) ==
          OrderedSet(['how', 'you', 'are']))  # False
