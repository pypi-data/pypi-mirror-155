import math
from copy import deepcopy
from unittest import TestCase
from collections import OrderedDict


from ..models.point import Point
from ..models.vertex import Vertex
from ..models.edge import Edge, OrientedEdge
from ..models.graph import Graph, OrientedGraph
from ..models.bin_tree_node import Node, QuickhullNode, NodeWithParent
from ..models.bin_tree import BinTree, ChainsBinTree, KdTree


from ..algo.stripe_method import stripe
from ..algo.kd_tree_method import kd_tree
from ..algo.jarvis import jarvis
from ..algo.graham import graham
from ..algo.quickhull import quickhull
from ..algo.loci import Loci
from ..algo.chain_method import chain_method
from ..algo.dc_closest_points import closest_points
from ..algo.region_tree_method import region_tree_method


class TestAlgorithms(TestCase):
    """algorithm tests."""

    def test_stripe(self):
        p1 = Vertex(Point(7, 0))
        p2 = Vertex(Point(2, 2.5))
        p3 = Vertex(Point(12, 3))
        p4 = Vertex(Point(8, 5))
        p5 = Vertex(Point(0, 7))
        p6 = Vertex(Point(13, 8))
        p7 = Vertex(Point(6, 11))

        g = Graph()

        g.add_vertex(p1)
        g.add_vertex(p2)
        g.add_vertex(p3)
        g.add_vertex(p4)
        g.add_vertex(p5)
        g.add_vertex(p6)
        g.add_vertex(p7)

        g.add_edge(p1, p2)
        g.add_edge(p1, p3)
        g.add_edge(p2, p3)
        g.add_edge(p7, p6)
        g.add_edge(p3, p6)
        g.add_edge(p4, p6)
        g.add_edge(p4, p5)
        g.add_edge(p4, p7)
        g.add_edge(p5, p7)
        g.add_edge(p2, p5)

        dot = Point(11.5, 5.5)

        ans = list(stripe(g, dot))
        self.assertEqual(
            ans[0],
            [
                (-math.inf, 0.0),
                (0.0, 2.5),
                (2.5, 3.0),
                (3.0, 5.0),
                (5.0, 7.0),
                (7.0, 8.0),
                (8.0, 11.0),
                (11.0, math.inf),
            ],
        )

        self.assertTrue(
            TestAlgorithms.fragmentation_eq(
                ans[1],
                {
                    (-math.inf, 0.0): [],
                    (0.0, 2.5): [Edge(p1, p2), Edge(p1, p3)],
                    (2.5, 3.0): [Edge(p1, p3), Edge(p2, p3), Edge(p2, p5)],
                    (3.0, 5.0): [Edge(p2, p5), Edge(p3, p6)],
                    (5.0, 7.0): [
                        Edge(p2, p5),
                        Edge(p4, p5),
                        Edge(p4, p7),
                        Edge(p4, p6),
                        Edge(p3, p6),
                    ],
                    (7.0, 8.0): [
                        Edge(p5, p7),
                        Edge(p4, p7),
                        Edge(p4, p6),
                        Edge(p3, p6),
                    ],
                    (8.0, 11.0): [Edge(p5, p7), Edge(p4, p7), Edge(p7, p6)],
                    (11.0, math.inf): [],
                },
            )
        )

        self.assertEqual(ans[2], (5.0, 7.0))
        self.assertEqual(ans[3], [Edge(p4, p6), Edge(p3, p6)])

    @staticmethod
    def fragmentation_eq(f1, f2):
        for i in f1:
            for item in f1[i]:
                if item not in f2[i]:
                    return False
        for i in f2:
            for item in f2[i]:
                if item not in f1[i]:
                    return False
        return True

    def test_jarvis1(self):
        pts = [
            Point(1, 4),
            Point(0, 0),
            Point(3, 3),
            Point(3, 1),
            Point(7, 0),
            Point(5, 5),
            Point(5, 2),
            Point(9, 6),
        ]
        hull = [Point(0, 0), Point(1, 4), Point(9, 6), Point(7, 0)]
        ans = jarvis(pts)
        self.assertEqual(ans, hull)

    def test_jarvis2(self):
        pts = [Point(3, 3), Point(1, 1), Point(5, 0)]
        hull = [Point(1, 1), Point(3, 3), Point(5, 0)]
        ans = jarvis(pts)
        self.assertEqual(ans, hull)

    def test_kd_tree(self):
        pts = [
            Point(0, 9),
            Point(2, 3),
            Point(3, 6),
            Point(5, 8),
            Point(6, 1),
            Point(8, 13),
            Point(10, 2),
            Point(12, 4),
            Point(14, 11),
            Point(15, 5),
            Point(17, 10)
        ]
        rx = [3, 14]
        ry = [0, 8]

        ordered_x = pts
        ordered_y = [
            Point(6, 1),
            Point(10, 2),
            Point(2, 3),
            Point(12, 4),
            Point(15, 5),
            Point(3, 6),
            Point(5, 8),
            Point(0, 9),
            Point(17, 10),
            Point(14, 11),
            Point(8, 13)
        ]

        tree = KdTree(Node(Point(8, 13)), [], [])
        tree.root.left = Node(Point(3, 6))
        tree.root.left.left = Node(Point(6, 1))
        tree.root.left.left.left = Node(Point(2, 3))
        tree.root.left.right = Node(Point(5, 8))
        tree.root.left.right.left = Node(Point(0, 9))

        tree.root.right = Node(Point(15, 5))
        tree.root.right.left = Node(Point(12, 4))
        tree.root.right.left.left = Node(Point(10, 2))
        tree.root.right.right = Node(Point(17, 10))
        tree.root.right.right.left = Node(Point(14, 11))

        partition = [
            (Point(8, 13), True),
            (Point(3, 6), False),
            (Point(6, 1), True),
            (Point(2, 3), False),
            (Point(5, 8), True),
            (Point(0, 9), False),
            (Point(15, 5), False),
            (Point(12, 4), True),
            (Point(10, 2), False),
            (Point(17, 10), True),
            (Point(14, 11), False)
        ]

        search_list = [
            (Point(8, 13), False, True),
            (Point(3, 6), True, True),
            (Point(6, 1), True, True),
            (Point(2, 3), False, True),
            (Point(5, 8), True, True),
            (Point(0, 9), False, False),
            (Point(15, 5), False, True),
            (Point(12, 4), True, True),
            (Point(10, 2), True, True),
            (Point(17, 10), False, False),
            (Point(14, 11), False, False)
        ]

        result = [
            Point(3, 6),
            Point(5, 8),
            Point(6, 1),
            Point(10, 2),
            Point(12, 4),
        ]

        ans = kd_tree(pts, rx, ry)

        self.assertEqual((ordered_x, ordered_y), next(ans))
        self.assertEqual(partition, next(ans))
        self.assertEqual(tree, next(ans))
        self.assertEqual(search_list, next(ans))
        self.assertEqual(result, sorted(next(ans)))

    def test_graham1(self):
        pts = [Point(7, 0), Point(3, 3), Point(0, 0)]
        centroid = Point(3.3333333333333335, 1.0)
        ordered = [Point(7, 0), Point(3, 3), Point(0, 0)]
        origin = Point(7, 0)
        steps = [
            ([ordered[0], ordered[1], ordered[2]], True),
            ([ordered[1], ordered[2], ordered[0]], True)
        ]
        hull = [Point(7, 0), Point(3, 3), Point(0, 0)]
        ans = graham(pts)
        
        self.assertAlmostEqual(centroid, next(ans))
        self.assertEqual(ordered, next(ans))
        self.assertEqual(origin, next(ans))
        self.assertEqual(steps, next(ans))
        self.assertEqual(hull, next(ans))

    def test_graham2(self):
        pts = [
            Point(3, 10),
            Point(6, 8),
            Point(3, 5),
            Point(2, 8),
            Point(4, 8),
            Point(5, 5),
            Point(3, 3),
            Point(7, 7),
            Point(5, 0),
            Point(0, 0),
            Point(10, 3),
        ]
        centroid = Point(4.0, 7.666666666666667)
        ordered = [
            Point(5, 0),
            Point(5, 5),
            Point(10, 3),
            Point(7, 7),
            Point(6, 8),
            Point(4, 8),
            Point(3, 10),
            Point(2, 8),
            Point(0, 0),
            Point(3, 5),
            Point(3, 3),
        ]
        origin = Point(5, 0)
        steps = [
            ([ordered[0], ordered[1], ordered[2]], False),
            ([ordered[0], ordered[2], ordered[3]], True),
            ([ordered[2], ordered[3], ordered[4]], True),
            ([ordered[3], ordered[4], ordered[5]], True),
            ([ordered[4], ordered[5], ordered[6]], False),
            ([ordered[3], ordered[4], ordered[6]], True),
            ([ordered[4], ordered[6], ordered[7]], True),
            ([ordered[6], ordered[7], ordered[8]], True),
            ([ordered[7], ordered[8], ordered[9]], True),
            ([ordered[8], ordered[9], ordered[10]], False),
            ([ordered[7], ordered[8], ordered[10]], True),
            ([ordered[8], ordered[10], ordered[0]], False),
            ([ordered[7], ordered[8], ordered[0]], True)
        ]
        hull = [
            Point(5, 0),
            Point(10, 3),
            Point(7, 7),
            Point(6, 8),
            Point(3, 10),
            Point(2, 8),
            Point(0, 0)
        ]
        ans = graham(pts)
        self.assertAlmostEqual(centroid, next(ans))
        self.assertEqual(ordered, next(ans))
        self.assertEqual(origin, next(ans))
        self.assertEqual(steps, next(ans))
        self.assertEqual(hull, next(ans))

    def test_graham3(self):
        pts = [
            Point(2, 8),
            Point(5, 6),
            Point(7, 8),
            Point(8, 11),
            Point(7, 5),
            Point(10, 7),
            Point(11, 5),
            Point(8, 2),
            Point(1, 3),
            Point(5, 2),
        ]
        centroid = Point(4.666666666666667, 7.333333333333333)
        ordered = [
            Point(8, 2),
            Point(7, 5),
            Point(11, 5),
            Point(10, 7),
            Point(7, 8),
            Point(8, 11),
            Point(2, 8),
            Point(1, 3),
            Point(5, 2),
            Point(5, 6)
        ]
        origin = Point(8, 2)
        steps = [
	        ([ordered[0], ordered[1], ordered[2]], False),
	        ([ordered[0], ordered[2], ordered[3]], True),
	        ([ordered[2], ordered[3], ordered[4]], True),
	        ([ordered[3], ordered[4], ordered[5]], False),
	        ([ordered[2], ordered[3], ordered[5]], False),
	        ([ordered[0], ordered[2], ordered[5]], True),
	        ([ordered[2], ordered[5], ordered[6]], True),
	        ([ordered[5], ordered[6], ordered[7]], True),
	        ([ordered[6], ordered[7], ordered[8]], True),
	        ([ordered[7], ordered[8], ordered[9]], True),
	        ([ordered[8], ordered[9], ordered[0]], False),
	        ([ordered[7], ordered[8], ordered[0]], True)
        ]
        hull = [
            Point(8, 2),
            Point(11, 5),
            Point(8, 11),
            Point(2, 8),
            Point(1, 3),
            Point(5, 2)
        ]
        ans = graham(pts)
        self.assertAlmostEqual(centroid, next(ans))
        self.assertEqual(ordered, next(ans))
        self.assertEqual(origin, next(ans))
        self.assertEqual(steps, next(ans))
        self.assertEqual(hull, next(ans))

    def test_quickhull1(self):
        pts = [Point(3, 4), Point(0, 0), Point(7, 2)]
        hull = [pts[1], pts[0], pts[2]]
        tree = BinTree(QuickhullNode([pts[1], pts[0], pts[2]], hull_piece=hull))
        tree.root.left = QuickhullNode([pts[1], pts[0], pts[2]], h=pts[0], hull_piece=hull)
        tree.root.right = QuickhullNode([pts[2], pts[1]], hull_piece=[pts[2], pts[1]])
        tree.root.left.left = QuickhullNode([pts[1], pts[0]], hull_piece=[pts[1], pts[0]])
        tree.root.left.right = QuickhullNode([pts[0], pts[2]], hull_piece=[pts[0], pts[2]])

        ans = quickhull(pts)
        lp, rp, s1, s2, _ = next(ans)
        
        self.assertEqual((pts[1], pts[2]), (lp, rp))
        self.assertEqual(([pts[1], pts[0], pts[2]], [pts[2], pts[1]]), (s1, s2))
        self.assertEqual(tree, next(ans))
        self.assertEqual(hull, next(ans))

    def test_quickhull2(self):
        pts = [
            Point(0, 6),
            Point(8, 11),
            Point(10, 4),
            Point(7, 13),
            Point(6, 3),
            Point(3, 0),
            Point(4, 2),
            Point(12, 1),
            Point(14, 10),
            Point(5, 9),
            Point(3, 11),
            Point(1, 4),
        ]
        hull = [pts[0], pts[10], pts[3], pts[8], pts[7], pts[5]]
        tree = BinTree(
            QuickhullNode(
                [
                    pts[0],
                    pts[10],
                    pts[9],
                    pts[3],
                    pts[1],
                    pts[8],
                    pts[7],
                    pts[2],
                    pts[4],
                    pts[6],
                    pts[5],
                    pts[11],
                ],
                hull_piece=hull
            )
        )

        tree.root.left = QuickhullNode(
            [pts[0], pts[10], pts[9], pts[3], pts[1], pts[8]],
            h=pts[3],
            hull_piece=[pts[0], pts[10], pts[3], pts[8]]
        )
        tree.root.right = QuickhullNode(
            [pts[8], pts[7], pts[2], pts[4], pts[6], pts[5], pts[11], pts[0]],
            h=pts[7],
            hull_piece=[pts[8], pts[7], pts[5], pts[0]]
        )

        tree.root.left.left = QuickhullNode([pts[0], pts[10], pts[3]], h=pts[10], hull_piece=[pts[0], pts[10], pts[3]])
        tree.root.left.right = QuickhullNode([pts[3], pts[8]], hull_piece=[pts[3], pts[8]])
        tree.root.left.left.left = QuickhullNode([pts[0], pts[10]], hull_piece=[pts[0], pts[10]])
        tree.root.left.left.right = QuickhullNode([pts[10], pts[3]], hull_piece=[pts[10], pts[3]])

        tree.root.right.left = QuickhullNode([pts[8], pts[7]], hull_piece=[pts[8], pts[7]])
        tree.root.right.right = QuickhullNode(
            [pts[7], pts[4], pts[6], pts[5], pts[11], pts[0]],
            h=pts[5],
            hull_piece=[pts[7], pts[5], pts[0]]
        )
        tree.root.right.right.left = QuickhullNode([pts[7], pts[5]], hull_piece=[pts[7], pts[5]])
        tree.root.right.right.right = QuickhullNode([pts[5], pts[0]], hull_piece=[pts[5], pts[0]])

        ans = quickhull(pts)
        lp, rp, s1, s2, _ = next(ans)

        self.assertEqual((pts[0], pts[8]), (lp, rp))
        self.assertEqual((tree.root.left.data.points, tree.root.right.data.points), (s1, s2))
        self.assertEqual(tree, next(ans))
        self.assertEqual(hull, next(ans))

    def test_loci(self):
        l = Loci()
        p1 = Point(1, 1)
        p2 = Point(2, 1)
        p3 = Point(2, 3)
        p4 = Point(2, 2)

        l.append_points(p1, p2, p3, p4)
        q = l.query(Point(2.5, 0.5))
        self.assertEqual(q, 0)
        res = l.get_points_in_rect(((1.5, 2.5), (0.5, 3.5)))
        res2 = l.get_points_in_rect(((0.5, 2.5), (0.5, 3.5)))

        self.assertEqual(res, 3)
        self.assertEqual(res2, 4)

        p1 = Point(2, 1)
        p2 = Point(1, 2)
        p3 = Point(0, 3)
        l = Loci()
        l.append_points(p1, p2, p3)
        res = l.get_points_in_rect(((0.5, 2.5), (0.5, 2.5)))
        self.assertEqual(res, 2)

    def test_chain_method(self):
        graph = OrientedGraph()
        point = Point(4, 5)
        v1 = Vertex(Point(4, 2))
        v2 = Vertex(Point(2, 4))
        v3 = Vertex(Point(6, 5))
        v4 = Vertex(Point(5, 7))

        e1 = OrientedEdge(v1, v2, 1)
        e2 = OrientedEdge(v1, v3, 1)
        e3 = OrientedEdge(v2, v3, 1)
        e4 = OrientedEdge(v2, v4, 1)
        e5 = OrientedEdge(v3, v4, 1)

        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        graph.add_vertex(v4)

        graph.add_edge(v1, v2, 1)
        graph.add_edge(v1, v3, 1)
        graph.add_edge(v2, v3, 1)
        graph.add_edge(v2, v4, 1)
        graph.add_edge(v3, v4, 1)

        ordered = [v1, v2, v3, v4]

        weight_table = OrderedDict(
            {
                v1: {"vin": [], "vout": [e1, e2], "win": 0, "wout": 2},
                v2: {"vin": [e1], "vout": [e4, e3], "win": 1, "wout": 2},
                v3: {"vin": [e3, e2], "vout": [e5], "win": 2, "wout": 1},
                v4: {"vin": [e4, e5], "vout": [], "win": 2, "wout": 0},
            }
        )

        e1_balanced = copy.deepcopy(e1)
        e1_balanced.weight = 2
        e5_balanced = copy.deepcopy(e5)
        e5_balanced.weight = 2
        weight_table_balanced = {
            v1: {"vin": [], "vout": [e1_balanced, e2], "win": 0, "wout": 3},
            v2: {"vin": [e1_balanced], "vout": [e4, e3], "win": 2, "wout": 2},
            v3: {"vin": [e3, e2], "vout": [e5_balanced], "win": 2, "wout": 2},
            v4: {"vin": [e4, e5_balanced], "vout": [], "win": 3, "wout": 0},
        }

        e1_new = deepcopy(e1)
        e1_new.weight = 0
        e2_new = deepcopy(e2)
        e2_new.weight = 0
        e3_new = deepcopy(e3)
        e3_new.weight = 0
        e4_new = deepcopy(e4)
        e4_new.weight = 0
        e5_new = deepcopy(e5)
        e5_new.weight = 0

        chains = [[e1_new, e4_new], [e1_new, e3_new, e5_new], [e2_new, e5_new]]

        root = NodeWithParent(data=chains[1])
        tree = ChainsBinTree(root)
        tree.root.left = NodeWithParent(data=chains[0], parent=root)
        tree.root.right = NodeWithParent(data=chains[2], parent=root)

        point_between = (chains[0], chains[1])

        ans = chain_method(graph, point)
        self.assertEqual(ordered, next(ans))
        self.assertEqual(weight_table, next(ans))
        self.assertEqual(weight_table_balanced, next(ans))
        self.assertEqual(chains, next(ans))
        self.assertEqual(tree, next(ans))
        self.assertEqual(point_between, next(ans))

    def test_closest_points(self):
        points_test = [Point(3, 3), Point(6, 2), Point(5, 6), Point(7, 4), Point(2, 9)]

        close_pair_true = (Point(6, 2), Point(7, 4))

        self.assertTupleEqual(closest_points(points_test), close_pair_true)

    def test_region_tree_method(self):
        pts = [Point(1, 9), Point(7, 13), Point(3, 3), Point(1.5, 3), Point(5, 7),
               Point(9, 8), Point(6, 9), Point(7, 5), Point(7, 12), Point(4, 11), Point(1, 5)]
        x_range, y_range = [2.2, 7.7], [6.6, 11.11]

        pre = (sorted(pts), sorted(sorted(pts), key=lambda u: u.y))
        projections = [
            [Point(1, 5), Point(1, 9)],
            [Point(1.5, 3)],
            [Point(3, 3)],
            [Point(4, 11)],
            [Point(5, 7)],
            [Point(6, 9)],
            [Point(7, 5), Point(7, 12), Point(7, 13)],
            [Point(9, 8)]
        ]

        tree = BinTree(Node([[1, 8], [Point(1.5, 3),
                                      Point(3, 3),
                                      Point(1, 5),
                                      Point(7, 5),
                                      Point(5, 7),
                                      Point(9, 8),
                                      Point(1, 9),
                                      Point(6, 9),
                                      Point(4, 11),
                                      Point(7, 12),
                                      Point(7, 13)]]))
        tree.root.left = Node([[1, 4], [Point(1.5, 3),
                                        Point(3, 3),
                                        Point(1, 5),
                                        Point(1, 9),
                                        Point(4, 11)]])
        tree.root.left.left = Node([[1, 2], [Point(1.5, 3), Point(1, 5), Point(1, 9)]])
        tree.root.left.right = Node([[2, 4], [Point(1.5, 3), Point(3, 3), Point(4, 11)]])
        tree.root.left.right.left = Node([[2, 3], [Point(1.5, 3), Point(3, 3)]])
        tree.root.left.right.right = Node([[3, 4], [Point(3, 3), Point(4, 11)]])

        tree.root.right = Node([[4, 8], [Point(7, 5),
                                         Point(5, 7),
                                         Point(9, 8),
                                         Point(6, 9),
                                         Point(4, 11),
                                         Point(7, 12),
                                         Point(7, 13)]])
        tree.root.right.left = Node([[4, 6], [Point(5, 7), Point(6, 9), Point(4, 11)]])
        tree.root.right.left.left = Node([[4, 5], [Point(5, 7), Point(4, 11)]])
        tree.root.right.left.right = Node([[5, 6], [Point(5, 7), Point(6, 9)]])
        tree.root.right.right = Node([[6, 8], [Point(7, 5),
                                               Point(9, 8),
                                               Point(6, 9),
                                               Point(7, 12),
                                               Point(7, 13)]])
        tree.root.right.right.left = Node([[6, 7], [Point(7, 5),
                                                    Point(6, 9),
                                                    Point(7, 12),
                                                    Point(7, 13)]])
        tree.root.right.right.right = Node([[7, 8], [Point(7, 5),
                                                     Point(9, 8),
                                                     Point(7, 12),
                                                     Point(7, 13)]])

        ps = [tree.root.left.right.right, tree.root.right.left, tree.root.right.right.left]
        ss = [[Point(4, 11)], [Point(5, 7), Point(6, 9), Point(4, 11)], [Point(6, 9)]]

        ans = region_tree_method(pts, x_range, y_range)
        self.assertEqual(pre, next(ans))
        self.assertEqual(projections, next(ans))
        self.assertEqual(tree, next(ans))
        self.assertEqual([3, 7], next(ans))
        self.assertEqual(ps, next(ans))
        self.assertEqual(ss, next(ans))
