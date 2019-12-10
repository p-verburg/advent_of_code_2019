from enum import IntEnum


class OperationCode(IntEnum):
    ADD = 1,
    MULTIPLY = 2,
    INPUT = 3,
    OUTPUT = 4,
    END = 99


class AddOperation:
    parameter_count = 3

    @staticmethod
    def execute(parameters, input, output):
        parameters[2].set(parameters[0].get() + parameters[1].get())


class MultiplyOperation:
    parameter_count = 3

    @staticmethod
    def execute(parameters, input, output):
        parameters[2].set(parameters[0].get() * parameters[1].get())


class InputOperation:
    parameter_count = 1

    @staticmethod
    def execute(parameters, input, output):
        parameters[0].set(input.receive())


class OutputOperation:
    parameter_count = 1

    @staticmethod
    def execute(parameters, input, output):
        output.send(parameters[0].get())


class HaltOperation:
    parameter_count = 0

    @staticmethod
    def execute(parameters, input, output):
        pass


class OperationFactory:
    def __init__(self, memory, input, output):
        self._memory = memory
        self._input = input
        self._output = output

    @staticmethod
    def create_operation(opcode):
        operation_code = OperationCode(opcode)
        if operation_code == OperationCode.ADD:
            return AddOperation()
        if operation_code == OperationCode.MULTIPLY:
            return MultiplyOperation()
        if operation_code == OperationCode.INPUT:
            return InputOperation()
        if operation_code == OperationCode.OUTPUT:
            return OutputOperation()
        if operation_code == OperationCode.END:
            return HaltOperation()
        raise ValueError('Unsupported operation code {}'.format(operation_code))
