from copy import deepcopy

from computer.circuit.point import Point
from computer.circuit.line import Line, Direction


class shortcircuit_detector:

    def __init__(self):
        pass

    def detect_line_intersection(self, first_line, second_line):
        line_one = deepcopy(first_line)
        line_one.normalize()
        line_two = deepcopy(second_line)
        line_two.normalize()
        
        if line_one.direction == line_two.direction:
            if line_one.fixed_coordinate != line_two.fixed_coordinate:
                return None
            if line_one.end == line_two.start:
                return line_one.get_end_point()
            if line_one.start == line_two.end:
                return line_one.get_start_point()

            if line_two.contains(line_one.start):
                if line_two.contains(line_one.end):
                    return deepcopy(line_one)
                else:
                    return Line(line_one.direction, line_one.fixed_coordinate, line_one.start, line_two.end)
            elif line_two.contains(line_one.end):
                return Line(line_one.direction, line_one.fixed_coordinate, line_two.start, line_one.end)
            elif line_one.contains(line_two.start):
                return deepcopy(line_two)

        if line_one.start == line_two.fixed_coordinate \
                or line_one.start < line_two.fixed_coordinate != line_one.end >= line_two.fixed_coordinate:
            if line_one.direction == Direction.Horizontal:
                return Point(line_two.fixed_coordinate, line_one.fixed_coordinate)
            else:
                return Point(line_one.fixed_coordinate, line_two.fixed_coordinate)
        return None

    def detect_intersections(self, first_wire, second_wire):
        intersections = []
        for first_line in first_wire.sections:
            for second_line in second_wire.sections:
                intersection = self.detect_line_intersection(first_line, second_line)
                if intersection is not None:
                    intersections.append(intersection)
        return intersections
