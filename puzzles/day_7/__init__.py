from computer.amplification import AmplificationOptimizer

program = []
input_file = open("amplification_program.txt", 'r')
for line in input_file:
    program.extend([int(code) for code in line.split(',')])
optimizer = AmplificationOptimizer(program, [0, 1, 2, 3, 4])

phases, max_signal = optimizer.optimize(0)

print("Maximum signal {} achieved with phase settings {}".format(max_signal, phases))
