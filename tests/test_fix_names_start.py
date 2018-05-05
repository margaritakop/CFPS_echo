from unittest import TestCase
import generate_protocol

class TestFix_names_start(TestCase):
    def test_fix_names_start(self):
        result = generate_protocol.fix_names_start(['A', 'B'], 'REG')
        self.assertEqual(result, ['REG_A', 'REG_B'])
