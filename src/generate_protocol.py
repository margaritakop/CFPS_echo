__author__ = 'margaritakop'
# This script for HeLa TX-TL experiments. It generates picklists and a writes a protocol for source plate prep.

import sys
from collections import OrderedDict
import random
import logging


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')


def fix_names_start(what_samples, WHAT):
    "In order to distinguish DNA from REG, even if names given by user are uninformative."
    for x, sample in enumerate(what_samples):
        start = sample[:3].upper()
        if start == str(WHAT):
            what_samples[x] = start + sample[3:]
        else:
            what_samples[x] = WHAT + '_' + str(sample)
    return what_samples

def get_wells_list(adv_form):
    "Get a list of wells as strs, according to 384 format, starting from well given in adv_form dictionary."
    startwell = adv_form['start_destwell']
    row_letter = startwell[0]
    column_number = int(startwell[1:])
    wells_list = []
    for i in range(ord(row_letter), ord("P")+1):
        for p in range(column_number, 25):
            if p < 10:
                wells_list.append(chr(i) + "0" + str(p))
            else:
                wells_list.append(chr(i) + str(p))
    if wells_list == []:
        sys.exit('Give a valid start destination well!')
    return wells_list

#mid-level functions for fixing the contents on the various reactions
def generate_st_content_dictionary(adv_form):
    st_volumes = adv_form['st_volumes']
    total_st_volume = adv_form['total_st_volume']

    st_content_dictionary = {}
    try:
        ID_item = {}
        x = 1
        for volume in st_volumes:
            ID = str('ID_st'+str(x).zfill(2))
            ID_item['FITC'] = volume
            ID_item['PBS'] = total_st_volume - volume
            st_content_dictionary[ID] = ID_item
            x = x+1
            ID_item = {}
    except:
        pass
    return st_content_dictionary


def generate_sample_content_dictionary(form, adv_form):
    cargo_content = adv_form['cargo_content']
    positive_DNAvol = adv_form['positive_DNAvol']
    mm_in_reaction = adv_form['mm_in_reaction']

    ID_content_dictionary = {}
    ID_item = {}
    x = 1

    try:
        DNA_samples = form['DNA_samples'].split(", ")
    except:
        DNA_samples = form['DNA_samples']

    fix_names_start(DNA_samples, 'DNA')

    try:
        DNA_volumes = (form['DNA_volumes'].split(", "))
    except:
        DNA_volumes = (form['DNA_volumes'])

    DNA_volumes = list(map(int, DNA_volumes))

    if form['REG_samples'] == []:
        for DNA_sample in DNA_samples:
           for DNA_volume in DNA_volumes:
                ID_item[DNA_sample] = DNA_volume
                ID_item['BUF'] = cargo_content-DNA_volume
                if adv_form['MM_in_picklist'] == 'YES':
                    ID_item['MM'] = mm_in_reaction
                else:
                    pass
                ID_content_dictionary['ID_'+str(x).zfill(2)] = ID_item
                x = x+1
                ID_item = {}
        if adv_form['MM_in_picklist'] == 'YES':
            ID_P_content = {'DNAP': positive_DNAvol, 'BUF': cargo_content-positive_DNAvol,  'MM' : mm_in_reaction}
            ID_B_content = {'DNAP': 0, 'BUF': cargo_content,  'MM' : mm_in_reaction}
        else:
            ID_P_content = {'DNAP': positive_DNAvol, 'BUF': cargo_content-positive_DNAvol}
            ID_B_content = {'DNAP': 0, 'BUF': cargo_content}
        ID_content_dictionary['ID_P'] = ID_P_content
        ID_content_dictionary['ID_B'] = ID_B_content
    else:
        try:
            REG_samples = form['REG_samples'].split(", ")
        except:
            REG_samples = form['REG_samples']
        fix_names_start(REG_samples, 'REG')
        try:
            REG_volumes = (form['REG_volumes'].split(", "))
        except:
            REG_volumes = (form['REG_volumes'])
        REG_volumes = list(map(int, REG_volumes))
        for DNA_sample in DNA_samples:
            for DNA_volume in DNA_volumes:
                for REG_sample in REG_samples:
                    for REG_volume in REG_volumes:
                        ID_item[REG_sample] = REG_volume
                        ID_item[DNA_sample] = DNA_volume
                        ID_item['BUF'] = cargo_content-DNA_volume-REG_volume
                        if adv_form['MM_in_picklist'] == 'YES':
                            ID_item['MM'] = mm_in_reaction
                        else:
                            pass
                        ID_content_dictionary['ID_'+str(x).zfill(2)] = ID_item
                        x = x+1
                        ID_item = {}
        if adv_form['MM_in_picklist'] == 'YES':
            ID_content_dictionary['ID_P'] = {'DNAP': positive_DNAvol, 'BUF': cargo_content-positive_DNAvol,  'MM' : mm_in_reaction}
            ID_content_dictionary['ID_B'] = { 'DNAP': 0, 'BUF': cargo_content,  'MM' : mm_in_reaction}
        else:
            ID_content_dictionary['ID_P'] = {'DNAP': positive_DNAvol, 'BUF': cargo_content-positive_DNAvol}
            ID_content_dictionary['ID_B'] = {'DNAP': 0, 'BUF': cargo_content}
    return ID_content_dictionary


