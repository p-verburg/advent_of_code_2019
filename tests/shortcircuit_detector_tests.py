import unittest

from computer.circuit.point import Point
from computer.circuit.line import HorizontalLine, VerticalLine
from computer.circuit.reader import CircuitMapReader
from computer.circuit.wire import WireLayer
from computer.shortcircuit_detector import ShortCircuitDetector


class ShortCircuitDetectorLineIntersectionTestCase(unittest.TestCase):
    @staticmethod
    def check_lines_intersect(first_line, second_line):
        detector = ShortCircuitDetector()
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

    def test_crossing_lines_intersect2(self):
        self.lines_intersect_test(None, HorizontalLine(1, 1, 9), VerticalLine(7, 6, 4))

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
        detector = ShortCircuitDetector()
        return detector.detect_intersections(first_wire, second_wire)

    @staticmethod
    def find_closest_intersection(first_wire, second_wire):
        detector = ShortCircuitDetector()
        return detector.find_closest_intersection(first_wire, second_wire)

    @staticmethod
    def create_test_data_1():
        first_wire = WireLayer().right(8).up(5).left(5).down(3).wire
        second_wire = WireLayer().up(7).right(6).down(4).left(4).wire
        return first_wire, second_wire

    def test_intersections_wires_1(self):
        first_wire, second_wire = self.create_test_data_1()

        intersections = self.find_intersections(first_wire, second_wire)

        self.assertCountEqual([Point(0, 0), Point(6, 5), Point(3, 3)], intersections)

    def test_find_closest_intersection_1(self):
        first_wire, second_wire = self.create_test_data_1()

        intersection = self.find_closest_intersection(first_wire, second_wire)

        self.assertEqual(Point(3, 3), intersection.location)
        self.assertEqual(6, intersection.distance)

    @staticmethod
    def create_test_data_2():
        first_wire = WireLayer().right(75).down(30).right(83).up(83).left(12) \
            .down(49).right(71).up(7).left(72).wire
        second_wire = WireLayer().up(62).right(66).up(55).right(34) \
            .down(71).right(55).down(58).right(83).wire
        return first_wire, second_wire

    def test_find_closest_intersection_2(self):
        first_wire, second_wire = self.create_test_data_2()

        intersection = self.find_closest_intersection(first_wire, second_wire)

        self.assertEqual(159, intersection.distance)

    @staticmethod
    def create_test_data_3():
        first_wire = WireLayer().right(98).up(47).right(26).down(63) \
            .right(33).up(87).left(62).down(20) \
            .right(33).up(53).right(51).wire
        second_wire = WireLayer().up(98).right(91).down(20).right(16) \
            .down(67).right(40).up(7).right(15) \
            .up(6).right(7).wire
        return first_wire, second_wire

    def test_find_closest_intersection_3(self):
        first_wire, second_wire = self.create_test_data_3()

        intersection = self.find_closest_intersection(first_wire, second_wire)

        self.assertEqual(135, intersection.distance)


class CircuitMapParserTestCase(unittest.TestCase):
    class MockBuilder:
        wire = []

        def __init__(self):
            self.wire = []

        def reset(self):
            self.wire = []

        def up(self, distance):
            self.wire.append("U{}".format(distance))

        def down(self, distance):
            self.wire.append("D{}".format(distance))

        def right(self, distance):
            self.wire.append("R{}".format(distance))

        def left(self, distance):
            self.wire.append("L{}".format(distance))

    def test_reads_circuit(self):
        lines = ["R75,D30,R83,U83,L12,D49,R71,U7,L72",
                 "U62,R66,U55,R34,D71,R55,D58,R83"]

        parser = CircuitMapReader(self.MockBuilder())
        wires = parser.read(lines)

        self.assertSequenceEqual(["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"], wires[0])
        self.assertSequenceEqual(["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"], wires[1])


if __name__ == '__main__':
    unittest.main()
