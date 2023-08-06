from CGLib.models.point import Point


class Node:
    def __init__(self, data):
        """By default Node has no children."""
        self.data = data
        self.left = None
        self.right = None

    def __eq__(self, other):
        """Recursive equality."""
        return (
            self.data == other.data
            and self.left == other.left
            and self.right == other.right
        )


class NodeWithParent(Node):
    def __init__(self, data, parent = None):
        self.parent = parent
        super().__init__(data)


class QuickhullData:
    def __init__(self, points, h, hull_piece):
        self.points = points
        self.h = h
        self.hull_piece = hull_piece


class QuickhullNode(Node):
    def __init__(self, points, h=None, hull_piece=None):
        super().__init__(QuickhullData(points, h, hull_piece))
