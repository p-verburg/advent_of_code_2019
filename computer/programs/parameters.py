class BaseParameter:
    def __init__(self, memory, pointer):
        self._memory = memory
        self._pointer = pointer


class PositionParameter(BaseParameter):
    def __init__(self, memory, pointer):
        BaseParameter.__init__(self, memory, pointer)

    def get(self):
        return self._memory[self._memory[self._pointer]]

    def set(self, value):
        self._memory[self._memory[self._pointer]] = value


class ImmediateParameter(BaseParameter):
    def __init__(self, memory, pointer):
        BaseParameter.__init__(self, memory, pointer)

    def get(self):
        return self._memory[self._pointer]

    def set(self, value):
        self._memory[self._pointer] = value


class ParameterFactory:
    _default_mode = 0

    def __init__(self, memory):
        self._memory = memory

    def create_parameter(self, parameter_code, pointer):
        if parameter_code == 0:
            return PositionParameter(self._memory, pointer)
        if parameter_code == 1:
            return ImmediateParameter(self._memory, pointer)
        raise ValueError('Unknown parameter code {}'.format(parameter_code))

    def create_parameters(self, parameter_codes, parameter_count, instruction_pointer):
        codes_count = len(parameter_codes)

        if codes_count > parameter_count:
            raise ValueError('Too many parameter codes {} (expected max {})'.format(codes_count, parameter_count))

        ordered_parameter_codes = list(reversed(parameter_codes))

        missing_codes_count = parameter_count - codes_count
        if missing_codes_count > 0:
            ordered_parameter_codes.extend([ParameterFactory._default_mode for _ in range(missing_codes_count)])
        assert(len(ordered_parameter_codes) == parameter_count)

        parameter_pointer = instruction_pointer + 1
        parameters = []
        for code in ordered_parameter_codes:
            parameters.append(self.create_parameter(code, parameter_pointer))
            parameter_pointer += 1

        return parameters