def add_extra_component(ID_content_dictionary, extra_component, extra_component_volume, criterium):
    for ID in ID_content_dictionary:
        components = ID_content_dictionary[ID].keys() #make a list from the initial components
        for component in list(components):
            if component[0:6] == criterium:
                ID_content_dictionary[ID].update({extra_component : extra_component_volume})
            else:
                pass
    logging.debug('Extra component added: ' + extra_component)
    return ID_content_dictionary


def adjust_buffer(ID_content_dictionary, adv_form):
    cargo_content = adv_form['cargo_content']
    cargo = 0
    for ID in ID_content_dictionary:
        components =  ID_content_dictionary[ID]
        for component, volume in components.items():
            cargo = cargo + volume
        for component in components:
            if component == 'BUF':
                if cargo > cargo_content:
                    components['BUF'] = 0
                    ID_content_dictionary[ID] = components #update the big dictionary
                if cargo < cargo_content:
                    components['BUF'] = cargo_content - cargo
                    ID_content_dictionary[ID] = components #update the big dictionary
                else:
                    pass
            else:
                pass
        cargo = 0
    return  ID_content_dictionary
def fix_buffer_and_mm(ID_content_dictionary, ID_position_dictionary):
    well_count = 1
    vol_inwell = dead_volume
    components = ['BUF']
    if adv_form['MM_in_picklist'] == 'YES':
        components.append('MM')
    else: 
        pass
    for component in components:
        SAMPL  = str(component) + str(well_count)
        for ID in ID_content_dictionary:
            try:
                content = ID_content_dictionary[ID]
                Sum_volume_ID = content[component] * len(get_destination_wells(ID, ID_position_dictionary))
                if vol_inwell+Sum_volume_ID > max_sourcewell_volume:
                    well_count = well_count + 1
                    SAMPL = str(component) + str(well_count)
                    vol_inwell = dead_volume + Sum_volume_ID
                else:
                    vol_inwell = vol_inwell + Sum_volume_ID
                content[SAMPL] = ID_content_dictionary[ID].pop(component)   
            except:
                pass
    return (ID_content_dictionary)
def remove_0_contents(ID_content_dictionary):
    "Remove component of a reaction (or ID), if they are 0."
    for ID in ID_content_dictionary:
        components = list(ID_content_dictionary[ID].keys())
        volumes = list(ID_content_dictionary[ID].values())
        for component, volume in zip(components, volumes):
            if volume == 0:
                ID_content_dictionary[ID].pop(component)
            else:
                pass
    return ID_content_dictionary
