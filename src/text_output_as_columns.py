# when you want to output some texts as several columns,
# and you don't know there is module called textwrap,
# this is what you do.      (T_T)feeling stupid...

COL_WIDTH = 20
from itertools import zip_longest
TEXT = """My house is small but cosy.

    It has a white kitchen and an empty fridge.

    I have a very comfortable couch, people love to sit on it.

    My mornings are filled with coffee and reading, if only I had a garden"""


OUTPUT = """
My house is small             It has a white                I have a very                 My mornings are               
but cosy.                     kitchen and an empty          comfortable couch,            filled with coffee            
                              fridge.                       people love to sit            and reading, if only          
                                                            on it.                        I had a garden                

"""


def text_to_columns(text):
    output = []
    paras = text.split('\n\n')
    for para in paras:
        words = para.strip().split(' ')
        x = ''
        x_try = ''
        x_out = []
        x_transient = ''
        for word in words:
            # print(word)
            if len(x_try) < COL_WIDTH:
                x = x_try
                x_try += ' ' + word if len(x_try) != 0 else word
                x_transient = word

                continue
            elif len(x_try) == COL_WIDTH:
                x_out.append(x_try)
                x = ''
                x_try = word
                continue
            else:
                x_out.append(x)
                # print(x)
                x = ''
                x_try = x_transient + ' ' + word
                # print(x_transient, x_try)
                continue
        x_out.extend([x_try] if len(x_try) < COL_WIDTH else [x_transient, words[-1]])
        output.append(x_out)

    i = 0
    output1 = ''
    for items in zip_longest(*output, fillvalue=''):
        # print(items)
        for item in items:
            output1 += f"{str(item):<30}"
            i += 1
            if i % len(paras) == 0:
                output1 += '\n'
    return output1


print(text_to_columns(TEXT))


# too sad to refactor the above code
# here is a better way using textwrap from Pybites
import textwrap
def _format(row):
    return " ".join(['{c:{w}}'.format(c=col, w=COL_WIDTH+PADDING)
                     for col in row])


def text_to_columns(text):
    cols = []
    for paragraph in text.split("\n\n"):
        col_lines = textwrap.fill(paragraph, width=COL_WIDTH).split("\n")
        cols.append(col_lines)

    output = []
    # need zip_longest otherwise text will get lost
    for row in zip_longest(*cols, fillvalue=''):
        output.append(_format(row))

    return "\n".join(output)