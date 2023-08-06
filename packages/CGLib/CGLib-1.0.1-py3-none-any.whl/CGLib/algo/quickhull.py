from models.line2d import Line2D
from models.bin_tree_node import QuickhullNode
from models.bin_tree import BinTree
from models.point import Point


sort_lr = lambda p: (p.x, -p.y)
sort_rl = lambda p: (-p.x, p.y)


def quickhull(points):
    lp = min(points, key=lambda p: p.coords)
    rp = max(points, key=lambda p: p.coords)

    s1 = make_subset(points, lp, rp, sort_key=sort_lr)
    s2 = make_subset(points, rp, lp, sort_key=sort_rl)

    tree = BinTree(QuickhullNode(s1 + s2[1:-1]))
    tree.root.left, tree.root.right = QuickhullNode(s1), QuickhullNode(s2)

    hull = (
        partition(s1, lp, rp, tree.root.left) +
        partition(s2, rp, lp, tree.root.right)[1:-1]
    )
    tree.root.data.hull_piece = hull

    yield lp, rp, s1, s2, tree
    yield tree
    yield hull


def partition(points, left, right, node):
    if len(points) == 2:
        node.data.hull_piece = [left, right]
        return node.data.hull_piece

    lr = Line2D(left, right)
    pts = filter(lambda x: x != left and x != right, points)

    h = max(pts, key=lambda p: (p.dist_to_line(lr), p.angle_with(left, right)))
    s1 = left_points(points, left, h)
    s2 = left_points(points, h, right)

    node.data.h, node.left, node.right = h, QuickhullNode(s1), QuickhullNode(s2)
    node.data.hull_piece = partition(s1, left, h, node.left) + partition(s2, h, right, node.right)[1:]
    
    return node.data.hull_piece


def make_subset(points, left, right, sort_key):
    return sorted(left_points(points, left, right), key=sort_key)


def left_points(points, p1, p2):
    """Points at the left of vector p1->p2 and p1, p2"""
    return (
        [p1] +
        [p for p in points if Point.direction(p1, p2, p) < 0] +
        [p2]
    )
