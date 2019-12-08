class CircuitMapReader:
    wires = []
    builder = None

    def __init__(self, builder):
        self.wires = []
        self.builder = builder

    def parse_line(self, line):
        self.builder.reset()
        circuit_lines = line.split(',')
        for circuit_line in circuit_lines:
            direction = circuit_line[0]
            distance = int(circuit_line[1:])
            if direction == 'R':
                self.builder.right(distance)
            elif direction == 'L':
                self.builder.left(distance)
            elif direction == 'U':
                self.builder.up(distance)
            elif direction == 'D':
                self.builder.down(distance)

        self.wires.append(self.builder.wire)

    def read(self, lines):
        for line in lines:
            self.parse_line(line)
        return self.wires
