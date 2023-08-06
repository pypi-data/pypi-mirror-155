from math import pi
from models.point import Point


def graham(points):
    i = 2
    while Point.direction(points[0], points[1], points[i]) == 0:
        i += 1
    
    centroid = Point.centroid([points[0], points[1], points[i]])
    yield centroid
    
    origin = min(points, key=lambda p: (p.y, -p.x))
    ordered = sort_points(points, centroid, origin)
    yield ordered
    yield origin

    ordered.append(origin)
    steps_table = []
    hull = make_hull(steps_table, ordered)
    ordered.pop()
    yield steps_table
    yield hull


def sort_points(points, centroid, origin):
    min_angle = origin.polar_angle_with(centroid)

    def angle_and_dist(p):
        p_angle = p.polar_angle_with(centroid)
        angle = p_angle if p_angle >= min_angle else 2 * pi + p_angle
        return (angle, p.dist_to_point(centroid))

    return sorted(points, key=angle_and_dist)


def make_hull(steps_table, ordered):
    ans = ordered[:2]
    for p in ordered[2:]:
        while len(ans) > 1 and Point.direction(ans[-2], ans[-1], p) >= 0:
            steps_table.append(current_step(ans, False, p))
            ans.pop()

        if len(ans) > 1:
            steps_table.append(current_step(ans, True, p))
        ans.append(p)

    return ans[:-1]


def current_step(ans, add, p):
    """Current step: current points' triple, add/delete, point to add/delete."""
    return [ans[-2], ans[-1], p], add
