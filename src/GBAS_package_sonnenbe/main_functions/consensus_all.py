from pathlib import Path
import customtkinter as ctk
import json, csv, subprocess, os, sys, multiprocessing, math
from itertools import product, combinations_with_replacement

from GBAS_package_sonnenbe.helper_functions.write_fasta import writeFasta
from GBAS_package_sonnenbe.helper_functions.parse_fasta import parse_fasta
from GBAS_package_sonnenbe.helper_functions.parse_fastq import parse_fastq

from GBAS_package_sonnenbe.main_functions.extract_lengths import extract_locinames_from_matrix
from GBAS_package_sonnenbe.helper_functions.parse_samplefile import get_samples

def main():


    return 0





def FindVariants_Likelihoods_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict, performance : bool, number_cores : int):
    mergedout_path = Path(paramsdict["Outputfolder"] + '/MergedOut')
    qualities_path = Path(paramsdict["Outputfolder"] + '/QualityScores')
    allelesout_path = Path(paramsdict["Outputfolder"] + '/AllelesOut')
    variants_path = Path(paramsdict["Outputfolder"] + '/Variants_Likelihoods')
    textbox_pipeline.insert('end-1c', "\nStoring Quality Scores! \n")
    get_quality_scores(mergedout_path, qualities_path, 1)
    textbox_pipeline.insert('end-1c', "\nFinishedStoring Quality Scores! \n")
    textbox_pipeline.insert('end-1c', "\nFinding Variants! \n")
    samples_dict, number_lines = get_samples(paramsdict["Samplefile"])
    FindVariantsAll(allelesout_path, qualities_path, variants_path, samples_dict, float(paramsdict["Consensusthreshold"]), performance, number_cores)
    textbox_pipeline.insert('end-1c', "\nFinished finding Variants! \n")

    # consensustogetherpath = Path(paramsdict["Outputfolder"] + "/ConsensusTogether")
    # length_matrix_json_path = Path(paramsdict["Outputfolder"] + '/MarkerPlots/markermatrix.json')
    # loci_list = extract_locinames_from_matrix(length_matrix_json_path)
    # textbox_pipeline.insert('end-1c', "\nStarting Adding all ConsensusSequences per Marker into 1 file! \n")
    # joinSamplesSameMarker(consensusout_path, consensustogetherpath, loci_list)
    # textbox_pipeline.insert('end-1c', "\nFinished Adding all ConsensusSequences per Marker into 1 file! \n")


def FindVariantsAll(allelesoutpath : Path, qualities_path : Path, variants_path : Path, samples_dict : dict, consensusthreshold : float, performance : bool, number_cores : int):
    quality_scores = {}
    qualities_dict = qualities_path / "quality_scores.json"
    with open(qualities_dict, "r") as f:
        quality_scores = json.load(f)
    
    try:
        if (performance):
            with multiprocessing.Pool(processes = number_cores) as pool:
                processes = []
                args_list = [(allelesoutfilepath, quality_scores, variants_path, samples_dict, consensusthreshold) for allelesoutfilepath in allelesoutpath.iterdir()]
                results = pool.starmap_async(FindVariantsPerFile, args_list)
                processes = results.get()
        else:
            for allelesoutfilepath in allelesoutpath.iterdir():
                FindVariantsPerFile(allelesoutfilepath, quality_scores, variants_path, samples_dict, consensusthreshold)
    except Exception as e:
            print(f"Error when trying to run ConsensusAll! \nException: {e} \n")


def construct_genotype_options_diploid(bases : list, sites : list):
    possible_genotypes = ["".join(genotype) for genotype in product(bases, repeat = len(sites))]
    genotype_pairs = list(combinations_with_replacement(possible_genotypes, 2))
    return possible_genotypes, genotype_pairs

def logsumexp(log_values):
    max_log = max(log_values)
    if max_log == -math.inf:
        return -math.inf
    return max_log + math.log(sum(math.exp(x - max_log) for x in log_values))


def calculate_probability_diploid(genotype_tuple : tuple, read : str, number_sites : int, qualities : list):
    allele_log_probs = []
    for genotype in genotype_tuple: #only 2
        site_log_probs = []
        for i in range(0, number_sites, 1):
            base_error_probability = float(10**((-qualities[i])/10))
            if (read[i] != genotype[i]):
                prob = base_error_probability/3
            else:
                prob = 1-base_error_probability
            if (prob == 0):
                site_log_probs.append(-math.inf)
            else:
                site_log_probs.append(math.log(prob))

        allele_log_prob = sum(site_log_probs)
        allele_log_probs.append(math.log(0.5) + allele_log_prob)
    
    return logsumexp(allele_log_probs)


def FindVariantsPerFile(allelesoutfilepath : Path, quality_scores : dict, variants_path : Path, samples_dict : dict, consensusthreshold : float):
    
    for fastafile in allelesoutfilepath.iterdir():
        if not(fastafile.suffix == ".fasta"):
            continue
        locus = "_".join(fastafile.name.split('_')[0:2])
        sample = fastafile.name.split('_')[2]
        length = fastafile.name.split('_')[4]
        print(locus)
        print(sample)

    bases = ["A", "C", "T", "G"]
    sites = [0, 1, 2]
    possible_genotypes, genotype_pairs_diploid = construct_genotype_options_diploid(bases, sites)

    











def get_quality_scores(input_path : Path, output_path : Path, indexcomboposition : int):
    out = {"Indexcombos" : {}}

    for fastqfile in input_path.iterdir():
        if not(fastqfile.suffix == ".fastq"):
            continue

        indexcombo = fastqfile.name.split("_")[indexcomboposition-1]
        out["Indexcombos"][indexcombo]  = {}
        out["Indexcombos"][indexcombo]["Sequences"]  = {}
        print("Getting Quality scores for sample " + indexcombo + "...\n")
        for header, data in parse_fastq(fastqfile).items():
            quality = data["quality"]
            length = len(data["sequence"])

            out["Indexcombos"][indexcombo]["Sequences"][header] = {}
            list_qualities_converted = []
            for char in quality:
                list_qualities_converted.append(ord(char) - 33) #ord() gets the unicode for the given characters, if its an ASCII character than it givs the ASCII number (0-128)
            out["Indexcombos"][indexcombo]["Sequences"][header] = (length, list_qualities_converted)
    
    output_path.mkdir(parents=True, exist_ok=True)

    out_path = output_path / "quality_scores.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4, ensure_ascii=False)











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


def RunConsensusAll_CLI(paramsdict : dict, performance : bool, number_cores : int):
    allelesout_path = Path(paramsdict["Outputfolder"] + '/AllelesOut')
    consensusout_path = Path(paramsdict["Outputfolder"] + '/ConsensusOut')
    print("\nStarting Building ConsensusSequences! \n")
    RunConsensusAll(allelesout_path, consensusout_path, float(paramsdict["Consensusthreshold"]), performance, number_cores)
    print("\nFinished Building ConsensusSequences! \n")

    consensustogetherpath = Path(paramsdict["Outputfolder"] + "/ConsensusTogether")
    length_matrix_json_path = Path(paramsdict["Outputfolder"] + '/MarkerPlots/markermatrix.json')
    loci_list = extract_locinames_from_matrix(length_matrix_json_path)
    print("\nStarting Adding all ConsensusSequences per Marker into 1 file! \n")
    joinSamplesSameMarker(consensusout_path, consensustogetherpath, loci_list)
    print("\nFinished Adding all ConsensusSequences per Marker into 1 file! \n")


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