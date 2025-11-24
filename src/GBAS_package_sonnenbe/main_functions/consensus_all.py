from pathlib import Path
import customtkinter as ctk
import json, csv, subprocess, os, sys, multiprocessing

from GBAS_package_sonnenbe.helper_functions.write_fasta import writeFasta
from GBAS_package_sonnenbe.helper_functions.parse_fasta import parse_fasta
from GBAS_package_sonnenbe.helper_functions.parse_fastq import parse_fastq

from GBAS_package_sonnenbe.main_functions.extract_lengths import extract_locinames_from_matrix

def main():


    return 0


def RunConsensusAll_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict, performance : bool, number_cores : int):
    allelesout_path = Path(paramsdict["Outputfolder"] + '/AllelesOut')
    consensusout_path = Path(paramsdict["Outputfolder"] + '/ConsensusOut')
    textbox_pipeline.insert('end-1c', "\nStarting Building ConsensusSequences! \n")
    RunConsensusAll(allelesout_path, consensusout_path, float(paramsdict["Consensusthreshold"]), performance, number_cores)
    textbox_pipeline.insert('end-1c', "\nFinished Building ConsensusSequences! \n")

    consensustogetherpath = Path(paramsdict["Outputfolder"] + "/ConsensusTogether")
    length_matrix_json_path = Path(paramsdict["Outputfolder"] + '/MarkerPlots/markermatrix.json')
    loci_list = extract_locinames_from_matrix(length_matrix_json_path)
    textbox_pipeline.insert('end-1c', "\nStarting Adding all ConsensusSequences per Marker into 1 file! \n")
    joinSamplesSameMarker(consensusout_path, consensustogetherpath, loci_list)
    textbox_pipeline.insert('end-1c', "\nFinished Adding all ConsensusSequences per Marker into 1 file! \n")


def joinSamplesSameMarker(consensusout_path : Path, consensustogetherpath : Path, loci_list : list):
    for locus in loci_list:
        print(f"Adding all Consensussequences for Locus {locus} into one file. \n")
        output_fasta_path = consensustogetherpath / (locus + '_together.fasta')
        with open(output_fasta_path, 'w') as output_fasta:
            for file in consensusout_path.iterdir():
                if (file.stem.startswith(locus+"_") and file.suffix == ".fasta"):
                    #input_fasta_path = Path(consensusout_path + '/' + file)
                    with open(file) as input_fasta:
                        for line in input_fasta:
                            output_fasta.write(line)
    

def RunConsensusAll(allelesoutpath : Path, consensusoutpath : Path, consensusthreshold : float, performance : bool, number_cores : int):
    try:
        if (performance):
            with multiprocessing.Pool(processes = number_cores) as pool:
                processes = []
                args_list = [(allelesoutfilepath, consensusoutpath, consensusthreshold) for allelesoutfilepath in allelesoutpath.iterdir()]
                results = pool.starmap_async(MakeConsensusPerFile, args_list)
                processes = results.get()
        else:
            for allelesoutfilepath in allelesoutpath.iterdir():
                MakeConsensusPerFile(allelesoutfilepath, consensusoutpath, consensusthreshold)
    except Exception as e:
            print(f"Error when trying to run ConsensusAll! \nException: {e} \n")
            
    
def MakeConsensusPerFile(allelesoutfilepath : Path, consensusoutpath : Path, consensusthreshold : float):
    fasta_dict = parse_fasta(allelesoutfilepath)
    nr_seqs = len(fasta_dict)

    #check if file has sequences with different lengths:
    seq_length_fixed = len(list(fasta_dict.values())[0])
    different_lengths = [seq for header, seq in fasta_dict.items() if (len(seq) != seq_length_fixed)]
    if (different_lengths):
        raise Exception("Different Sequence Lengths in the file " + allelesoutfilepath.name + " \n")

    data = {}
    for i in range(0, seq_length_fixed, 1): # iterate through positions
        nuc = [] #list of all nucleotides for each sequence in the file at a certain position i
        for header, sequence in fasta_dict.items():
            nuc.append(sequence[i]) # save nucleotides for all sequences into a list
        data[i] = nuc
    
    outName = allelesoutfilepath.stem + '_C_' + str(nr_seqs)
    con_sequence_file_path = consensusoutpath / (outName + '_' + str(int(float(consensusthreshold)*100)) + '.fasta')
    frequency_file_path = consensusoutpath / (outName + '.txt')

    with open (con_sequence_file_path, 'w') as cons_file:
        with open(frequency_file_path, 'w') as freq_file:
            conSeq = '>' + outName + '\n' # consensus sequence head
            freq_file.write('Position' + '\t' + 'Freq(A)' + '\t' + 'Freq(C)' + '\t' + 'Freq(G)' + '\t' + 'Freq(T)' + '\t' + '\n')
            for position, nuc in data.items(): #nuc is a list of nucleotides for the position rec for all sequences in the file
                temp = str(position + 1) # position in sequence
                # it assumes N as the defoult nucleotide and only replaces it if a nucleotyde has a frequency above the threashold
                base = 'N' # define nucleotide as N
                for nucleotide in ['A', 'C', 'G', 'T']:
                    freq = float(nuc.count(nucleotide))/len(nuc) # get frequency from each nucleotide #nr_seq should be the same value as len(nuc)
                    temp += '\t' + str(freq) # save fequency in freq file
                    #check of nucleotide frequncy is above the threashold
                    if freq >= float(consensusthreshold):
                        base = nucleotide 
                    #else:
                        #self.files_addedN.append(os.path.basename(os.path.normpath(con_sequence_file_path)))
                freq_file.write(temp + '\n')
                conSeq += base # save nucleotide in consensus sequence
            cons_file.write(conSeq + '\n')

if __name__ == "__main__":
    main()