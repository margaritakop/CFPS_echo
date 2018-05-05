from unittest import TestCase
import generate_protocol

class TestGenerate_st_content_dictionary(TestCase):
    def test_generate_st_content_dictionary(self):
        from src.generate_protocol import generate_st_content_dictionary
        result = generate_st_content_dictionary({'total_st_volume' : 2000, 'st_volumes' : [1500, 1000, 0]})
        expected_result = {'ID_st01': {'PBS': 500, 'FITC': 1500}, 'ID_st02': {'PBS': 1000, 'FITC': 1000}, 'ID_st03': {'PBS': 2000, 'FITC': 0}}
        self.assertEqual(result, expected_result)
        result = generate_st_content_dictionary({'total_st_volume' : 2000, 'st_volumes' : []})
        expected_result = {}
        self.assertEqual(result, expected_result)
