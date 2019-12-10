import unittest

from computer.io import LastOutput, SingleInput, NoneInput
from computer.programs.memory import Memory
from computer.programs.operations import OperationFactory, OperationCode
from tests.computer_mocks import MockParameter


class OperationsTests(unittest.TestCase):
    _memory = Memory()
    _input = NoneInput()
    _output = LastOutput()
    _operation_factory = OperationFactory(_memory, _input, _output)

    def test_add_operation(self):
        parameters = [MockParameter(11), MockParameter(7), MockParameter(0)]
        operation = self._operation_factory.create_operation(OperationCode.ADD)

        operation.execute(parameters, None, None)

        self.assertEqual(None, parameters[0].set_value)
        self.assertEqual(None, parameters[1].set_value)
        self.assertEqual(18, parameters[2].set_value)

    def test_add_advances_pointer(self):
        operation = self._operation_factory.create_operation(OperationCode.ADD)

        self.assertEqual(7, operation.get_new_pointer(3))

    def test_multiply_operation(self):
        parameters = [MockParameter(11), MockParameter(7), MockParameter(0)]
        operation = self._operation_factory.create_operation(OperationCode.MULTIPLY)

        operation.execute(parameters, None, None)

        self.assertEqual(None, parameters[0].set_value)
        self.assertEqual(None, parameters[1].set_value)
        self.assertEqual(77, parameters[2].set_value)

    def test_multiply_advances_pointer(self):
        operation = self._operation_factory.create_operation(OperationCode.MULTIPLY)

        self.assertEqual(7, operation.get_new_pointer(3))

    def test_input_operation(self):
        parameters = [MockParameter(4)]
        input = SingleInput(17)
        operation = self._operation_factory.create_operation(OperationCode.INPUT)

        operation.execute(parameters, input, None)

        self.assertEqual(17, parameters[0].set_value)

    def test_input_advances_pointer(self):
        operation = self._operation_factory.create_operation(OperationCode.INPUT)

        self.assertEqual(5, operation.get_new_pointer(3))

    def test_output_operation(self):
        parameters = [MockParameter(7)]
        output = LastOutput()
        operation = self._operation_factory.create_operation(OperationCode.OUTPUT)

        operation.execute(parameters, None, output)

        self.assertEqual(7, output)

    def test_output_advances_pointer(self):
        operation = self._operation_factory.create_operation(OperationCode.OUTPUT)

        self.assertEqual(5, operation.get_new_pointer(3))

    def test_jump_if_true_jumps(self):
        parameters = [MockParameter(17), MockParameter(39)]
        operation = self._operation_factory.create_operation(OperationCode.JUMP_IF_TRUE)

        operation.execute(parameters, None, None)

        self.assertEqual(39, operation.get_new_pointer(9))

    def test_jump_if_true_doesnt(self):
        parameters = [MockParameter(0), MockParameter(39)]
        operation = self._operation_factory.create_operation(OperationCode.JUMP_IF_TRUE)

        operation.execute(parameters, None, None)

        self.assertEqual(12, operation.get_new_pointer(9))

    def test_jump_if_false_jumps(self):
        parameters = [MockParameter(0), MockParameter(39)]
        operation = self._operation_factory.create_operation(OperationCode.JUMP_IF_FALSE)

        operation.execute(parameters, None, None)

        self.assertEqual(39, operation.get_new_pointer(9))

    def test_jump_if_false_doesnt(self):
        parameters = [MockParameter(17), MockParameter(39)]
        operation = self._operation_factory.create_operation(OperationCode.JUMP_IF_FALSE)

        operation.execute(parameters, None, None)

        self.assertEqual(12, operation.get_new_pointer(9))

    def test_less_than_operation(self):
        parameters = [MockParameter(231), MockParameter(11232), MockParameter(23)]
        operation = self._operation_factory.create_operation(OperationCode.LESS_THAN)

        operation.execute(parameters, None, None)

        self.assertEqual(1, parameters[2].set_value)

    def test_less_than_operation_if_equal(self):
        parameters = [MockParameter(231), MockParameter(231), MockParameter(23)]
        operation = self._operation_factory.create_operation(OperationCode.LESS_THAN)

        operation.execute(parameters, None, None)

        self.assertEqual(0, parameters[2].set_value)

    def test_less_than_operation_if_greater(self):
        parameters = [MockParameter(1231), MockParameter(231), MockParameter(23)]
        operation = self._operation_factory.create_operation(OperationCode.LESS_THAN)

        operation.execute(parameters, None, None)

        self.assertEqual(0, parameters[2].set_value)

    def test_less_than_advances_pointer(self):
        operation = self._operation_factory.create_operation(OperationCode.LESS_THAN)

        self.assertEqual(17, operation.get_new_pointer(13))

    def test_equals_operation(self):
        parameters = [MockParameter(231), MockParameter(231), MockParameter(23)]
        operation = self._operation_factory.create_operation(OperationCode.EQUALS)

        operation.execute(parameters, None, None)

        self.assertEqual(1, parameters[2].set_value)

    def test_equals_operation_if_less(self):
        parameters = [MockParameter(231), MockParameter(2315), MockParameter(23)]
        operation = self._operation_factory.create_operation(OperationCode.EQUALS)

        operation.execute(parameters, None, None)

        self.assertEqual(0, parameters[2].set_value)

    def test_equals_operation_if_greater(self):
        parameters = [MockParameter(1231), MockParameter(231), MockParameter(23)]
        operation = self._operation_factory.create_operation(OperationCode.EQUALS)

        operation.execute(parameters, None, None)

        self.assertEqual(0, parameters[2].set_value)

    def test_equals_advances_pointer(self):
        operation = self._operation_factory.create_operation(OperationCode.EQUALS)

        self.assertEqual(17, operation.get_new_pointer(13))

    def test_halt_operation(self):
        parameters = [MockParameter(11), MockParameter(7), MockParameter(0)]
        operation = self._operation_factory.create_operation(OperationCode.END)

        operation.execute(parameters, None, None)

        self.assertEqual(None, parameters[0].set_value)
        self.assertEqual(None, parameters[1].set_value)
        self.assertEqual(None, parameters[2].set_value)


if __name__ == '__main__':
    unittest.main()
