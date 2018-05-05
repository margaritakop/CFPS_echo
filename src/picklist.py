
#functions used to retreive information from the dictionaries
def get_destination_wells(ID, ID_position_dictionary):
    wells = ID_position_dictionary[ID]
    return wells
def get_sourcewell(sample, SourceWell_position_dictionary):
    sourcewell = SourceWell_position_dictionary[sample]
    return sourcewell
def get_transfer_volume(ID, sample, ID_content_dictionary):
    content = ID_content_dictionary[ID]
    volume = content[sample]
    return volume
def get_transfer_type(sample):
    if sample[0:3] == 'BUF' or 'DNA' or 'PBS' or 'FIT':
        trtype = '384PP_AQ_SP'
    if sample[0:3] == 'REG':
        trtype = '384PP_AQ_BP_Plus'
    if sample[0:2] == 'MM':
        trtype = '384PP_AQ_BP'
    return trtype

#the above combined are used to get a complete transfer step for echo instructions
def get_transfer(ID, sample, destwell, ID_content_dictionary, SourceWell_position_dictionary):
    transfer = [destwell,]
    transfer.append(get_sourcewell(sample, SourceWell_position_dictionary))
    transfer.append(get_transfer_volume(ID, sample, ID_content_dictionary))
    transfer.append(ID)
    #transfer.append(get_transfer_type(sample))
    return(transfer)

#functions to output the picklist
def initiate_picklist(picklistfilename):
    picklist = open(picklistfilename, 'w')
    picklist.write("Destination Well, Source Well, Transfer Volume, ID \n")
    picklist.close()
def write_to_picklist(picklistfilename, transfer):
    picklist = open(picklistfilename, 'a')
    for element in transfer:
        picklist.write(str(element) + ',')
    picklist.write('\n')

