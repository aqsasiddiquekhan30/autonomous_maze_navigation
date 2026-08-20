import numpy as np
from numbers import Real
import json

problem_id = 820165 #id for individualism
seed = 42
rng = np.random.RandomState(problem_id)

def fraction_in_range(lower_bound: Real, upper_bound: Real): 
    if lower_bound > upper_bound:
        raise ValueError("Lower bound should be less than upper bound.")
    return float(rng.uniform(lower_bound, upper_bound))


def load_params(key=None,file_path=None):
    with open(file_path, 'r') as f:
        params = json.load(f)
    if key not in params:
        raise KeyError(f"This'{key}' not found in the JSON file.")
    elif key == "maze":
        params["maze"]["left_wall"] = fraction_in_range(0.18, 0.30)
        params["maze"]["right_wall"] = fraction_in_range(0.52, 0.68)
        params["maze"]["horizontal_gap"] = fraction_in_range(0.38, 0.48)
        params["maze"]["vertical_gap"] = fraction_in_range(0.42, 0.58)
        return params["maze"]
    else:
        return params[key]


# if __name__ == "__main__":
#     # Get ONLY the maze parameters with calculations included
#     file_path = "params.json"
#     maze_params = load_params("maze", file_path=file_path)
#     print("Maze:", maze_params)
    
#     # Get ONLY the robot parameters
#     robot_params = load_params("robot", file_path=file_path)
#     print("Robot:", robot_params)
    