#the above 3 functions together
def adjust_sort_remove0(ID_content_dictionary, adv_form):
    ID_content_dictionary.update(adjust_buffer(ID_content_dictionary, adv_form))
    ID_content_dictionary.update(generate_st_content_dictionary(adv_form))
    remove_0_contents(ID_content_dictionary)
    ID_content_dictionary = OrderedDict(sorted(ID_content_dictionary.items()))
    return ID_content_dictionary


#higher level functions for generating the final dictionaries

def generate_ID_position_dictionary(DEST_list, sample_content_dictionary, adv_form):

    st_replicates = adv_form['st_replicates']
    TXTL_replicates = adv_form['TXTL_replicates']
    sample_replicates = adv_form['sample_replicates']
    BP_replicates = adv_form['BP_replicates']
    shuffle = adv_form['shuffle']

    st_content_dictionary = {}
    for ID, content in sample_content_dictionary.items():
        if 'st' in ID:
            st_content_dictionary[ID] = content

    number_of_standard_wells = len(st_content_dictionary) * st_replicates
    # remove the standards, they are already asigned to wells.
    TXTL_IDs_list = list(sample_content_dictionary)
    for key in sample_content_dictionary:
        if 'st' in key:
            TXTL_IDs_list.remove(key)

    number_of_TXTL_wells = len(TXTL_IDs_list) * TXTL_replicates

    if number_of_standard_wells + number_of_TXTL_wells > len(DEST_list):
        sys.exit('Not enough wells! {} in experiment, only {} from {} - P25.'.format
                 (number_of_standard_wells + number_of_TXTL_wells, len(DEST_list),  DEST_list[0]) )
    else:
        pass

    ID_position_dictionary={}
    m = 0
    wells = []
    for x, key in enumerate(sorted(st_content_dictionary.keys())):
        for i in range (st_replicates):
            wells.append(DEST_list[m])
            m = m+1
        ID_position_dictionary[key] = wells
        wells = []

    DEST_list = DEST_list[number_of_standard_wells : (number_of_standard_wells+number_of_TXTL_wells)] #crop to exclude standards for randomisation

    m = 0
    try:
        for ID in TXTL_IDs_list:
            for i in range (sample_replicates):
                if shuffle == 'YES':
                    well= random.choice(DEST_list)
                    wells.append(well)
                    DEST_list.remove(well)
                else:
                    wells.append(DEST_list[m])
                    m = m+1
            ID_position_dictionary[ID] = wells
            wells = []
        if BP_replicates - sample_replicates > 0:
            for i in range (BP_replicates - sample_replicates):
                ID_position_dictionary['ID_P'].append(DEST_list[m])
                m = m + 1
                ID_position_dictionary['ID_B'].append(DEST_list[m])
                m = m + 1
    except:
        print('TXTL wells not asigned')

    ID_position_dictionary = OrderedDict(sorted(ID_position_dictionary.items()))
    logging.debug('ID position dictionary generated')
    return ID_position_dictionary


def generate_Sourcewell_content_dictionary(ID_content_dictionary, ID_position_dictionary):
    dead_volume = 20000 #nL depends on liquid and plate type, this is a safe overestimate
    SourceWell_volume_dictionary = {}
    for ID in ID_content_dictionary:
        contents = ID_content_dictionary[ID]
        for content in contents:
            for i in range (len(ID_position_dictionary[ID])):
                volume = contents[content]
                SourceWell_volume_dictionary[content] = SourceWell_volume_dictionary.get(content, dead_volume) + volume

    #check if max volume is exceeded
    max_source_volume = 65000
    for reagent, totalvolume in SourceWell_volume_dictionary.items():
        if totalvolume > max_source_volume:
            sys.exit('Not enough space in a sourcewell! {}nL of {} needed, {}nL is the maximum. Redesign the experiment!'.format(totalvolume, reagent, max_source_volume))
        else:
            pass

    SourceWell_volume_dictionary_ordered = OrderedDict(sorted(SourceWell_volume_dictionary.items()))
    return SourceWell_volume_dictionary_ordered