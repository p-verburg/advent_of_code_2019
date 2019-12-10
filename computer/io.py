class NoneInput:
    @staticmethod
    def receive():
        return None


class ListInput:
    def __init__(self, inputs):
        self._inputs = inputs

    def receive(self):
        return self._inputs.pop()


class SingleInput:
    def __init__(self, input):
        self._input = input

    def receive(self):
        return self._input


class VoidOutput:
    def send(self, value):
        pass


class ListOutput:
    def __init__(self):
        self.list = []

    def __eq__(self, other):
        return self.list == other

    def __str__(self):
        return str(self.list)

    def send(self, value):
        self.list.append(value)


class LastOutput:
    def __init__(self):
        self.value = None

    def __eq__(self, other):
        return self.value == other

    def __str__(self):
        str(self.value)

    def send(self, value):
        self.value = value
