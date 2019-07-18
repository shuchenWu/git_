"""
questions about python on StackOverflow with more than 1 million views,
sorted by votes in descending order
"""

from operator import itemgetter
from bs4 import BeautifulSoup
import requests

URL = 'https://stackoverflow.com/questions/tagged/python?tab=Frequent'
r = requests.get(URL)

bs = BeautifulSoup(r.text, 'html.parser')


def top_python_questions():
    x = bs.find_all('h3')[3:]
    y = bs.find_all('span', class_='vote-count-post')
    z = bs.find_all('div', class_='views')

    x = (i.get_text().strip() for i in x)
    y = (i.get_text().strip() for i in y)
    z = (i.get_text().strip() for i in z)
    s = sorted(((b, a) for a, b, c in zip(x, y, z) if 'm' in c), reverse=True)
    return list(s)


# this method's from PyBites,
def top_python_questions_1():
    questions = bs.select(".question-summary")
    print(type(questions))
    res = []

    for que in questions:
        question = que.select_one('.question-hyperlink').getText()
        votes = que.select_one('.vote-count-post').getText()

        views = que.select_one('.views').getText().strip()
        if 'm views' not in views:
            continue

        res.append((question, int(votes)))

    return sorted(res, key=itemgetter(1), reverse=True)


if __name__ == '__main__':
    print(top_python_questions())
