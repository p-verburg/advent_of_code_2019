import unittest

from computer.programs.memory import Memory
from computer.programs.parameters import ParameterFactory, ImmediateParameter, PositionParameter


class ParametersTests(unittest.TestCase):
    def test_get_immediate_parameter(self):
        memory = Memory([2, 4, 15, 12])
        pointer = 2
        parameter = ImmediateParameter(memory, pointer)

        value = parameter.get()

        self.assertEqual(15, value)

    def test_set_immediate_parameter(self):
        memory = Memory([2, 4, 15, 12])
        pointer = 1
        parameter = ImmediateParameter(memory, pointer)

        parameter.set(57)

        self.assertEqual(57, memory[1])

    def test_get_position_parameter(self):
        memory = Memory([2, 3, 15, 12])
        pointer = 1
        parameter = PositionParameter(memory, pointer)

        value = parameter.get()

        self.assertEqual(12, value)

    def test_set_position_parameter(self):
        memory = Memory([2, 3, 15, 12])
        pointer = 0
        parameter = PositionParameter(memory, pointer)

        parameter.set(73)

        self.assertEqual(73, memory[2])


class ParameterFactoryTests(unittest.TestCase):
    def test_creates_immediate_parameter(self):
        memory = Memory()
        factory = ParameterFactory(memory)
        pointer = 3

        parameter = factory.create_parameter(1, pointer)

        self.assertTrue(isinstance(parameter, ImmediateParameter))
        self.assertEqual(memory, parameter._memory)
        self.assertEqual(pointer, parameter._pointer)

    def test_creates_position_parameter(self):
        memory = Memory()
        factory = ParameterFactory(memory)
        pointer = 7

        parameter = factory.create_parameter(0, pointer)

        self.assertTrue(isinstance(parameter, PositionParameter))
        self.assertEqual(memory, parameter._memory)
        self.assertEqual(pointer, parameter._pointer)


if __name__ == '__main__':
    unittest.main()
