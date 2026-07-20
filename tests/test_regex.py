import unittest
from utils.category_regex import *
class RegexTests(unittest.TestCase):
 def test_unchanged(self):self.assertEqual(MEASUREMENT_PATTERN.pattern,r"\A[A-Za-z_][A-Za-z0-9_.]*\Z");self.assertEqual(CHARACTERISTIC_PATTERN.pattern,r"\A(?:[A-Za-z][A-Za-z0-9_.]*|_[A-Za-z0-9_.]+)\Z");self.assertEqual(SYSTEM_CONSTANT_PATTERN.pattern,r"\A[A-Za-z_][A-Za-z0-9_.]*\Z")
