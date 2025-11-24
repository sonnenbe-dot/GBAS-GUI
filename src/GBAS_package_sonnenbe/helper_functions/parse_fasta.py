import os
from pathlib import Path
from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import is_valid 

def main():
    
    return 0

def parse_fasta(fastafilepath : Path) -> dict:
    fasta_dict = {}
    if (is_valid(fastafilepath) and fastafilepath.suffix == ".fasta"):
        with open(fastafilepath) as fastafile:
            for line in fastafile:
                if line.startswith('>'): # head starts with '>'
                    head = line.rstrip('\r\n')[1:] # exclude new line and starting character '>'
                    if head in fasta_dict.keys():
                        head += '_2' # if head already existing in dictionary add _2 sufix so seuqneces with the same head are considered
                    fasta_dict[head] = '' #The value for each head is an empty string, this string will be a sequence in the next step
                else:
                    if (head in fasta_dict.keys()):
                        fasta_dict[head] = line.rstrip('\r\n').upper()
    else:
        print("\n fastafilepath has either no .fasta ending! \n")                
    return fasta_dict


def is_valid(path):
    return (os.path.exists(os.path.normpath(path)) and (os.path.basename(os.path.normpath(path)) != "None") and (os.path.normpath(path) != "") and (os.path.normpath(path) != ".") and (os.path.basename(os.path.normpath(path)) != "."))



if __name__ == "__main__":
    main()