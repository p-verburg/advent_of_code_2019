from computer.intcode_computer import IntcodeComputer, ListInput, ListOutput

input = ListInput([1])
output = ListOutput()
computer = IntcodeComputer(input, output)

initial_memory = []
input_file = open("input.txt", 'r')
for line in input_file:
    initial_memory.extend([int(code) for code in line.split(',')])
computer.reset_memory(initial_memory)

computer.run_program()

print(output.list)
