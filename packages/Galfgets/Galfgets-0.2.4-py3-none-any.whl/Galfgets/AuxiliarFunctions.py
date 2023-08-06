
# Math computing functions

import math
import string
import random
import functools


def mean(list_input:list) -> float:
    aggregation = functools.reduce(sum_funct, list_input, 0)

    return aggregation / float(len(list_input))

def variance(list_input:list) -> float:
    m = mean(list_input)
    v = functools.reduce(sum_funct, map(functools.partial(variance_funct, m=m), list_input))
    
    return v / float(len(list_input))

def standard_desviation(list_input:list) -> float:
    return math.sqrt(variance(list_input))

# Lambda functions

flatten_list        = lambda t: [item for sublist in t for item in sublist]
formatter_sentences = lambda x, y: "{}\n{}".format(x,y)
gen_dict_from_int   = lambda x: {item:0 for item in range(x)}

sum_funct               = lambda x, y: x+y
variance_funct          = lambda x, m: (x - m) ** 2

coordinates_oper        = lambda x1, x2: math.pow((x2 - x1), 2)
distance_between_points = lambda p1, p2: math.sqrt(functools.reduce(sum_funct, map(coordinates_oper, p1, p2)))

get_random_string       = lambda n_chars: ''.join(random.choice(string.ascii_letters + string.digits) for i in range(n_chars))