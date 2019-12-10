import unittest
from computer.intcode_computer import IntcodeComputer, ListOutput
from computer.programs.operations import OperationCode
from tests.computer_mocks import MockConstantInput


class InstructionTests(unittest.TestCase):
    def create_computer(self, memory):
        computer = IntcodeComputer()
        computer.reset_memory(memory)
        return computer

    def test_parse_operation(self):
        code = OperationCode(1)
        self.assertEqual(OperationCode.ADD, code)

    def test_halt_instruction(self):
        computer = self.create_computer([99])

        pointer = computer.execute_instruction(0)

        self.assertEqual(-1, pointer)
        self.assertEqual([99], computer._memory._data)

    def test_add_instruction(self):
        computer = self.create_computer([4, 8, 5, 1, 1, 2, 0, 99])

        pointer = computer.execute_instruction(3)

        self.assertEqual(7, pointer)
        self.assertEqual([13, 8, 5, 1, 1, 2, 0, 99], computer._memory._data)

    def test_multiply_instruction(self):
        computer = self.create_computer([4, 8, 5, 2, 1, 2, 0, 99])

        pointer = computer.execute_instruction(3)

        self.assertEqual(7, pointer)
        self.assertEqual([40, 8, 5, 2, 1, 2, 0, 99], computer._memory._data)

    def test_multiply_instruction_modes(self):
        computer = self.create_computer([1002, 4, 3, 4, 33])

        pointer = computer.execute_instruction(0)

        self.assertEqual(99, computer._memory[4])

    def test_multiply_instruction_negative(self):
        computer = self.create_computer([1101, 100, -1, 4, 0])

        pointer = computer.execute_instruction(0)

        self.assertEqual(99, computer._memory[4])


class ProgramTests(unittest.TestCase):

    def single_program_test(self, expected, memory, input=None, output=None):
        computer = IntcodeComputer(input, output)
        computer.reset_memory(memory)
        computer.run_program()
        self.assertEqual(expected, computer._memory._data)

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

    def test_input_output_program(self):
        input = MockConstantInput(34)
        output = ListOutput()
        self.single_program_test(
            [34, 0, 4, 0, 99],
            [3, 0, 4, 0, 99],
            input, output)

        self.assertEqual([34], output.list)


if __name__ == '__main__':
    unittest.main()
