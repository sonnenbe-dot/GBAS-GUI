
import re, os
from pathlib import Path
from typing import Tuple

def main():

    return 0

def get_samples(samplesfilepath : str) -> Tuple[dict, int]:
    samples_dict = {
        "forward" : {}, #sampleleft : sampleright
        "reverse" : {}, #sampleright : sampleleft
        "linksforward" : {}, #oldsamplename : newsamplename
        "linksreverse" : {} #newsamplename : oldsamplename
    }
    number_lines = 0
    samplesfilepath = Path(samplesfilepath)
    with samplesfilepath.open("r") as samplefile:
        lines = samplefile.readlines()
        for line in lines:
    # with open(os.path.normpath(samplesfilepath)) as samplefile:
    #     for line in samplefile:
            line = line.rstrip("\r\n")
            number_lines += 1
            samplename_left = re.split(',|\t|;', line)[0].strip()
            samplename_right = re.split(',|\t|;', line)[1].strip()
            samplename_right_new = samplename_right.replace("_", "").replace(".", "").replace(",", "")
            if (samplename_left not in samples_dict["forward"]):
                samples_dict["forward"][samplename_left] = samplename_right_new
                samples_dict["linksforward"][samplename_right] = samplename_right_new
                samples_dict["linksreverse"][samplename_right_new] = samplename_right
            if (samplename_right_new not in samples_dict["reverse"]):
                samples_dict["reverse"][samplename_right_new] = samplename_left
    return samples_dict, number_lines

def get_samples_duplicates(samples_dict : dict) -> Tuple[dict, dict]:
    samplesleft_dict = {}
    samplesright_dict = {}
    for sampleleft, sampleright in samples_dict["forward"].items():
        if (sampleright not in samplesright_dict):
            samplesright_dict[sampleright] = 0
        samplesright_dict[sampleright] += 1
    for sampleright, sampleleft in samples_dict["reverse"].items():
        if (sampleleft not in  samplesleft_dict):
             samplesleft_dict[sampleleft] = 0
        samplesleft_dict[sampleleft] += 1
    return samplesleft_dict, samplesright_dict

def get_rawsamples_list(samples_dict : dict) -> list:
    return [key for key, count in samples_dict["forward"].items()]




if __name__ == "__main__":
    main()