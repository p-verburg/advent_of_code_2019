import copy
import itertools
import sys

from computer.intcode_computer import IntcodeComputer
from computer.io import ListInput, LastOutput


class Amplifier:
    def __init__(self, program, phase):
        self._program = program
        self._phase = phase

    def calculate(self, input_value):
        input = ListInput([self._phase, input_value])
        output = LastOutput()
        computer = IntcodeComputer(input, output)
        computer.reset_memory(self._program)

        computer.run_program()

        return output.value


class AmplifierPipeline:
    def __init__(self, program, phase_sequence=[]):
        self._amplifiers = []
        for phase in phase_sequence:
            amplifier = Amplifier(copy.deepcopy(program), phase)
            self._amplifiers.append(amplifier)

    def calculate_signal(self, input_value):
        for amplifier in self._amplifiers:
            input_value = amplifier.calculate(input_value)
        return input_value


class AmplificationOptimizer:
    def __init__(self, program, phases):
        self._program = program
        self._phases = phases

    def permutations(self):
        return itertools.permutations(self._phases)

    def optimize(self, input):
        max_signal = -sys.maxsize - 1
        optimal_phases = None
        for phases in self.permutations():
            pipeline = AmplifierPipeline(self._program, list(phases))
            signal = pipeline.calculate_signal(input)
            if signal > max_signal:
                max_signal = signal
                optimal_phases = list(phases)

        return optimal_phases, max_signal
