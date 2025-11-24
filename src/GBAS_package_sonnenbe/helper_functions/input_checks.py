from pathlib import Path

from GBAS_package_sonnenbe.helper_functions.parse_samplefile import get_samples
from GBAS_package_sonnenbe.helper_functions.parse_primerfile import get_primers
from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import is_valid
from GBAS_package_sonnenbe.helper_functions.parse_executables import check_executables
from GBAS_package_sonnenbe.helper_functions.parse_rawdata import get_rawdata
from GBAS_package_sonnenbe.helper_functions.parse_samplefile import get_samples, get_samples_duplicates, get_rawsamples_list
from GBAS_package_sonnenbe.helper_functions.get_combatibility import samples_to_process
from GBAS_package_sonnenbe.helper_functions.parse_primerfile import get_primers

def main():


    return 0


def check_inputs(paramsdict : dict, executables_dict : dict, params_list : list, list_mandatory : list):
    flag_executables = check_executables(executables_dict)

    flag_rawfiles_duplicate = False

    flag_samplesleft_duplicate = False
    flag_samplesright_duplicate = False

    inputs_mandatory_flag = True
    for param in list_mandatory:
        if (not(is_valid(str(paramsdict[param])))):
            inputs_mandatory_flag = False
    
    if (not(flag_executables) and not(inputs_mandatory_flag)):
        return 0
    
    rawfile_dict, rawfile_number = get_rawdata(paramsdict["Rawdata"], paramsdict["Indexcomboposition"])
    duplicate_rawsamples = [key for key, count in rawfile_dict.items() if (count > 2)]
    if (duplicate_rawsamples):
        flag_rawfiles_duplicate = True
    
    samples_dict, number_lines = get_samples(paramsdict["Samplefile"])
    samplesleft_dict, samplesright_dict = get_samples_duplicates(samples_dict)
    duplicate_samplesleft = [key for key, count in samplesleft_dict.items() if (count > 1)]
    duplicate_samplesright = [key for key, count in samplesright_dict.items() if (count > 1)]

    if (duplicate_samplesleft):
        flag_samplesleft_duplicate = True
    if (duplicate_samplesleft):
        flag_samplesleft_duplicate = True
    
    primers_flag = True
    primers_dict = get_primers(paramsdict["Primerfile"])
    if (not(primers_dict)):
        primers_flag = False
    
    return (not(flag_rawfiles_duplicate) and not(flag_samplesleft_duplicate) and not(flag_samplesleft_duplicate) and primers_flag)

if __name__ == "__main__":
    main()