import unittest

from computer.programs.memory import Memory
from computer.programs.operations import OperationFactory, OperationCode
from tests.computer_mocks import MockConstantInput, MockListOutput, MockParameter


class OperationsTests(unittest.TestCase):
    _memory = Memory()
    _input = MockConstantInput()
    _output = MockListOutput()
    _operation_factory = OperationFactory(_memory, _input, _output)

    def test_add_operation(self):
        parameters = [MockParameter(11), MockParameter(7), MockParameter(0)]
        operation = self._operation_factory.create_operation(OperationCode.ADD)

        operation.execute(parameters, None, None)

        self.assertEqual(None, parameters[0].set_value)
        self.assertEqual(None, parameters[1].set_value)
        self.assertEqual(18, parameters[2].set_value)

    def test_multiply_operation(self):
        parameters = [MockParameter(11), MockParameter(7), MockParameter(0)]
        operation = self._operation_factory.create_operation(OperationCode.MULTIPLY)

        operation.execute(parameters, None, None)

        self.assertEqual(None, parameters[0].set_value)
        self.assertEqual(None, parameters[1].set_value)
        self.assertEqual(77, parameters[2].set_value)

    def test_input_operation(self):
        parameters = [MockParameter(4)]
        input = MockConstantInput(17)
        operation = self._operation_factory.create_operation(OperationCode.INPUT)

        operation.execute(parameters, input, None)

        self.assertEqual(17, parameters[0].set_value)

    def test_output_operation(self):
        parameters = [MockParameter(7)]
        output = MockListOutput()
        operation = self._operation_factory.create_operation(OperationCode.OUTPUT)

        operation.execute(parameters, None, output)

        self.assertEqual([7], output.list)

    def test_halt_operation(self):
        parameters = [MockParameter(11), MockParameter(7), MockParameter(0)]
        operation = self._operation_factory.create_operation(OperationCode.END)

        operation.execute(parameters, None, None)

        self.assertEqual(None, parameters[0].set_value)
        self.assertEqual(None, parameters[1].set_value)
        self.assertEqual(None, parameters[2].set_value)


if __name__ == '__main__':
    unittest.main()
