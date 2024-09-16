import unittest
from modules.dependency_mapper import parse_requirements

class TestParsing(unittest.TestCase):
    def test_parse_requirements(self):
        self.assertEqual(parse_requirements('requirements.txt'), ['dependency'])