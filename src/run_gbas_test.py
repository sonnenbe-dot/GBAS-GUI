import multiprocessing as mp
import os, argparse, json, re, shutil
from pathlib import Path
import platform, threading, multiprocessing, time, subprocess

from GBAS_package_sonnenbe.main_CLI import prepare_params, prepare_executables, run_GBAS_CLI, run_GBAS_CLI_memory




def main():

    performance = True
    zipping = False
    
    ###Micromeria###

    current_workspace = Path.cwd()
    test_workspace = current_workspace / ("GBAS_package_sonnenbe/testfolder/spruce_test")
    parameters = [("Outputfolder", str(test_workspace / "output")), ("Bin", str(current_workspace / "bin")), ("Rawdata", str(test_workspace / ("inputs/rawdata"))), ("Primerfile", str(test_workspace / ("inputs/primers_EPIC_and_SSR.txt"))), ("Samplefile", str(test_workspace / ("inputs/samplesheet.txt"))), ("Metadata", str(test_workspace / ("inputs/metadata.xlsx"))), ("Allelelist", "None"), ("Database", "database.db"), ("Maxmismatch", 2), ("Mincount", 20), ("Minlength", 290), ("Consensusthreshold", 0.7), ("Lengthwindow", "310, 600"), ("Filtering", 0.8), ("Ploidy", "diploid"), ("Operatingsystem", platform.system()), ("Uniqueidentifier", "default"), ("Indexcomboposition", 1), ("NumberCores", multiprocessing.cpu_count()-1)]
    parameters_list = ["Outputfolder", "Bin", "Rawdata", "Primerfile", "Samplefile", "Metadata", "Allelelist", "Database", "Maxmismatch", "Mincount", "Minlength", "Consensusthreshold", "Lengthwindow", "Filtering", "Ploidy", "Operatingsystem", "Uniqueidentifier", "Indexcomboposition", "NumberCores"]
    list_mandatory = ["Outputfolder", "Bin", "Rawdata", "Primerfile", "Samplefile"]
    list_not_mandatory = ["Metadata", "Allelelist", "Database"]

    flag, paramsdict = prepare_params(parameters, parameters_list)

    if (not(flag)):
        raise Exception("Preparation of parameters failed!\n\n")

    executables_dict = prepare_executables(paramsdict)
    
    run_GBAS_CLI_memory(paramsdict, executables_dict, parameters_list, list_mandatory, performance, zipping)




if __name__ == "__main__":
    main()