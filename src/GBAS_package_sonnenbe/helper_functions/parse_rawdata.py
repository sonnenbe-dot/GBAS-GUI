from typing import Tuple
from pathlib import Path

def main():

    return 0

def get_rawdata(rawdatafolderpath : str, indexcombonameposition : int) -> Tuple[dict, int]:
        number = 0
        rawfile_dict = {}
        rawdatafolderpath = Path(rawdatafolderpath)
        for file_path in rawdatafolderpath.rglob("*"):
            if file_path.is_file():
                if (file_path.suffixes == [".fastq", ".gz"] or file_path.suffix == ".fastq"):
                    number += 1
                    filename = file_path.name
                    indexcombo = filename.split("_")[int(indexcombonameposition)-1]
                    if (indexcombo not in rawfile_dict):
                        rawfile_dict[indexcombo] = 0
                    rawfile_dict[indexcombo] += 1
        return rawfile_dict, number
        
if __name__ == "__main__":
    main()