from pathlib import Path
import customtkinter as ctk
from collections import Counter

from GBAS_package_sonnenbe.helper_functions.parse_fasta import parse_fasta

def main():


    return 0

def RunVariants_Determination_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict):
    consensustogetherpath = Path(paramsdict["Outputfolder"] + "/ConsensusTogether")
    allelesoutpath = Path(paramsdict["Outputfolder"] + "/AllelesOut")
    correctedpath = Path(paramsdict["Outputfolder"] + "/Corrected")
    textbox_pipeline.insert('end-1c', "\nStarting Determining Variants! \n")
    RunVariants_Determination(consensustogetherpath, allelesoutpath, correctedpath, paramsdict["Ploidy"], int(paramsdict["Mincount"]))
    textbox_pipeline.insert('end-1c', "\nFinished Determining Variants! \n")


def RunVariants_Determination(consensustogetherpath : Path, allelesoutpath : Path, correctedpath : Path, ploidy : str, mincount : int):
    for consensus_file_path in consensustogetherpath.iterdir():
        correctedfastafilepath = Path(correctedpath / (consensus_file_path.stem + "_Corr.fasta"))
        print(f"\nDetermine Variants for file {consensus_file_path.name}\n")
        if (ploidy.lower() == "diploid"):
            new_variants_per_file = correctSequences(consensus_file_path, allelesoutpath, correctedfastafilepath, mincount)
        elif (ploidy.lower() == "haploid"):
            correctSequences_Hap(consensus_file_path, allelesoutpath, correctedfastafilepath, mincount)
        else:
            print(ploidy.lower() + " must be either diploid or haploid! Pipeline cannot continue! \n")
            break

def correctSequences(consensus_file_path : Path, allelesoutpath : Path, correctedfastafilepath : Path, mincount : int):
    Npositions_dict = {}
    names_info = {}
    for header, sequence in parse_fasta(consensus_file_path).items():
        if sequence != '':
            Npositions_dict[(header, sequence)] = get_Ns_records(sequence) #For this particular sequence with unique header get all base positions where the base is N
            #Consensustogethersequences can only have N bases at certain positions if the bases at these positions from corresponding sequences from the allelesoutfolder did not read a frequency equal to the consensusthreshold!
            samplename = header.split('_')[2]
            # For a diploid invididual at a certain locus we can have 2 different or 2 same allele lengths (gene variants)
            # If the samplename appears 2 times in the consensusfasta it means we have 2 different lengths
            # Each length corresponds to one allele.
            # However if the samplename appears only once it means we have the same length twice and thus for this one length we can have 2 alleles
            if samplename in names_info: 
                names_info[samplename] = 1 
            else:
                names_info[samplename] = 2
    
    with open(correctedfastafilepath, 'w') as output:
        Samples_to_exclude = []
        DataOut = {}
        for name_seq, Npositions in Npositions_dict.items():
            header = name_seq[0]
            sequence = name_seq[1]
            samplename = header.split("_")[2]
            length = header.split("_")[4]
            number_sequences = int(header.split('_')[-1])

            allelesoutfilepath = Path(allelesoutpath / ('_'.join(header.split('_')[:5]) + '.fasta'))
            het_info = names_info[samplename]

            Counter_dict = get_seq_freq(allelesoutfilepath, Npositions) #Counter dict is a dict with sequences (keys) formed from Npositions of each sequence from allelesoutfile and the corresponding counts (how often they appear)
            print(f"\nGet variants for sample {samplename} for length {length}\n")
            variants = get_variants(Counter_dict, het_info) #list with retried variants, either 2, 1 or zero variants (the latter when the consensustogethersequence has no Ns and thus no variants can be retrieved!) 

            if variants[0].count('N') > 0:
                Samples_to_exclude.append(samplename)
                print(samplename + ' excluded for ambiguous SNPs')

            corrected_sequences = [] #can be either 1 or 2 corrected sequences
            #All consensussequences from the consensustogether file fasta will have their N's replaced by the found variants 
            #If the consensussequence does not have Ns then no replacement needs to be made and that sequence is already an allele for that respective locus
            if number_sequences > int(mincount):
                for variant in variants:
                    corrected_sequence = ""
                    for i, base in enumerate(sequence, 0):
                        if (base == "N" and i in Npositions):
                            corrected_sequence += variant[Npositions.index(i)]
                        else:
                            corrected_sequence += base
                    corrected_sequences.append(corrected_sequence)

                DataOut[header] = corrected_sequences
                # if (len(corrected_sequences) == 2):
                #     new_variants_number += 1
            else:
                Samples_to_exclude.append(samplename)
                print(samplename + ' excluded for too little reads')
        
        for header, corrected_sequences in DataOut.items():
            print("Filtering...")
            sampleName = header.split('_')[2]
            print(sampleName)
            if sampleName not in Samples_to_exclude:
                # All sequences will be save with '_0' at the end of the name. In case of heterozygotes SNPs the second sequence will be saved with '_1'
                for c, corrected_sequence in enumerate(corrected_sequences, 0):
                    output.write('>' + header + '_' + str(c) + '\n' + corrected_sequence + '\n')






