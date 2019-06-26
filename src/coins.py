
# given denominations, figure out ways to get a certain amount
import pickle


def cache_for_coins(func):
    d = dict()

    def wrapper(*args):
        x = pickle.dumps(args)
        if x not in d:
            d[x] = func(*args)
        return d[x]
    return wrapper


@cache_for_coins  # recursion plus cache -> memoization
def coins_rec(denominations, amount):
    if len(denominations) == 0:
        return 0
    if amount < 0:
        return 0
    if amount == 0:
        return 1
    else:
        ways_with = coins_rec(denominations, amount - denominations[0])
        ways_without = coins_rec(denominations[1:], amount)
        return ways_with + ways_without

# print(coins_rec([50, 10, 5, 2, 1], 1000))
# print(coins_rec([1, 2, 3, 4], 5))


# bottom-up
def coins_b(denominations, amount):
    lst = [0] * (amount + 1)
    lst[0] = 1
    for denomination in denominations:
        for i in range(denomination, amount+1):
            lst[i] = lst[i] + lst[i - denomination]
    return lst


if __name__ == '__main__':
    print(coins_rec([50, 10, 5, 2, 1], 1000))
    print(coins_b([1, 2, 3, 4], 5))
