from enum import IntEnum
import operator


class OperationCode(IntEnum):
    ADD = 1,
    MULTIPLY = 2,
    INPUT = 3,
    OUTPUT = 4,
    JUMP_IF_TRUE = 5,
    JUMP_IF_FALSE = 6,
    LESS_THAN = 7,
    EQUALS = 8,
    END = 99


class BaseOperation:
    parameter_count = 0

    @staticmethod
    def execute(parameters, input, output):
        pass

    def get_new_pointer(self, instruction_pointer):
        return instruction_pointer + self.parameter_count + 1


class AddOperation(BaseOperation):
    parameter_count = 3

    @staticmethod
    def execute(parameters, input, output):
        parameters[2].set(parameters[0].get() + parameters[1].get())


class MultiplyOperation(BaseOperation):
    parameter_count = 3

    @staticmethod
    def execute(parameters, input, output):
        parameters[2].set(parameters[0].get() * parameters[1].get())


class InputOperation(BaseOperation):
    parameter_count = 1

    @staticmethod
    def execute(parameters, input, output):
        parameters[0].set(input.receive())


class OutputOperation(BaseOperation):
    parameter_count = 1

    @staticmethod
    def execute(parameters, input, output):
        output.send(parameters[0].get())


class JumpIfOperation(BaseOperation):
    parameter_count = 2

    def __init__(self, condition):
        self.new_pointer = None
        self.condition = condition

    def execute(self, parameters, input, output):
        if (parameters[0].get() != 0) == self.condition:
            self.new_pointer = parameters[1].get()
        else:
            self.new_pointer = None

    def get_new_pointer(self, instruction_pointer):
        if self.new_pointer is not None:
            return self.new_pointer
        return BaseOperation.get_new_pointer(self, instruction_pointer)


class CompareOperation(BaseOperation):
    parameter_count = 3

    def __init__(self, operator):
        self.operator = operator

    def execute(self, parameters, input, output):
        parameters[2].set(int(self.operator(parameters[0].get(), parameters[1].get())))


class HaltOperation(BaseOperation):
    @staticmethod
    def execute(parameters, input, output):
        pass

    def get_new_pointer(self, instruction_pointer):
        return -1


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
        if operation_code == OperationCode.JUMP_IF_TRUE:
            return JumpIfOperation(True)
        if operation_code == OperationCode.JUMP_IF_FALSE:
            return JumpIfOperation(False)
        if operation_code == OperationCode.LESS_THAN:
            return CompareOperation(operator.lt)
        if operation_code == OperationCode.EQUALS:
            return CompareOperation(operator.eq)
        if operation_code == OperationCode.END:
            return HaltOperation()
        raise ValueError('Unsupported operation code {}'.format(operation_code))
