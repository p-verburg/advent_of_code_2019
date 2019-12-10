from computer.intcode_computer import IntcodeComputer
from computer.io import SingleInput, LastOutput

# input = SingleInput(1)
input = SingleInput(5)
output = LastOutput()
computer = IntcodeComputer(input, output)

initial_memory = []
input_file = open("input.txt", 'r')
for line in input_file:
    initial_memory.extend([int(code) for code in line.split(',')])
computer.reset_memory(initial_memory)

computer.run_program()

print(output.value)
