import hashlib
import numpy as np
from numbers import Real

problem_id = 820165 #id for individualism
seed = 42
rng = np.random.RandomState(problem_id)

def fraction_in_range(lower_bound: Real, upper_bound: Real): 
    if lower_bound > upper_bound:
        raise ValueError("Lower bound should be less than upper bound.")
    return float(rng.uniform(lower_bound, upper_bound))


