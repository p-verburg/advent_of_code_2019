import unittest
import computer.io as io


def list_output(first, second):
    output = io.ListOutput()
    output.send(first)
    output.send(second)
    return output


def last_output(first, second):
    output = io.LastOutput()
    output.send(first)
    output.send(second)
    return output


class InputTests(unittest.TestCase):
    def test_none_input(self):
        input = io.NoneInput()

        self.assertIsNone(input.receive())

    def test_list_input(self):
        input = io.ListInput([1, 2, 3])

        self.assertEqual(1, input.receive())
        self.assertEqual(2, input.receive())
        self.assertEqual(3, input.receive())

    def test_single_input(self):
        input = io.SingleInput(37)

        self.assertEqual(37, input.receive())
        self.assertEqual(37, input.receive())

    @staticmethod
    def test_void_output():
        output = io.VoidOutput()

        output.send(21)
        output.send(39)

    def test_list_output(self):
        output = list_output(-5, 29)

        self.assertEqual([-5, 29], output.list)

    def test_list_output_str(self):
        output = list_output(-5, 29)

        self.assertEqual("[-5, 29]", str(output))

    def test_list_output_eq(self):
        output = list_output(-5, 29)

        equal = list_output(-5, 29)
        not_equal = list_output(3, 29)

        self.assertEqual(equal, output)
        self.assertNotEqual(not_equal, output)

    def test_last_output(self):
        output = last_output(7, 21)

        self.assertEqual(21, output.value)

    def test_last_output_str(self):
        output = last_output(7, 21)

        self.assertEqual("21", str(output))

    def test_last_output_eq(self):
        output = last_output(7, 21)

        equal = last_output(9, 21)
        not_equal = last_output(21, 7)

        self.assertEqual(equal, output)
        self.assertNotEqual(not_equal, output)


if __name__ == '__main__':
    unittest.main()
