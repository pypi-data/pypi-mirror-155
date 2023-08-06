from models import Node, KdTree


def kd_tree(points, x_range, y_range):
    ordered_x = sorted(points)
    ordered_y = sorted(points, key=lambda p: (p.y, p.x))
    yield ordered_x, ordered_y

    root = Node(ordered_x[len(ordered_x) // 2])
    tree = KdTree(root, x_range, y_range)
    tree.make_tree(ordered_x, root)
    yield tree.partition
    yield tree

    result = tree.region_search(root, vertical=True)
    yield tree.search_list
    yield result
