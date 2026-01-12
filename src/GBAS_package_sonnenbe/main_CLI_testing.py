import os, argparse, json, re, shutil
from pathlib import Path
import platform, threading, multiprocessing, time, subprocess

import psutil

from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import parse_parameterfile, check_paramsdict, new_paramsdict

def main():

    ###Testing on Spruce subset###

    current_workspace = Path.cwd()
    
    test_workspace = current_workspace / ("testfolder"/"spruce_test")

    parameters = [("Outputfolder", str(test_workspace / "output")), ("Bin", str(current_workspace / "bin")), ("Rawdata", str(test_workspace / ("inputs/rawdata"))), ("Primerfile", str(test_workspace / ("inputs/primers_EPIC_and_SSR.txt"))), ("Samplefile", str(test_workspace / ("inputs/samplesheet.txt"))), ("Metadata", str(test_workspace / ("inputs/metadata.xlsx"))), ("Allelelist", "None"), ("Database", "database.db"), ("Maxmismatch", 2), ("Mincount", 20), ("Minlength", 290), ("Consensusthreshold", 0.7), ("Lengthwindow", "310, 600"), ("Filtering", 0.8), ("Ploidy", "diploid"), ("Operatingsystem", platform.system()), ("Uniqueidentifier", "default"), ("Indexcomboposition", 1), ("NumberCores", multiprocessing.cpu_count()-1)]
    parameters_list = ["Outputfolder", "Bin", "Rawdata", "Primerfile", "Samplefile", "Metadata", "Allelelist", "Database", "Maxmismatch", "Mincount", "Minlength", "Consensusthreshold", "Lengthwindow", "Filtering", "Ploidy", "Operatingsystem", "Uniqueidentifier", "Indexcomboposition", "NumberCores"]


    return 0