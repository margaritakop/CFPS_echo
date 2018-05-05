from unittest import TestCase


class TestGenerate_sample_content_dictionary(TestCase):
    def test_generate_sample_content_dictionary(self):
        from src.generate_protocol import generate_sample_content_dictionary
        form = {'DNA_samples': ['Cas9A_A'],
                'DNA_volumes': [125],
                'REG_samples': ['sgA_01', 'sgA_02'],
                'REG_volumes': [250]}
        adv_form = {'positive_DNAvol': 500,
                    'max_sourcewell_volume': 65000, 'mm_in_reaction': 1500, 'cargo_content': 500, 'MM_in_picklist': 'NO'}
        result = generate_sample_content_dictionary(form, adv_form)
        expected_result = {'ID_01': {'DNA_Cas9A_A': 125, 'REG_sgA_01': 250, 'BUF': 125},
                           'ID_02': {'DNA_Cas9A_A': 125, 'REG_sgA_02': 250, 'BUF': 125},
                           'ID_B': {'BUF': 500, 'DNAP': 0},
                           'ID_P': {'BUF': 0, 'DNAP': 500}}
        self.assertEqual(result, expected_result)
        #with Master Mix
        form = {'DNA_samples': ['Cas9A_A'],
                'DNA_volumes': [125],
                'REG_samples': ['sgA_01'],
                'REG_volumes': [250]}
        adv_form = {'positive_DNAvol': 500,
                    'max_sourcewell_volume': 65000, 'mm_in_reaction': 1500, 'cargo_content': 500, 'MM_in_picklist': 'YES'}
        result = generate_sample_content_dictionary(form, adv_form)
        expected_result = {'ID_01': {'BUF': 125, 'DNA_Cas9A_A': 125, 'REG_sgA_01': 250, 'MM': 1500},
                           'ID_B': {'BUF': 500, 'DNAP': 0, 'MM': 1500},
                           'ID_P': {'BUF': 0, 'DNAP': 500, 'MM': 1500}}
        self.assertEqual(result, expected_result)
