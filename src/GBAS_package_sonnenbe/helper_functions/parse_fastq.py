import os
from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import is_valid
from pathlib import Path

def main():
    
    return 0

def parse_fastq(fastqfilepath : Path):
    fastq_dict = {}
    if (is_valid(fastqfilepath) and fastqfilepath.suffix == ".fastq"):
        with open(fastqfilepath, "r") as fastqfile:
            header = ""
            for i, line in enumerate(fastqfile):
                line = line.rstrip('\r\n')
                if (i % 4 == 0):
                    header = line
                    fastq_dict[header] = {}
                elif (i % 4 == 1):
                    fastq_dict[header]["sequence"] = line
                elif (i % 4 == 3):
                    fastq_dict[header]["quality"] = line
    else:
        print("\n fastqfilepath has either no .fastq ending! \n")
    return fastq_dict


if __name__ == "__main__":
    main()