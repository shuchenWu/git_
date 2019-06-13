import argparse
from functools import reduce
import operator


operations = dict(add=sum,
                  sub=lambda items: reduce(operator.sub, items),
                  mul=lambda items: reduce(operator.mul, items),
                  div=lambda items: reduce(operator.truediv, items))


def calculator(operation, numbers):
    """TODO 1:
       Create a calculator that takes an operation and list of numbers.
       Perform the operation returning the result rounded to 2 decimals"""
    func = operations.get(operation)
    if not func:
        raise ValueError('Invalid operator')
    numbers = [float(num) for num in numbers]
    re = func(numbers)
    return round(re, 2)


def create_parser():
    """TODO 2:
       Create an ArgumentParser object:
       - have one operation argument,
       - have one or more integers that can be operated on.
       Returns a argparse.ArgumentParser object.

       Note that type=float times out here so do the casting in the calculator
       function above!"""
    parser = argparse.ArgumentParser(description='a simple calculator')
    parser.add_argument('-a', '--add', metavar='ADD',
                        nargs='+', help='Sums numbers')
    parser.add_argument('-s', '--sub', metavar='SUB',
                        nargs='+', help='Subtracts numbers')
    parser.add_argument('-m', '--mul', metavar='MUL',
                        nargs='+', help='Multiplies numbers')
    parser.add_argument('-d', '--div', metavar='DIV',
                        nargs='+', help='Divides numbers')

    return parser


def call_calculator(args=None, stdout=False):
    """Provided/done:
       Calls calculator with provided args object.
       If args are not provided get them via create_parser,
       if stdout is True print the result"""
    parser = create_parser()

    if args is None:
        args = parser.parse_args()

    # taking the first operation in args namespace
    # if combo, e.g. -a and -s, take the first one
    for operation, numbers in vars(args).items():
        if numbers is None:
            continue

        try:
            print(operation, numbers)
            res = calculator(operation, numbers)
        except ZeroDivisionError:
            res = 0

        if stdout:
            print(res)

        return res


if __name__ == '__main__':
    call_calculator(stdout=True)
