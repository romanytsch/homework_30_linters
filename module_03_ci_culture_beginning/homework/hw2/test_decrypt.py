import unittest

from decrypt import decrypt

class TestDecrypt(unittest.TestCase):
    def test_single_dots(self):
        test_cases = [
            ("абра-кадабра.", "абра-кадабра"),
            ("абрау...-кадабра", "абра-кадабра"),
            (".", "")
        ]
        for data, expected in test_cases:
            with self.subTest(data=data):
                self.assertEqual(decrypt(data), expected)

    def test_double_dots(self):
        test_cases = [
            ("абраа..-кадабра", "абра-кадабра"),
            (" абраа..-.кадабра", " абра-кадабра"),
            ("абра--..кадабра", "абра-кадабра"),
            ("1..2.3", "23"),
        ]
        for data, expected in test_cases:
            with self.subTest(data=data):
                self.assertEqual(decrypt(data), expected)

    def test_many_dots(self):
        test_cases = [
            ("абра........", ""),
            ("1.......................", ""),
            ("бр......a.", "a"),
        ]
        for data, expected in test_cases:
            with self.subTest(data=data):
                self.assertEqual(decrypt(data), expected)
