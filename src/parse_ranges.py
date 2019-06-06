import re


def parse_ranges(string):
    """takes a string ,eg: '1-5, 20, 30->exit'"""
    p = re.compile(r'(?P<start>\d+)-?(?P<end>\d+)?')
    match = re.finditer(p, string)
    ls = list()

    for m in match:
        begin = int(m.group('start'))
        end = int(m.group('end'))+1 if m.group('end') is not None else begin+1
        ls.append(i for i in range(begin, end))  # somehow a list of generators
        for item in ls:
            for value in item:
                yield value
