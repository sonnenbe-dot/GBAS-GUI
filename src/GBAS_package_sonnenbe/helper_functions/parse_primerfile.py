
import re
from pathlib import Path

def main():

    return 0

def get_primers(primerfilepath : str) -> dict:
    primers_dict = {}
    primers_dict["primers"] =  {}
    primers_dict["primersboundaries"] = {}
    primerfilepath = Path(primerfilepath)
    with primerfilepath.open("r") as primerfile:
        lines = primerfile.readlines()
        for line in lines:
    # with open(primerfilepath, 'r') as primerfile:
    #     for line in primerfile:
            line = line.rstrip("\r\n")
            if (not line):
                continue
            line_list = re.split('\t|,|;', line)
            if (len(line_list) > 0):
                primername = line_list[0].strip("").rstrip("\r\n\t").lstrip("\r\n\t")
                if (len(line_list) == 3):
                    primers = line_list[1:]
                elif (len(line_list) < 3):
                    print("Primer " + str(primername) + " is incomplete in primerlist, will be ignored! \n")
                    continue
                else:
                    primers = line_list[1:3]
                    boundaries = line_list[3:]
                    boundaries = [(int(element.lstrip('\r\n').rstrip('\r\n').split()[0]), int(element.lstrip().rstrip().split()[1])) for element in line_list[3:]]
                    print("Primer " + str(primername) + " has boundaries! " + str(boundaries) + " \n")
                    primers_dict["primersboundaries"][primername] = boundaries

                primers_dict["primers"][primername] = primers
    primers_dict["primers"] = {k : v for k, v in primers_dict["primers"].items() if k != ""}
    return primers_dict



if __name__ == "__main__":
    main()