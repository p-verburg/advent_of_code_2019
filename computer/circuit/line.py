from enum import IntEnum

from computer.circuit.point import Point


class Direction(IntEnum):
    Horizontal = 0,
    Vertical = 1


class Line:
    direction = Direction.Horizontal
    fixed_coordinate = 0
    start = 0
    end = 0

    def __init__(self, direction, position=0, start=0, end=0):
        self.direction = direction
        self.fixed_coordinate = position
        self.start = start
        self.end = end

    def __eq__(self, other):
        return isinstance(other, Line) \
               and other.direction == self.direction \
               and other.fixed_coordinate == self.fixed_coordinate \
               and other.start == self.start \
               and other.end == self.end

    def __str__(self):
        return "{} to {}".format(self.get_start_point(), self.get_end_point())

    def __hash__(self):
        return 19 + 31 * hash(int(self.direction)) \
               + 31 * hash(self.fixed_coordinate) \
               + 31 * hash(self.start) \
               + 31 * hash(self.end)

    @staticmethod
    def from_points(first_point, second_point):
        if first_point.x == second_point.x:
            return VerticalLine(first_point.x, first_point.y, second_point.y)
        elif first_point.y == second_point.y:
            return HorizontalLine(first_point.y, first_point.x, second_point.x)
        raise ValueError

    def normalize(self):
        if self.end < self.start:
            self.start, self.end = self.end, self.start
            return True
        return False

    def length(self):
        return abs(self.end - self.start)

    def get_end_point(self):
        if self.direction == Direction.Horizontal:
            return Point(self.end, self.fixed_coordinate)
        else:
            return Point(self.fixed_coordinate, self.end)

    def get_start_point(self):
        if self.direction == Direction.Horizontal:
            return Point(self.start, self.fixed_coordinate)
        else:
            return Point(self.fixed_coordinate, self.start)

    def contains(self, position):
        return (self.start >= position >= self.end) or (self.start <= position <= self.end)


class HorizontalLine(Line):
    def __init__(self, position=0, start=0, end=0):
        Line.__init__(self, Direction.Horizontal, position, start, end)

    def __eq__(self, other):
        return Line.__eq__(self, other)

    def __str__(self):
        return Line.__str__(self)


class VerticalLine(Line):
    def __init__(self, position=0, start=0, end=0):
        Line.__init__(self, Direction.Vertical, position, start, end)

    def __eq__(self, other):
        return Line.__eq__(self, other)

    def __str__(self):
        return Line.__str__(self)
