#Edward Lippel

import unittest
import Task1

class TestPositiveValue(unittest.TestCase):
    def test_decimal_to_binary(self):
        test_cases = [
            (10, '00000000000000000000000000001010'),
            (255, '00000000000000000000000011111111'),
            (1024, '00000000000000000000010000000000'),
            (65536, '00000000000000010000000000000000'),
        ]
        for value, expected in test_cases:
            with self.subTest(value=value):
                self.assertEqual(Task1.decimal_to_binary(value), expected)
    def test_binary_to_decimal(self):
        test_cases = [
            ('00000000000000000000000000001010', 10),
            ('00000000000000000000000011111111', 255),
            ('00000000000000010000000000000000', 65536),
            ('01111111111111111111111111111111', 2147483647),
        ]
        for binary, expected in test_cases:
            with self.subTest(binary=binary):
                self.assertEqual(Task1.binary_to_decimal(binary), expected)
    def test_binary_to_hexadecimal(self):
        test_cases = [
            ('00000000000000000000000000001010', '0000000A'),
            ('00000000000000000000000011111111', '000000FF'),
            ('00000000000000111111111111111111', '0003FFFF'),
            ('01111111111111111111111111111111', '7FFFFFFF'),
        ]
        for binary, expected in test_cases:
            with self.subTest(binary=binary):
                self.assertEqual(Task1.binary_to_hexadecimal(binary), expected)

class TestNegativeValue(unittest.TestCase):
    def test_decimal_to_binary(self):
        test_cases = [
            (-10, '11111111111111111111111111110110'),
            (-255, '11111111111111111111111100000001'),
            (-1024, '11111111111111111111110000000000'),
            (-65536, '11111111111111110000000000000000'),
        ]
        for value, expected in test_cases:
            with self.subTest(value=value):
                self.assertEqual(Task1.decimal_to_binary(value), expected)
    def test_binary_to_decimal(self):
        test_cases = [
            ('11111111111111111111111111110110', -10),
            ('11111111111111111111111100000001', -255),
            ('11111111111111111111110000000000', -1024),
            ('11111111111111110000000000000000', -65536),
        ]
        for binary, expected in test_cases:
            with self.subTest(binary=binary):
                self.assertEqual(Task1.binary_to_decimal(binary), expected)
    def test_binary_to_hexadecimal(self):
        test_cases = [
            ('10000000000000000000000000000110', '80000006'),
            ('10000000000000000000000000000001', '80000001'),
            ('11111111111111111111111111111111', 'FFFFFFFF'),
        ]
        for binary, expected in test_cases:
            with self.subTest(binary=binary):
                self.assertEqual(Task1.binary_to_hexadecimal(binary), expected)

class TestZeroValue(unittest.TestCase):
    def test_decimal_to_binary(self):
        test_cases = [
            (0, '00000000000000000000000000000000'),
        ]
        for value, expected in test_cases:
            with self.subTest(value=value):
                self.assertEqual(Task1.decimal_to_binary(value), expected)
    def test_binary_to_decimal(self):
        test_cases = [
            ('00000000000000000000000000000000', 0),
        ]
        for binary, expected in test_cases:
            with self.subTest(binary=binary):
                self.assertEqual(Task1.binary_to_decimal(binary), expected)
    def test_binary_to_hexadecimal(self):
        test_cases = [
            ('00000000000000000000000000000000', '00000000'),
        ]
        for binary, expected in test_cases:
            with self.subTest(binary=binary):
                self.assertEqual(Task1.binary_to_hexadecimal(binary), expected)

class TestOutOfRangeValue(unittest.TestCase):
    def test_decimal_to_binary(self):
        test_cases = [
            (2**31 + 4, '01111111111111111111111111111111'),
            (-2147483648 - 4, '11111111111111111111111111111111'),
        ]
        for value, expected in test_cases:
            with self.subTest(value=value):
                self.assertEqual(Task1.decimal_to_binary(value), expected)
    def test_binary_to_decimal(self):
        test_cases = [
            ('01111111111111111111111111111111', 2147483647),
            ('11111111111111111111111111111111', -2147483648),
        ]
        for binary, expected in test_cases:
            with self.subTest(binary=binary):
                self.assertEqual(Task1.binary_to_decimal(binary), expected)
    def test_binary_to_hexadecimal(self):
        test_cases = [
            ('01111111111111111111111111111111', '7FFFFFFF'),
            ('10000000000000000000000000000000', '80000000'),
        ]
        for binary, expected in test_cases:
            with self.subTest(binary=binary):
                self.assertEqual(Task1.binary_to_hexadecimal(binary), expected)

if __name__ == '__main__':
    unittest.main()