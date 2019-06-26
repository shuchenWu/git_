
# different lengths of rods have different prices, given a length, figure out maximum price we can get.
import math


def cache_for_cut(func):
    d = {}

    def wrapper(lst, n):
        if n not in d:
            d[n] = func(lst, n)
        return d[n]
    return wrapper


@cache_for_cut
def cut_rods(price_list, length):
    if length == 0:
        return 0
    else:
        q = -math.inf
        for (l, price) in price_list:
            if length - l < 0:
                break
            q = max(q, price + cut_rods(price_list, length - l))
        return q


print(cut_rods([(1, 1), (2, 5), (5, 10), (6, 17), (7, 17), (8, 20), (10, 30)], 9))


# bottom-up
def cut_rod_b(price_lst, length):
    lst = [0] * (length + 1)
    for (l, price) in price_lst:
        for i in range(l, length+1):
            lst[i] = max(price + lst[i - l], lst[i])
    return lst


print(cut_rod_b([(1, 1), (2, 5), (5, 10), (6, 17), (7, 17), (8, 20), (10, 30)], 9))
