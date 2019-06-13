import sys
import unicodedata
import re


START_EMOJI_RANGE = 100000  # estimate


def what_means_emoji(emoji):
    try:
        return unicodedata.name(emoji)
    except (TypeError, ValueError):
        return 'Not found'


def _make_emoji_mapping():

    d = dict()
    for i in range(START_EMOJI_RANGE, sys.maxunicode + 1):
        if what_means_emoji(chr(i)) != 'Not found':
            d[chr(i)] = what_means_emoji(chr(i)).lower()
    return d


def find_emoji(term):
    term = term.lower()
    pattern = re.compile(r'\b' + str(term))
    emoji_mapping = _make_emoji_mapping()

    for key, value in emoji_mapping.items():
        if re.search(pattern, value):
            print(f'{value:<40}       |{key}')


find_emoji('sun')
