class Memory:
    def __init__(self, data=[]):
        self._data = data

    def reset(self, data=[]):
        self._data.clear()
        self._data = data

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, key, value):
        self._data[key] = value

    def insert(self, data):
        self._data.extend(data)
