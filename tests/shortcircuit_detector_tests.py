import unittest

from computer.circuit.point import Point
from computer.circuit.line import Line, HorizontalLine, VerticalLine, Direction
from computer.circuit.wire import Wire, WireLayer
from computer.shortcircuit_detector import shortcircuit_detector


class ShortCircuitDetectorLineIntersectionTestCase(unittest.TestCase):
    @staticmethod
    def check_lines_intersect(first_line, second_line):
        detector = shortcircuit_detector()
        return detector.detect_line_intersection(first_line, second_line)

    def lines_intersect_test(self, expected_result, first_line, second_line):
        intersection = self.check_lines_intersect(first_line, second_line)
        self.assertEqual(expected_result, intersection)

    def test_vertical_parallel_lines_dont_intersect(self):
        self.lines_intersect_test(None, VerticalLine(0, 0, 5), VerticalLine(1, 0, 5))

    def test_horizontal_parallel_lines_dont_intersect(self):
        self.lines_intersect_test(None, HorizontalLine(0, 0, 5), HorizontalLine(1, 0, 5))

    def test_crossing_lines_intersect(self):
        self.lines_intersect_test(Point(2, 2), HorizontalLine(2, 0, 5), VerticalLine(2, 0, 5))

    def test_touching_lines_intersect(self):
        self.lines_intersect_test(Point(0, 2), HorizontalLine(2, 0, 5), VerticalLine(0, 0, 5))

    def test_continuing_lines_intersect(self):
        self.lines_intersect_test(Point(5, 0), HorizontalLine(0, 0, 5), HorizontalLine(0, 5, 7))

    def test_end_start_overlap(self):
        self.lines_intersect_test(HorizontalLine(0, 2, 3), HorizontalLine(0, 0, 3), HorizontalLine(0, 2, 4))

    def test_start_end_overlap(self):
        self.lines_intersect_test(HorizontalLine(0, 2, 3), HorizontalLine(0, 2, 4), HorizontalLine(0, 0, 3))

    def test_containing_overlap(self):
        self.lines_intersect_test(HorizontalLine(0, 1, 4), HorizontalLine(0, 0, 5), HorizontalLine(0, 1, 4))

    def test_contained_by_overlap(self):
        self.lines_intersect_test(HorizontalLine(0, 1, 4), HorizontalLine(0, 1, 4), HorizontalLine(0, 0, 5))

    def test_contained_by_overlap_inverse(self):
        self.lines_intersect_test(HorizontalLine(0, 1, 4), HorizontalLine(0, 4, 1), HorizontalLine(0, 0, 5))


class ShortCircuitDetectorWireIntersectionsTestCase(unittest.TestCase):
    @staticmethod
    def find_intersections(first_wire, second_wire):
        detector = shortcircuit_detector()
        return detector.detect_intersections(first_wire, second_wire)

    def test_intersections_wires_1(self):
        self.maxDiff = None
        layer1 = WireLayer(1, 1)
        first_wire = layer1.right(8).up(5).left(5).down(3).wire
        layer2 = WireLayer(1, 1)
        second_wire = layer2.up(7).right(6).down(4).left(4).wire

        intersections = self.find_intersections(first_wire, second_wire)

        self.assertCountEqual([Point(0, 0), Point(7, 6), Point(4, 4)], intersections)


if __name__ == '__main__':
    unittest.main()
