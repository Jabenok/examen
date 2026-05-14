import unittest
from bilet2 import Library


class TestLibrary(unittest.TestCase):
    
    def test_validate_isbn(self):

        self.assertTrue(Library.validate_isbn("1234567891111"))
        self.assertFalse(Library.validate_isbn("123456789111"))
        self.assertFalse(Library.validate_isbn("1"))
        self.assertFalse(Library.validate_isbn("asdasd"))
        self.assertFalse(Library.validate_isbn("123456789111a"))
