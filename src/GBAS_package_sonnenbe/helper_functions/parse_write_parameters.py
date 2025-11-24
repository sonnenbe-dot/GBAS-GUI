import os, platform, subprocess
from typing import List, Tuple
from pathlib import Path

def main():

    return 0



def show_file(filepath : str, operatingsystem : str):
    if (operatingsystem.lower() == "windows"):
        os.startfile(filepath)
    elif(operatingsystem.lower() == "linux"):
        subprocess.call(["xdg-open", filepath])


def parse_parameterfile(parameterfilepath : str) -> dict: 
    paramsdict = {}
    parameterfilepath = Path(parameterfilepath)
    with parameterfilepath.open("r") as parameterfile:
        lines = parameterfile.readlines()
        for line in lines:
            line = line.rstrip("\r\n")
            if (not line) or line.startswith("#"):
                continue
            elements = line.split("=")
            key = elements[0].rstrip("\r\n").strip()
            value = elements[1].rstrip("\r\n").strip(".").strip()
            if (value and value != "."):
                paramsdict[key] = value
    return paramsdict


def check_paramsdict(paramsdict : dict, paramslist : list) -> bool:
    check = True
    if not paramsdict:
        check = False
        print("Parameterdict is empty! No parameters found! \n\n")
    else:
        for param in paramslist:
            if (str(param) not in paramsdict):
                check = False
                print("The key " + str(param) + " is not in paramdict! Check the parameterfile templet! \n\n")
                break
    return check


def new_paramsdict(paramslist : list[Tuple[str, str]]) -> dict:
    paramsdict = {}
    for param in paramslist:
        paramsdict[param[0]] = param[1]
    return paramsdict


def write_parameterfile(paramsdict : dict, parameterfilepath : str):
    parameterfilepath_new = Path(parameterfilepath)
    with parameterfilepath_new.open("w") as parameterfile:
        parameterfile.write("###Parameters for the Pipeline \n\n")
        for key, value in paramsdict.items():
            description = write_parameterfile_helper(key)
            parameterfile.write(description)
            parameterfile.write(key + " = " + str(value) + "\n")
            if (key == "Allelelist" or key == "Rawdata" or key == "Lengthwindow"):
                parameterfile.write("\n")
    if (platform.system().lower() == "windows"):
        os.startfile(parameterfilepath)
    elif (platform.system().lower() == "linux"):
        subprocess.run(["xdg-open", parameterfilepath], check=True)
    print("Parameters saved in: \n" + parameterfilepath + "\n\n")


def write_parameterfile_helper(keystring : str) -> str:
    default = "# \n"
    match keystring:
        case "Outputfolder":
            return "#Name of the Folder where results of the pipeline are stored: \n"
        case "Bin":
            return "#Path to the Bin Folder where Trimmo, Usearch and R executables are stored: \n"
        case "Rawdata":
            return "#Path to the Folder containing raw fastq/fastq.gz files: \n"
        case "Primerfile":
            return "#Path to the File containing primer information (.txt): \n"
        case "Samplefile":
            return "#Path to the File containing sample information (.txt or .csv): \n"
        case "Rexecutable":
            return "#Path to the Rexecutable (Only needed in windows) (.exe): \n"
        case "Allelelist":
            return "#Path to the Allelelist for GBAS (if user wants to do listbased Call) (.txt): \n"
        case "Metadata":
            return "#Path to the Metadata for GBAS outputs (.xlsx): \n"
        case "Barcodelist":
            return "#Path to the Barcodejson for Barcoding/Metabarcoding (.json): \n"
        case "Database":
            return "#Path to the SqLite Database for GBAS Outputs (.db): \n"
        case "Maxmismatch":
            return "#Maximum number of mismatches between primer and amplicon sequences (integer; default=2) \n"
        case "Mincount":
            return "#Minimum number of read count for an allele to be considered (integer; default = 20) \n"
        case "Minlength":
            return "#Minimum amplicon length to be considered (integer; default=250) \n"
        case "Consensusthreshold":
            return "#Consensusthreshold (float; default = 0.7) \n"
        case "Lengthwindow":
            return "#boundaries on the x-axis of Markerplots \n"
        case "Ploidy":
            return "#Ploidy level of the data (haploid = barcoding, diploid = SSR): \n"
        case "Operatingsystem":
            return "#Operating system of the current user (default = windows): \n"
        case "Uniqueidentifier":
            return "#Unique identifier for each sequence: \n"
        case "Indexcomboposition":
            return "#Position of the indexcombination in the raw fastqfilename (default = 1): \n"
        case "NumberCores":
            return "#Number of Cores used when using the Parallelized Pipeline version: \n"
    return default

def is_valid(path: str) -> bool:
    p = Path(path)
    #return (p.exists())
    return (p.exists() and p.name != "None" and str(p) not in ("", ".") and p.name != ".")

# def is_valid(path):
#     return (os.path.exists(os.path.normpath(path)) and (os.path.basename(os.path.normpath(path)) != "None") and (os.path.normpath(path) != "") and (os.path.normpath(path) != ".") and (os.path.basename(os.path.normpath(path)) != "."))

if __name__ == "__main__":
    main()