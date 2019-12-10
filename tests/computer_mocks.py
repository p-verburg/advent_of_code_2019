class MockFailInput:
    def __init__(self, test_case):
        self._test_case = test_case

    def receive(self):
        self._test_case.assertFail('Unexpected input read')


class MockParameter:
    set_value = None

    def __init__(self, value):
        self._get_value = value

    def get(self):
        return self._get_value

    def set(self, value):
        self.set_value = value
