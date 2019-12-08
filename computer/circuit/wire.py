from computer.circuit.line import Line, HorizontalLine, VerticalLine
from computer.circuit.point import Point


class Wire:
    sections = []

    def __int__(self):
        self.sections = []


class WireLayer:
    head = Point()
    wire = Wire()

    def __init__(self, start_x, start_y):
        self.head = Point(start_x, start_y)
        self.wire = Wire()

    def add_line(self, line):
        self.wire.sections.append(line)
        self.head = line.get_end_point()

    def right(self, distance):
        self.add_line(HorizontalLine(self.head.y, self.head.x, self.head.x + distance))
        return self

    def left(self, distance):
        self.right(-distance)
        return self

    def up(self, distance):
        self.add_line(VerticalLine(self.head.x, self.head.y, self.head.y + distance))
        return self

    def down(self, distance):
        self.up(-distance)
        return self