def correctSequences_Hap(consensus_file_path : Path, allelesoutpath : Path, correctedfastafilepath : Path, mincount : int):
    Npositions_dict = {}
    names_info = {}
    for header, sequence in parse_fasta(consensus_file_path).items():
        if sequence != '':
            Npositions_dict[(header, sequence)] = get_Ns_records(sequence) #For this particular sequence with unique header get all base positions where the base is N
            

    with open(correctedfastafilepath, 'w') as output:
        Samples_to_exclude = []
        DataOut = {}
        for name_seq, Npositions in Npositions_dict.items():
            header = name_seq[0]
            sequence = name_seq[1]
            samplename = header.split("_")[2]
            length = header.split("_")[4]
            number_sequences = int(header.split('_')[-1])

            allelesoutfilepath = Path(allelesoutpath / ('_'.join(header.split('_')[:5]) + '.fasta'))
            #het_info = names_info[samplename]

            Counter_dict = get_seq_freq(allelesoutfilepath, Npositions) #Counter dict is a dict with sequences (keys) formed from Npositions of each sequence from allelesoutfile and the corresponding counts (how often they appear)
            print(f"\nGet variants for sample {samplename} for length {length}\n")
            variants = get_variants(Counter_dict, 1) #list with retried variants, either 2, 1 or zero variants (the latter when the consensustogethersequence has no Ns and thus no variants can be retrieved!) 

            if variants[0].count('N') > 0:
                Samples_to_exclude.append(samplename)
                print(samplename + ' excluded for ambiguous SNPs')

            corrected_sequences = [] #can be either 1 or 2 corrected sequences
            #All consensussequences from the consensustogether file fasta will have their N's replaced by the found variants 
            #If the consensussequence does not have Ns then no replacement needs to be made and that sequence is already an allele for that respective locus
            if number_sequences > int(mincount):
                for variant in variants:
                    corrected_sequence = ""
                    for i, base in enumerate(sequence, 0):
                        if (base == "N" and i in Npositions):
                            corrected_sequence += variant[Npositions.index(i)]
                        else:
                            corrected_sequence += base
                    corrected_sequences.append(corrected_sequence)

                DataOut[header] = corrected_sequences
                # if (len(corrected_sequences) == 2):
                #     new_variants_number += 1
            else:
                Samples_to_exclude.append(samplename)
                print(samplename + ' excluded for too little reads')
        
        for header, corrected_sequences in DataOut.items():
            print("Filtering...")
            sampleName = header.split('_')[2]
            print(sampleName)
            if sampleName not in Samples_to_exclude:
                # All sequences will be save with '_0' at the end of the name. In case of heterozygotes SNPs the second sequence will be saved with '_1'
                for c, corrected_sequence in enumerate(corrected_sequences, 0):
                    output.write('>' + header + '_' + str(c) + '\n' + corrected_sequence + '\n')






def get_variants(Counter_dict : dict, number_alleles_allowed : int):
    #variants_counts = [] #Contains the counts of the sequence variants (built by the N positions of each sequences in the allelesoutfilepath)
    variants_counts = [count for variant, count in Counter_dict.items()] #Contains the counts of the sequence variants (built by the N positions of each sequences in the allelesoutfilepath)
    #for variant, count in Counter_dict.items():
        #variants_counts.append(count)
    variants_counts.sort() #Sort the counts in ascending order
    highest_counts = variants_counts[-number_alleles_allowed:] #get last 2 or 1 counts (these will be the 2 highest or 1 highest count)
    variant_results = [] #storing all variants which correspond to highest 2/1 counts
    incHapCount = 0 # count summ of the included haplotypes
    excHapCount = 0 # count summ of the excluded haplotypes
    for variant, count in Counter_dict.items():
        if count in highest_counts: #include the variant only if its count number is in the highest_counts list
            variant_results.append(variant) 
            incHapCount += count
        else:
            excHapCount += count
    print('included: ' + str(incHapCount) + ' excluded: ' + str(excHapCount) + ' nr. haps: ' + str(len(variant_results)))
    if (len(variant_results) == number_alleles_allowed and incHapCount > excHapCount):
        return variant_results
    else:
        return ['N' * len(variant_results[0])]

def get_seq_freq(allelesoutfilepath : Path, Npositions : list) -> dict:
    haps = [] #list which contains all the nucleotides at the positions of Npositions for each sequence in the allelesoutfastafile
    for header, sequence in parse_fasta(allelesoutfilepath).items():
        hap = ""
        for i in Npositions:
            hap += sequence[i]
        haps.append(hap) #Each element of haps list is a series of nucleotides at the N positions of the consensus sequences
    return dict(Counter(haps))

def get_Ns_records(sequence : str) -> list:
    positions = [] #list containing all N positions of the sequence
    for i, nucleotide in enumerate(sequence):   
        if (nucleotide.upper() == "N"):
            positions.append(i)
    positions.sort()
    return positions


if __name__ == "__main__":
    main()