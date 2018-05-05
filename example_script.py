import logging
import shutil

from src import generate_protocol as generate
from src import output_instructions as output

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

form = {'DNA_samples': ['pSM689_10', 'pSM689_7.5', 'pSM689_5', 'pSM689_2.5', 'pSM689_1.25', 'pSM689_0.25', 'pSM689_0.025',
                        'pCFE-GFP_10', 'pCFE-GFP_7.5', 'pCFE-GFP_5', 'pCFE-GFP_2.5', 'pCFE-GFP_1.25', 'pCFE-GFP_0.25', 'pCFE-GFP_0.025'],
        'DNA_volumes': [500],
        'REG_samples': [],
        'REG_volumes': []}

adv_form = {'total_st_volume' : 0, 'st_volumes' : [], 'st_replicates' : 3,
                'positive_DNAvol' : 500,
                'max_sourcewell_volume' : 65000, 'mm_in_reaction' : 1500, 'cargo_content': 500,
                'start_destwell':'M01', 'BP_replicates':0,
                'sample_replicates': 4, 'shuffle' : 'YES', 'MM_in_picklist':'NO', 'TXTL_replicates': 5}


SW_position_dictionary = {'DNA_pSM689_10': 'P01',
                          'DNA_pSM689_7.5': 'P02',
                          'DNA_pSM689_5': 'P03',
                          'DNA_pSM689_2.5': 'P04',
                          'DNA_pSM689_1.25': 'P05',
                          'DNA_pSM689_0.25': 'P06',
                          'DNA_pSM689_0.025': 'P07',
                          'DNA_pCFE-GFP_10': 'O01',
                          'DNA_pCFE-GFP_7.5': 'O02',
                          'DNA_pCFE-GFP_5': 'O03',
                          'DNA_pCFE-GFP_2.5': 'O04',
                          'DNA_pCFE-GFP_1.25': 'O05',
                          'DNA_pCFE-GFP_0.25': 'O06',
                          'DNA_pCFE-GFP_0.025': 'O07',
                          'BUF': 'K02',
                          'DNAP': 'K01'}

ID_content_dictionary = generate.generate_sample_content_dictionary(form, adv_form)

generate.adjust_sort_remove0(ID_content_dictionary, adv_form)


ID_position_dictionary = generate.generate_ID_position_dictionary(generate.get_wells_list(adv_form), ID_content_dictionary, adv_form)
SW_content_dictionary = (generate.generate_Sourcewell_content_dictionary(ID_content_dictionary, ID_position_dictionary))

MM_prep_dictionary = output.get_MM_prep(ID_position_dictionary)



output.set_folder('example_experiment files')

#copy the code in order to save a version along with the experiment instructions
shutil.copy('../example_script.py', 'script_save.py')

#save the files for the experiment
output.picklist_file(ID_content_dictionary, ID_position_dictionary, SW_position_dictionary)
output.source_plate_file(SW_position_dictionary, SW_content_dictionary)
output.MM_prep_file(MM_prep_dictionary)
output.dictionaries_file([ID_content_dictionary, ID_position_dictionary])