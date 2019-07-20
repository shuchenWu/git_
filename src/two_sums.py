"""Finds the indexes of the two numbers that add up to target.
   If multiple pairs meet the requirements, return the one with the minimum value at index1
"""
import heapq


# 跟下面那个比，花里胡哨的，但是可以返回所有符合条件的
def two_sums(numbers, target):
    d = {}
    candidate = []
    for idx, num in enumerate(numbers):
        if num in d:
            candidate.append((target-num, d[num], idx))
        else:
            d[target - num] = idx

    heapq.heapify(candidate)
    try:
        return heapq.heappop(candidate)[1:]
    except IndexError:
        return None


# this solution from PyBites
def two_sums_s(numbers, target):

    nums = sorted(numbers)
    i = 0
    j = len(numbers) - 1
    while i < j:
        total = nums[i] + nums[j]
        if total < target:
            i += 1
        elif total > target:
            j -= 1
        else:
            index1 = numbers.index(nums[i])
            index2 = numbers.index(nums[j])
            return index1, index2
    return None
