import unittest
from util import exec_with_return
import util


class TestExecWithReturn(unittest.TestCase):
    def test_exec_with_return_single_expression(self):
        code = "3 + 4"
        expected = 7
        result = exec_with_return(code)
        self.assertEqual(result, expected)

    def test_exec_with_return_single_statement(self):
        code = "x = 5"
        expected = None
        result = exec_with_return(code)
        self.assertEqual(result, expected)

    def test_exec_with_return_mixed_code(self):
        code = """
a = 2
b = 3
a * b
"""
        expected = 6
        result = exec_with_return(code)
        self.assertEqual(result, expected)

    def test_exec_with_return_function_definition(self):
        code = """
def add(x, y):
    return x + y

add(3, 4)
"""
        expected = 7
        result = exec_with_return(code)
        self.assertEqual(result, expected)

    def test_exec_with_return_complex_code(self):
        code = """
class MyClass:
    def __init__(self, x):
        self.x = x

    def multiply(self, y):
        return self.x * y

obj = MyClass(5)
obj.multiply(4)
"""
        expected = 20
        result = exec_with_return(code)
        self.assertEqual(result, expected)

    def test_get_small_trace(self):
        code = """
import string

def encrypt_text(text: str, key: str) -> str:
    alphabet = string.ascii_lowercase
    key_map = str.maketrans(alphabet, key[:len(alphabet)])
    return text.translate(key_map)

encrypt_text('Hello, World!', 'abc123')
"""

        try:
            exec_with_return(code)
        except Exception:
            small_trace = util.getSmallTrace()
            self.assertIn("ValueError", small_trace)
            self.assertIn("encrypt_text", small_trace)

            # Check if the output has exactly two lines
            lines = small_trace.splitlines()
            self.assertEqual(len(lines), 2)


if __name__ == "__main__":
    unittest.main()
