"""
from topcoder https://community.topcoder.com/stat?c=problem_statement&pm=10329&13757

We have a book with N pages, numbered 1 to N. How many times does each digit occur in the page numbers?
You are given an int N. Return a int[] with 10 elements, where for all i between 0 and 9, inclusive,
the element i will be the number of times digit i occurs when we write down all the numbers between 1 and N, inclusive.

Examples
0)  7
    Returns: {0, 1, 1, 1, 1, 1, 1, 1, 0, 0 }
1)  19
    Returns: {1, 12, 2, 2, 2, 2, 2, 2, 2, 2 }
    Digits 2 to 9 now occur twice each, and we have plenty of occurrences of the digit 1.
2)	999
    Returns: {189, 300, 300, 300, 300, 300, 300, 300, 300, 300 }
3)  543212345
    Returns: {429904664, 541008121, 540917467, 540117067, 533117017, 473117011, 429904664, 429904664, 429904664, 429904664}
"""


def cache(func):
    d = {}

    def wrapper(n):
        if n not in d:
            d[n] = func(n)
        return d[n]
    return wrapper


@cache
def get_digits(n):
    output = [0] * 10
    if len(str(n)) == 1:
        for i in range(n + 1):
            output[i] += 1
        return output
    else:
        s_n = str(n)
        digits = len(s_n)
        middle_number = int(s_n[0] + '0' * (len(s_n) - 1))  # eg: 3659, digit=4, remainder=659, middle=3000
        remainder = n - middle_number
        output[int(s_n[0])] += 1 + remainder
        output[0] += digits - 1
        for idx, i in enumerate(get_digits(middle_number-1)):  # recursively
            output[idx] += i
        for idx, i in enumerate(get_digits(remainder)):
            output[idx] += i
        output[0] += remainder*(digits - 1) - sum(get_digits(remainder))  # get leading zeros
        return output


if __name__ == '__main__':
    x = get_digits(543212345)
    x[0] -= 1  # the very first 0 that we've counted in
    print(x)
