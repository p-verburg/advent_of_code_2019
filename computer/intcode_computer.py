from computer.programs.memory import Memory
from computer.programs.operations import OperationFactory, HaltOperation
from computer.programs.parameters import ParameterFactory


class NoneInput:
    @staticmethod
    def receive():
        return None


class ListInput:
    def __init__(self, inputs):
        self._inputs = inputs

    def receive(self):
        return self._inputs.pop()


class VoidOutput:
    def send(self, value):
        pass


class ListOutput:
    def __init__(self):
        self.list = []

    def send(self, value):
        self.list.append(value)


class IntcodeComputer:

    def __init__(self, input=NoneInput(), output=VoidOutput()):
        self._input = input
        self._output = output
        self._memory = Memory()
        self._parameter_factory = ParameterFactory(self._memory)
        self._operation_factory = OperationFactory(self._memory, self._input, self._output)

    def reset_memory(self, data=[]):
        self._memory.reset(data)

    def write_memory(self, data):
        self._memory.insert(data)

    def execute_instruction(self, instruction_pointer):
        instruction_code = self._memory[instruction_pointer]
        instruction_digits = [int(digit) for digit in str(instruction_code)]
        opcode = instruction_digits.pop()
        if instruction_digits:
            opcode += instruction_digits.pop() * 10
        operation = self._operation_factory.create_operation(opcode)

        parameters = self._parameter_factory.create_parameters(
            instruction_digits, operation.parameter_count, instruction_pointer)

        operation.execute(parameters, self._input, self._output)

        if isinstance(operation, HaltOperation):
            return -1
        return instruction_pointer + operation.parameter_count + 1

    def run_program(self):
        instruction_pointer = 0
        while not instruction_pointer == -1:
            instruction_pointer = self.execute_instruction(instruction_pointer)
