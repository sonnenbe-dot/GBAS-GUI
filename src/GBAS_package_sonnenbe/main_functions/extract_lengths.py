from pathlib import Path
import customtkinter as ctk
import json, csv, subprocess, os, sys

from GBAS_package_sonnenbe.helper_functions.write_fasta import writeFasta
from GBAS_package_sonnenbe.helper_functions.parse_fasta import parse_fasta
from GBAS_package_sonnenbe.helper_functions.parse_fastq import parse_fastq

def main():

    return 0

def run_Length_Extraction_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict):
    length_matrix_json = Path(paramsdict["Outputfolder"] + '/MarkerPlots/markermatrix.json')
    separatoutpath = Path(paramsdict["Outputfolder"] + '/SeparatOut')
    allelesout_path = Path(paramsdict["Outputfolder"] + '/AllelesOut')
    textbox_pipeline.insert('end-1c', "\nStarting Length Extraction! \n")
    run_Length_Extraction(length_matrix_json, separatoutpath, allelesout_path)
    textbox_pipeline.insert('end-1c', "\nFinished Length Extraction! \n")

def run_Length_Extraction_CLI(paramsdict : dict):
    length_matrix_json = Path(paramsdict["Outputfolder"] + '/MarkerPlots/markermatrix.json')
    separatoutpath = Path(paramsdict["Outputfolder"] + '/SeparatOut')
    allelesout_path = Path(paramsdict["Outputfolder"] + '/AllelesOut')
    print("\n\nStarting Length Extraction! \n\n")
    run_Length_Extraction(length_matrix_json, separatoutpath, allelesout_path)
    print("\n\nFinished Length Extraction! \n\n")

def extract_locinames_from_matrix(length_matrix_path_json : Path) -> list:
    markermatrix_dict = {}
    with open(length_matrix_path_json) as json_file:
        markermatrix_dict = json.load(json_file)
    return [locus for locus in markermatrix_dict.keys()]

def extract_samplenames_from_matrix(length_matrix_path_json : Path) -> list:
    markermatrix_dict = {}
    with open(length_matrix_path_json) as json_file:
        markermatrix_dict = json.load(json_file)
    return [sample for sample in markermatrix_dict[list(markermatrix_dict.keys())[0]]["Samples"]]

def run_Length_Extraction(length_matrix_json : Path, separatoutpath : Path, allelesout_path : Path):
    markermatrix_dict = {}
    with open(length_matrix_json) as json_file:
        markermatrix_dict = json.load(json_file)
    
    loci = [locus for locus in markermatrix_dict.keys()]
    samples = [sample for sample in markermatrix_dict[list(markermatrix_dict.keys())[0]]["Samples"]]

    for sample in samples:
        for locus in loci:
            print('\n\nProcessing sample ' + sample + ' for locus ' + locus + '\n')
            print("Lengths: \n")
            separatout_filepath = Path(separatoutpath / (sample + "_" + locus + ".fasta"))
            #print(separatout_filepath)
            print("Locus: " + str(locus) + " \n")
            # if (not(sample in markermatrix_dict[locus]["Samples"])):
            #     continue
            if (markermatrix_dict[locus]["Samples"][sample]["LengthAlleles"]):
                print('......genotype:')
                for length, count in markermatrix_dict[locus]["Samples"][sample]["LengthAlleles"].items():
                    print(str(length) + "\n")
                    outFasta = Path(allelesout_path / (locus + '_' + sample +  '_Al_' + length + '.fasta'))
                    extracted_sequences_dict = extract_sequences_per_length(separatout_filepath, int(length))
                    if (not(extracted_sequences_dict)):
                         print('\nNo sequence found for allele length ' + length + "\n")
                    else:
                        print("\n" + str(len(extracted_sequences_dict)) + " sequences found for Sample " + sample + ", locus " + locus + " genotype length " + length + "\n")
                        writeFasta(extracted_sequences_dict, outFasta)
    print("\nFinished extracting lengths.\n")


def extract_sequences_per_length(separatout_filepath : Path, length : int):
    result = {}
    if (separatout_filepath.suffix == ".fasta"):
        for header, sequence in parse_fasta(separatout_filepath).items():
            if (len(sequence) == length and sequence.count("N") == 0):
                result[header] = sequence
    elif (separatout_filepath.suffix == ".fastq"):
        for header, data in parse_fastq(separatout_filepath).items():
            sequence = data["sequence"]
            if (len(sequence) == length and sequence.count("N") == 0):
                result[header] = sequence
    else:
        print(f"filepath \n {separatout_filepath.name} has wrong filetype!\n")
    return result
    


if __name__ == "__main__":
    main()