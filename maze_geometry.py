import initialization as i

maze_params = i.load_params("maze", file_path="params.json")

def get_wall_length(x1: float, y1: float, x2:float, y2:float):
    wall_length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return wall_length

def build_maze_walls(maze_params):
    width = maze_params['width']
    height = maze_params['height']
    walls = []
    goal_x = maze_params["horizontal_gap"] * width
    goal_half = maze_params["goal_radius"]
    walls.append((0, 0,width, 0))
    walls.append((0,0,0, height))
    walls.append((width, 0,0,0))
    walls.append((0, height, goal_x - goal_half, height))
    walls.append((goal_x + goal_half, height, width, height))
    y1 = maze_params["left_wall"] * height
    left_wall_len = 0.42 * width
    left_drop_bottom = maze_params["vertical_gap"] * 0.30 * height + 0.10 * height
    walls.append((0, y1, left_wall_len, y1))
    walls.append((left_wall_len, y1, left_wall_len, left_drop_bottom))
    
    y2 =maze_params["right_wall"] * height
    right_wall_start = 0.60 * width
    right_drop_bottom = 0.30*height
    walls.append((right_wall_start, y2, width, y2))
    walls.append((left_wall_len, y2, right_wall_start, right_drop_bottom))
    
    cross_wall = 0.5 * (left_drop_bottom + right_drop_bottom) - 0.03 * height
    cross_wall_x1 = (left_wall_len + 0.04) * width 
    cross_wall_x2 = (right_wall_start - 0.04) *width
    walls.append((cross_wall_x1,cross_wall, cross_wall_x2, cross_wall))
    
    
    return walls
    
    
    
def goal_position(maze_params):
    width = maze_params["width"]
    height = maze_params["height"]
    hg = maze_params["horizontal_gap"]
    radius = maze_params["goal_radius"]
    goal_x =  hg * width 
    goal_y = height - radius
    goal_target = (goal_x, goal_y)
    return goal_target


def bounds(maze_params):
    return (0, 0, maze_params["width"], maze_params["height"])


# maze_params = i.load_params("maze", file_path="params.json")
# walls = build_maze_walls(maze_params)
# print("Walls:", walls)
# goal = goal_position(maze_params)
# print("Goal Position:", goal)
# maze_bounds = bounds(maze_params)
# print("Maze Bounds:", maze_bounds)

