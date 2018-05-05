import logging
import os
import operator
import pprint
import collections

from src import picklist

def set_folder(name):
    "make and go to a sub-folder where all the outputs will be"
    try:
        os.mkdir("./" + name)
    except:
        pass
    os.chdir("./" + name)


def picklist_file(ID_content_dictionary, ID_position_dictionary, SW_position_dictionary):
    try:
        os.chdir("./experiment_files")  # Got to experiment_files folder
    except:
        os.mkdir("./experiment_files")  # Make the experiment_files folder
        os.chdir("./experiment_files")

    picklist.initiate_picklist('picklist.csv')

    for ID in sorted(ID_content_dictionary.keys()):
        components = ID_content_dictionary[ID]
        wells = ID_position_dictionary[ID]
        for well in wells:
            for component in components:
                transfer = picklist.get_transfer(ID, component, well, ID_content_dictionary, SW_position_dictionary)
                picklist.write_to_picklist('picklist.csv', transfer)

    logging.debug('picklist.csv output in experiment_files folder.')
    os.chdir("..")
    return ('picklist.csv generated')

def source_plate_file(SW_position_dictionary, SW_content_dictionary):
        try:
            os.chdir("./experiment_files")  # Got to experiment_files folder
        except:
            os.mkdir("./experiment_files")  # Make the experiment_files folder
            os.chdir("./experiment_files")

        source_plate = open('source_plate.csv', 'w')
        source_plate.write("Put the samples in the wells below: \n"
                           "Sample, Well, Minimum Volume (uL), \n")

        sorted_SW = sorted(SW_position_dictionary.items(), key=operator.itemgetter(1))

        for item in sorted_SW:
            try:
                volume = SW_content_dictionary[item[0]]/float(1000)
                source_plate.write(str(item[0] + ',' + item[1]) + ',' + str(volume) + '\n')
            except:
                print (str(item) + ' content in sourceplate missing from experiment!')
        source_plate.close()
        os.chdir("..")
        logging.debug('source_plate.txt output in experiment_files folder.')

def get_MM_prep(ID_content_dictionary):
    "calculate MM prep and make a dictionary"
    ID_content_dictionary_TXTL = ID_content_dictionary.copy()
    #remove standards, keep TXTL wells only

    for key in ID_content_dictionary:
        if 'st' in key:
            ID_content_dictionary_TXTL.pop(key)

    #count number or wells with TXTL in them and finds the first and last wells
    first_well = 'P24'
    last_well = 'A01'
    TXTL_wells_total = 0
    for ID, wells in ID_content_dictionary_TXTL.items():
        for well in wells:
            if well < first_well:
                first_well = well
            if well > last_well:
                last_well = well

            TXTL_wells_total += 1

    MM_prep = {}
    dead_volume = 200 #uL
    MM_needed = dead_volume + TXTL_wells_total*1.5
    MM_prep['Number of TXTL wells'] = TXTL_wells_total
    MM_prep['Location of TXTL wells'] = (first_well, last_well)
    MM_prep['Total MM needed (incl deadV)'] = MM_needed
    MM_prep['Lysate'] = MM_needed * 0.5
    MM_prep['Protein'] = MM_needed * 0.1
    MM_prep['Energy'] = MM_needed * 0.2
    MM_prep['PBS'] = MM_needed * 0.2
    return MM_prep

def MM_prep_file(MM_prep_dictionary):
    try:
        os.chdir("./experiment_files")  # Got to experiment_files folder
    except:
        os.mkdir("./experiment_files")  # Make the experiment_files folder
        os.chdir("./experiment_files")


    MM_prep = open('MM_prep.csv', 'w')
    MM_prep.write("Prepare the MM and transfer to the wells: \n")

    MM_prep.write('Number of TXTL wells,' + str(MM_prep_dictionary['Number of TXTL wells']) + ', \n')
    MM_prep.write('Lysate,' + str(MM_prep_dictionary['Lysate']) + '\n')
    MM_prep.write('Protein,' + str(MM_prep_dictionary['Protein']) + '\n')
    MM_prep.write('Energy,' + str(MM_prep_dictionary['Energy']) + '\n')
    MM_prep.write('PBS,' + str(MM_prep_dictionary['PBS']) + '\n')
    MM_prep.write('Total MM needed (incl deadV),' + str(MM_prep_dictionary['Total MM needed (incl deadV)']) + ', \n')
    MM_prep.write('Location of TXTL wells,' + str(MM_prep_dictionary['Location of TXTL wells']) + '\n')

    os.chdir("..")
    logging.debug('MM_prep.txt output in experiment_files folder.')

def dictionaries_file (dictionaries):
    try:
        os.chdir("./example_experiment_files")  # Got to experiment_files folder
    except:
        pass

    dictionaries_file = open('info_dictionaries.txt', 'w')

    for dictionary in dictionaries:
        dictionaries_file.write(str(pprint.pformat(dictionary)) + '\n')
    logging.debug('info_dictionaries.txt output in experiment_files folder.')
    dictionaries_file.close()

