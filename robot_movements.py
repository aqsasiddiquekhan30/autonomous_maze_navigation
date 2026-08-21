import math 



import initialization as i
robot_params = i.load_params("robot", file_path="params.json")
print("Robot Parameters:", robot_params)

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

def get_sensor_data(robot, walls, robot_params):
    readings=[]
    for sensor_angle in robot["sensor_angles"]:
        angle = robot["theta"] + sensor_angle 
        origin = (robot["x"] + robot_params["body_radius"] * math.cos(angle), robot["y"] + robot_params["body_radius"] * math.sin(angle))
        end = (robot["x"] + robot_params["sensor_max_range"] * math.cos(angle), robot["y"] + robot_params["sensor_max_range"] * math.sin(angle))
        min_distance = robot_params["sensor_max_range"]
        for wall in walls:
            wall_x1, wall_y1, wall_x2, wall_y2 = wall
            intersection_point = segment_interseaction(origin, end, (wall_x1, wall_y1), (wall_x2, wall_y2)) 
            if intersection_point is not None:
                distance = math.hypot(intersection_point[0] - origin[0], intersection_point[1] - origin[1])
                if distance < min_distance:
                    min_distance = distance
    activation = 1.0 - (min_distance / robot_params["sensor_max_range"])
    readings.append(max(0.0, min(1.0, activation)))
    return readings


def has_collided(x, y, walls, robot_params):
    r = robot_params["body_radius"]
    for wall in walls:
        wall_x1, wall_y1, wall_x2, wall_y2 = wall
        if point_segment_distance(x, y, wall_x1, wall_y1, wall_x2, wall_y2) < r:
            return True
    return False

def update_robot_movement(robot, left_speed, right_speed, dt, walls, robot_params):
    left_speed = max(-robot_params["max_speed"], min(robot_params["max_speed"], left_speed))
    right_speed = max(-robot_params["max_speed"], min(robot_params["max_speed"], right_speed))

    left_velocity = left_speed * robot_params["wheel_radius"]
    right_velocity = right_speed * robot_params["wheel_radius"]
    v = (left_velocity + right_velocity) / 2.0
    omega = (right_velocity - left_velocity) / robot_params["axle_length"]

    new_x = robot["x"] + v * math.cos(robot["theta"]) * dt
    new_y = robot["y"] + v * math.sin(robot["theta"]) * dt
    new_theta = robot["theta"] + omega * dt

    if has_collided(new_x, new_y, walls, robot_params):
        robot["collided"] = True
        robot["theta"] = new_theta
    else:
        robot["x"] = new_x
        robot["y"] = new_y
        robot["theta"] = new_theta
    robot["path"].append((robot["x"], robot["y"]))


# rc = robot_params

# # Example mock walls (simple square box bounds)
# mock_walls = [
#     (0, 0, 3.5, 0),
#     (3.5, 0, 3.5, 2.0),
#     (3.5, 2.0, 0, 2.0),
#     (0, 2.0, 0, 0)
# ]
# my_robot = creating_robot(x=0.3, y=0.3, theta=0.0, robot_params=rc)
    
# print("Initial sensors:", [f"{s:.2f}" for s in get_sensor_data(my_robot, mock_walls, rc)])

# # Run a few simulation steps
# for _ in range(20):
#     update_robot_movement(my_robot, left_speed=3.0, right_speed=2.5, dt=1/60, walls=mock_walls, robot_params=rc)
    
# print("After 20 steps:", my_robot["x"], my_robot["y"], my_robot["theta"])