import unittest
from unittest.mock import patch
import datetime

from person import Person  # предполагаем, что класс сохранён в person.py

class FixedDatetime(datetime.datetime):
    @classmethod
    def now(cls):
        return cls(2025, 9, 17)

class TestPerson(unittest.TestCase):

    def setUp(self):
        self.person = Person(name="Alice", year_of_birth=1990, address="123 Street")

    @patch('person.datetime.datetime', FixedDatetime)
    def test_get_age_correct(self):
        p = Person("Alice", 1990)
        self.assertEqual(p.get_age(), 35)

    def test_get_name(self):
        self.assertEqual(self.person.get_name(), "Alice")

    def test_set_name(self):
        self.person.set_name("Bob")
        self.assertEqual(self.person.get_name(), "Bob")

    def test_set_address(self):
        self.person.set_address("456 Avenue")
        self.assertEqual(self.person.get_address(), "456 Avenue")

    def test_get_address(self):
        self.assertEqual(self.person.get_address(), "123 Street")

    def test_is_homeless_true(self):
        person2 = Person("Charlie", 1985)
        self.assertTrue(person2.is_homeless())

    def test_is_homeless_false(self):
        self.assertFalse(self.person.is_homeless())


if __name__ == "__main__":
    unittest.main()
