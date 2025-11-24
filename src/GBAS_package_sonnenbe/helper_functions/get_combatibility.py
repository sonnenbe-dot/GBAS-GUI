


def main():


    return 0


def samples_to_process(indexcomboslist : str, rawfilenameslist : str) -> int:
    number = 0
    for indexcombo in indexcomboslist:
            for file in rawfilenameslist:
                if (indexcombo in file):
                    number += 1
    return number 