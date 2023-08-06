import sys


def get_max(arr):
    return max(arr) if len(arr) > 0 else sys.maxsize


def get_min(arr):
    return min(arr) if len(arr) > 0 else -sys.maxsize
