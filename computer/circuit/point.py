class Point:
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return 23 + 17 * hash(self.x) + 17 * hash(self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


def distance(first_point, second_point):
    return abs(first_point.x - second_point.x) + abs(first_point.y - second_point.y)
