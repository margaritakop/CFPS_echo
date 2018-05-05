from unittest import TestCase


class TestGenerate_ID_position_dictionary(TestCase):
    def test_generate_ID_position_dictionary(self):
        #needs to exit if there are not enough wells for the experiment
        with self.assertRaises(SystemExit):
            DEST_list = ['O15', 'O16', 'O17', 'O18', 'O19', 'O20', 'O21', 'O22', 'O23', 'O24', 'P15', 'P16', 'P17', 'P18', 'P19',
             'P20', 'P21', 'P22', 'P23', 'P24']
            sample_content_dictionary = {'ID_01': {'DNA_pCFE-GFP-MGapt': 450, 'REG_MG5000uM': 50},
             'ID_05': {'DNA_pCFE-GFP': 450, 'REG_MG5000uM': 50}, 'ID_03': {'DNA_pSM689': 450, 'REG_MG5000uM': 50},
             'ID_02': {'DNA_pCFE-GFP-MGapt': 450, 'REG_MG10000uM': 50}, 'ID_07': {'DNA_water': 450, 'REG_MG5000uM': 50},
             'ID_08': {'DNA_water': 450, 'REG_MG10000uM': 50}, 'ID_06': {'DNA_pCFE-GFP': 450, 'REG_MG10000uM': 50},
             'ID_04': {'DNA_pSM689': 450, 'REG_MG10000uM': 50}}
            adv_form = {'start_destwell': 'O15', 'shuffle': 'YES', 'st_replicates': 3, 'TXTL_replicates': 3, 'BP_replicates': 0,
             'st_volumes': [], 'sample_replicates': 3, 'total_st_volume': 0, 'cargo_content': 500,
             'max_sourcewell_volume': 65000, 'mm_in_reaction': 1500, 'MM_in_picklist': 'NO', 'start_sourcewell': 'A1',
             'positive_DNAvol': 500}

            from src.generate_protocol import generate_ID_position_dictionary
            generate_ID_position_dictionary(DEST_list, sample_content_dictionary, adv_form)
