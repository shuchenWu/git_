# to find the longest common sequences
# and a way to reconstruct the exact common sequence


seq1 = 'abcdaf'
seq2 = 'acbcf'
# OUTPUT : longest length:  4
#          Track: (0, 0),(1, 2),(2, 3),(5, 4),  the position of the common letters


def longest(i, j):
    if i == 0 or j == 0:
        if seq1[0] == seq2[0]:
            return 1, [(0, 0)]
        else:
            return 0, []
    if seq1[i] == seq2[j]:
        result, used_pair = longest(i - 1, j - 1), (i, j)
        return result[0] + 1, result[1] + [used_pair]

    else:
        result, used_pair = max([[longest(a, b), ((a+1, b) if idx == 0 else (a, b+1))] for idx, (a, b) in enumerate([(i-1, j), (i, j-1)])], key=lambda x: x[0][0])
        return result[0], result[1] + [used_pair]


print('-' * 20)
l, items = longest(len(seq1)-1, len(seq2)-1)
print('longest length: ', l)
print('Track: ', end='')
for item in items:
    i, j = item
    if seq1[i] == seq2[j]:
        print(f'({i}, {j})', end=',')
