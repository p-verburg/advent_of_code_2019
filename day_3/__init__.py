from computer.circuit.reader import CircuitMapReader
from computer.circuit.wire import WireLayer
from computer.shortcircuit_detector import ShortCircuitDetector

file = open("Circuit.txt", 'r')
builder = WireLayer()
reader = CircuitMapReader(builder)

detector = ShortCircuitDetector()

wires = reader.read(file)
distance = detector.find_closest_intersection(wires[0], wires[1]).distance

print("Minimum distance of intersection: ", distance)


