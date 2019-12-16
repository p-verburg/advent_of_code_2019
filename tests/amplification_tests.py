import copy
import unittest

from computer.amplification import AmplifierPipeline, Amplifier, AmplificationOptimizer


class TestProgram:
    def __init__(self, program, phases, max_signal):
        self.program = program
        self.phases = phases
        self.max_signal = max_signal


test1 = TestProgram([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], [4, 3, 2, 1, 0], 43210)
test2 = TestProgram([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0],
                    [0, 1, 2, 3, 4], 54321)
test3 = TestProgram([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
                     1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0], [1, 0, 4, 3, 2], 65210)


class AmplifierTests(unittest.TestCase):
    def test_phase_to_output(self):
        amplifier = Amplifier([3, 0, 4, 0, 99], 12)
        output = amplifier.calculate(71)

        self.assertEqual(12, output)


class AmplifierPipelineTests(unittest.TestCase):
    def program_test(self, test):
        test = copy.deepcopy(test)
        pipeline = AmplifierPipeline(test.program, test.phases)

        signal = pipeline.calculate_signal(0)

        self.assertEqual(test.max_signal, signal)

    def test_program1(self):
        self.program_test(test1)

    def test_program2(self):
        self.program_test(test2)

    def test_program3(self):
        self.program_test(test3)


class AmplificationOptimizerTests(unittest.TestCase):
    def test_generate_permutations(self):
        optimizer = AmplificationOptimizer(None, [0, 1, 2])

        permutations = list(optimizer.permutations())

        self.assertEqual(6, len(permutations))
        self.assertTrue((0, 1, 2) in permutations)
        self.assertTrue((0, 2, 1) in permutations)
        self.assertTrue((1, 0, 2) in permutations)
        self.assertTrue((1, 2, 0) in permutations)
        self.assertTrue((2, 0, 1) in permutations)
        self.assertTrue((2, 1, 0) in permutations)

    def optimize_amplification(self, test):
        optimizer = AmplificationOptimizer(test.program, [0, 1, 2, 3, 4])

        phases, signal = optimizer.optimize(0)

        self.assertEqual(phases, test.phases)
        self.assertEqual(signal, test.max_signal)

    def optimizes_program1(self):
        self.optimize_amplification(test1)

    def optimizes_program2(self):
        self.optimize_amplification(test2)

    def optimizes_program3(self):
        self.optimize_amplification(test3)


if __name__ == '__main__':
    unittest.main()
