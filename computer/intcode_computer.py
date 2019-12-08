from enum import IntEnum


class operation(IntEnum):
    ADD = 1,
    MULTIPLY = 2,
    END = 99


class intcode_computer:

    def __init__(self):
        pass

    def compute_instruction(self, memory, instruction_pointer):
        opcode = operation(memory[instruction_pointer])
        if opcode == operation.ADD:
            address1 = memory[instruction_pointer+1]
            address2 = memory[instruction_pointer+2]
            address3 = memory[instruction_pointer+3]
            memory[address3] = memory[address1] + memory[address2]
            return instruction_pointer + 4
        if opcode == operation.MULTIPLY:
            address1 = memory[instruction_pointer+1]
            address2 = memory[instruction_pointer+2]
            address3 = memory[instruction_pointer+3]
            memory[address3] = memory[address1] * memory[address2]
            return instruction_pointer + 4
        if opcode == operation.END:
            return -1
        raise ValueError

    def compute_program(self, memory):
        instruction_pointer = 0
        while not instruction_pointer == -1:
            instruction_pointer = self.compute_instruction(memory, instruction_pointer)
