import unittest
from computer.intcode_computer import IntcodeComputer
from computer.io import SingleInput, LastOutput
from computer.programs.operations import OperationCode


class InstructionTests(unittest.TestCase):
    @staticmethod
    def create_computer(memory):
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

        self.assertEqual(4, pointer)
        self.assertEqual(99, computer._memory[4])

    def test_multiply_instruction_negative(self):
        computer = self.create_computer([1101, 100, -1, 4, 0])

        pointer = computer.execute_instruction(0)

        self.assertEqual(4, pointer)
        self.assertEqual(99, computer._memory[4])


class SingleProgramTests(unittest.TestCase):
    def single_program_test(self, expected, memory):
        computer = IntcodeComputer()
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


class InputOutputProgramTests(unittest.TestCase):
    @staticmethod
    def run_program(memory, input, output):
        computer = IntcodeComputer(input, output)
        computer.reset_memory(memory)
        computer.run_program()

    def input_output_test(self, input_value, program, expected_output):
        input = SingleInput(input_value)
        output = LastOutput()

        self.run_program(program, input, output)

        self.assertEqual(expected_output, output)

    def test_input_output_program(self):
        self.input_output_test(34, [3, 0, 4, 0, 99], 34)

    def test_equal_position_mode_false(self):
        self.input_output_test(7, [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 0)

    def test_equal_position_mode_true(self):
        self.input_output_test(8, [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 1)

    def test_less_than_position_mode_false(self):
        self.input_output_test(12, [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 0)

    def test_less_than_position_mode_true(self):
        self.input_output_test(6, [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 1)

    def test_equal_immediate_mode_false(self):
        self.input_output_test(7, [3, 3, 1108, -1, 8, 3, 4, 3, 99], 0)

    def test_equal_immediate_mode_true(self):
        self.input_output_test(8, [3, 3, 1108, -1, 8, 3, 4, 3, 99], 1)

    def test_less_than_immediate_mode_false(self):
        self.input_output_test(12, [3, 3, 1107, -1, 8, 3, 4, 3, 99], 0)

    def test_less_than_immediate_mode_true(self):
        self.input_output_test(6, [3, 3, 1107, -1, 8, 3, 4, 3, 99], 1)

    def test_jump_if_zero_position_mode_false(self):
        self.input_output_test(3, [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1)

    def test_jump_if_zero_position_mode_true(self):
        self.input_output_test(0, [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0)

    def test_jump_if_zero_immediate_mode_false(self):
        self.input_output_test(3, [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1)

    def test_jump_if_zero_immediate_mode_true(self):
        self.input_output_test(0, [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0)

    def test_less_than_equal_or_greater_less(self):
        self.input_output_test(7, [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                                   1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                                   999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 999)

    def test_less_than_equal_or_greater_equal(self):
        self.input_output_test(8, [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                                   1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                                   999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 1000)

    def test_less_than_equal_or_greater_greater(self):
        self.input_output_test(9, [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                                   1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                                   999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 1001)


if __name__ == '__main__':
    unittest.main()
