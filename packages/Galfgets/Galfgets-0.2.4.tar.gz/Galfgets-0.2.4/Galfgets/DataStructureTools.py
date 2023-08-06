# Data Structures tools

from typing import Tuple


def binarySearch(list_input:list, item:int) -> Tuple[bool, int]:
    # Code from https://stackoverflow.com/questions/34420006/binary-search-python-3-5
    first = 0
    last = len(list_input)-1
    found = False
    
    while first<=last and not found:
        midpoint = (first + last)//2
        if list_input[midpoint] == item:
            found = True
        else:
            if item < list_input[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1

    return found, midpoint
