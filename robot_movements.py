import math 



import initialization as i
robot_params = i.load_params("robot", file_path="params.json")

def segment_interseaction(origin, end, wall_start, wall_end):
    x1, y1 = origin
    x2, y2 = end
    x3, y3 = wall_start
    x4, y4 = wall_end

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        return None 

    ray_factor = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    wall_factor = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

    if (0.0 <= ray_factor <= 1.0) and (0.0 <= wall_factor <= 1.0):
        intersection_x = x1 + ray_factor * (x2 - x1)
        intersection_y = y1 + ray_factor * (y2 - y1)
        return intersection_x, intersection_y

    return None

def point_segment_distance(point_x, point_y, x1, y1, x2, y2):
    dist_x = x2-x1
    dist_y =y2-y1
    len_sq = dist_x**2 + dist_y**2
    if len_sq == 0:
        return math.hypot(point_x - x1, point_y - y1)
    ray_factor = max(0.0, min(1.0, ((point_x - x1) * dist_x + (point_y - y1) * dist_y) / len_sq))
    projetion_x = x1 + ray_factor * dist_x
    projection_y = y1 + ray_factor * dist_y
    return math.hypot(point_x - projetion_x, point_y - projection_y)


def creating_robot(x, y, theta, robot_params):
    proximity = robot_params["proximity"]
    sensor_angles = [2* math.pi*(i/proximity) for i in range(proximity)]
    return {"x": x, "y": y, "theta": theta, "sensor_angles": sensor_angles, "path": [(x,y)]}

 