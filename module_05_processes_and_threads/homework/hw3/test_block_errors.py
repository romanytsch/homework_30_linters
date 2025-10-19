import unittest

from block_errors import BlockErrors

class TestBlockErrors(unittest.TestCase):

    def test_ignore_error(self):
        err_types = {ZeroDivisionError}
        try:
            with BlockErrors(err_types):
                a = 1 / 0
        except Exception:
            self.fail("Исключение ZeroDivisionError не было подавлено")

    def test_propagate_error(self):
        err_types = {ZeroDivisionError}
        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 / '0'

    def test_nested_blocks(self):
        outer_err_types = {TypeError}
        try:
            with BlockErrors(outer_err_types):
                inner_err_types = {ZeroDivisionError}
                with BlockErrors(inner_err_types):
                    a = 1 / '0'  # TypeError
        except Exception:
            self.fail("Исключение TypeError не было подавлено внешним блоком")

    def test_subclass_error_ignored(self):
        err_types = {Exception}
        try:
            with BlockErrors(err_types):
                a = 1 / '0'  # TypeError дочерний от Exception
        except Exception:
            self.fail("Исключение не было подавлено, хотя Error является подтипом Exception")


if __name__ == '__main__':
    unittest.main()
