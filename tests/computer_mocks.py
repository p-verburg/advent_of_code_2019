class MockConstantInput:
    def __init__(self, value=0):
        self._value = value

    def receive(self):
        return self._value


class MockFailInput:
    def __init__(self, test_case):
        self._test_case = test_case

    def receive(self):
        self._test_case.assertFail('Unexpected input read')


class MockListOutput:
    def __init__(self):
        self.list = []

    def send(self, value):
        self.list.append(value)


class MockParameter:
    set_value = None

    def __init__(self, value):
        self._get_value = value

    def get(self):
        return self._get_value

    def set(self, value):
        self.set_value = value
