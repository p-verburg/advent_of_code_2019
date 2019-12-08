import unittest
from computer.intcode_computer import operation, intcode_computer


class InstructionTestCase(unittest.TestCase):
    def test_parse_operation(self):
        code = operation(1)
        self.assertEqual(operation.ADD, code)

    @staticmethod
    def compute_instruction(memory, pointer):
        computer = intcode_computer()
        return computer.compute_instruction(memory, pointer)

    def test_halt_instruction(self):
        memory = [99]
        pointer = self.compute_instruction(memory, 0)
        self.assertEqual(-1, pointer)
        self.assertEqual([99], memory)

    def test_add_instruction(self):
        memory = [4, 8, 5, 1, 1, 2, 0, 99]
        pointer = self.compute_instruction(memory, 3)
        self.assertEqual(7, pointer)
        self.assertEqual([13, 8, 5, 1, 1, 2, 0, 99], memory)

    def test_multiply_instruction(self):
        memory = [4, 8, 5, 2, 1, 2, 0, 99]
        pointer = self.compute_instruction(memory, 3)
        self.assertEqual(7, pointer)
        self.assertEqual([40, 8, 5, 2, 1, 2, 0, 99], memory)


class ProgramTestCase(unittest.TestCase):

    def single_program_test(self, expected, memory):
        computer = intcode_computer()
        computer.compute_program(memory)
        self.assertEqual(expected, memory)

    def test_program_1(self):
        self.single_program_test(
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])

    def test_program_2(self):
        self.single_program_test(
            [2, 0, 0, 0, 99],
            [1, 0, 0, 0, 99])

    def test_program_3(self):
        self.single_program_test(
            [2, 3, 0, 6, 99],
            [2, 3, 0, 3, 99])

    def test_program_4(self):
        self.single_program_test(
            [2, 4, 4, 5, 99, 9801],
            [2, 4, 4, 5, 99, 0])

    def test_program_5(self):
        self.single_program_test(
            [30, 1, 1, 4, 2, 5, 6, 0, 99],
            [1, 1, 1, 4, 99, 5, 6, 0, 99])


if __name__ == '__main__':
    unittest.main()
