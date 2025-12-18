import unittest
from converter4 import parse_config, generate_xml


class TestConverter4(unittest.TestCase):
    def test_simple_number(self):
        text = "value: 1.5e2"
        result = parse_config(text)
        self.assertEqual(result['value'], 150.0)

    def test_array(self):
        text = "values: [10 20 30]"
        result = parse_config(text)
        self.assertEqual(result['values'], [10, 20, 30])

    def test_var_and_expr(self):
        text = """var x 5
result: ${x 1 +}"""
        result = parse_config(text)
        self.assertEqual(result['result'], 6)

    def test_pow_function(self):
        text = """var a 2
var b 3
result: ${a b pow}"""
        result = parse_config(text)
        self.assertEqual(result['result'], 8.0)

    def test_max_function(self):
        text = """var x 10
var y 15
result: ${x y max}"""
        result = parse_config(text)
        self.assertEqual(result['result'], 15)

    def test_complex_expr(self):
        text = """var base 2
var exp 4
result: ${base exp pow 10 +}"""
        result = parse_config(text)
        self.assertEqual(result['result'], 26.0)

    def test_nested_arrays(self):
        text = "matrix: [[1 2] [3 4]]"
        result = parse_config(text)
        self.assertEqual(result['matrix'], [[1, 2], [3, 4]])


if __name__ == '__main__':
    unittest.main()