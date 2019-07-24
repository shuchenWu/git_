"""
files: ['airbnb.txt', 'from_chris.txt', 'from_sara.txt', 'sometext.txt']
words_num: [1084486, 8801, 8777, 9]
Sequential: Read all 4 files in 0.16300010681152344 second.
Threading: Read all 4 files in 0.006033182144165039 second.
Async: Read all 4 files in 0.01296544075012207 second.
"""


from glob import glob
import concurrent.futures
import time
import asyncio
import aiofiles


files = glob('*.txt')
print(files)


def count_words_sequential(files):
    nums_words_seq = []
    start_time = time.time()
    for file in files:
        with open(file, encoding='utf8') as f:
            n = 0
            for line in f:
                n += len(line.split())
            nums_words_seq.append(n)
    duration = time.time() - start_time
    print(f'Sequential: Read all {len(files)} files in {duration} second.')
    return nums_words_seq



nums_words = []
def get_file_num_words(file):
    with open(file) as f:
        n = 0
        for line in f:
            n += len(line.split())
        nums_words.append(n)


def get_all_num(files):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(get_file_num_words, files)


def count_words_threading(files):
    start_time = time.time()
    get_all_num(files)
    duration = time.time() - start_time
    print(f'Threading: Read all {len(files)} files in {duration} second.')


nums_words_async = []


async def get_num_file_word(file):
    async with aiofiles.open(file, encoding='utf8') as f:
        n = 0
        content = await f.readline()
        n += len(content)
        nums_words_async.append(n)


async def get_all_num(files):
    tasks = []
    for file in files:
        task = asyncio.ensure_future(get_num_file_word(file))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    print(count_words_sequential(files))

    count_words_threading(files)

    start_time = time.time()
    asyncio.run(get_all_num(files))
    duration = time.time() - start_time
    print(f'Async: Read all {len(files)} files in {duration} second.')



# from csv to txt
# import csv
# with open('Airbnb Summary Listings NYC 2019-03-07.csv', newline='', encoding='utf8') as csv_file:
#     f = csv.reader(csv_file)
#     with open('airbnb.txt', 'w', encoding='utf8') as f_txt:
#         for row in f:
#             x = ', '.join(item for item in row)
#             f_txt.write(x)
