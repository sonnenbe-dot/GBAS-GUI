from pathlib import Path

import json, math, multiprocessing

import numpy as np

from GBAS_package_sonnenbe.helper_functions.parse_fastq import parse_fastq
from GBAS_package_sonnenbe.helper_functions.parse_fasta import parse_fasta
from GBAS_package_sonnenbe.helper_functions.parse_samplefile import get_samples

from itertools import product, combinations_with_replacement

from collections import Counter

import customtkinter as ctk




def main():

    print("Extracting Quality Scores.\n")

    inputs_path_str = r"C:\Users\Sebastian\Documents\Micromeria_test\inputs"
    inputs_path = Path(inputs_path_str)

    mergedout_path_str = r"C:\Users\Sebastian\Documents\Micromeria_test\outputs\output_2samples_2primers\MergedOut"
    output_path_str = r"C:\Users\Sebastian\Documents\Micromeria_test\output_quality_scores"
    allelesout_path_str = r"C:\Users\Sebastian\Documents\Micromeria_test\outputs\output_2samples_2primers\AllelesOut_test3" #AllelesOut_test #AllelesOut_test2, AllelesOut
    
    #samplelist_path_str r"C:\Users\Sebastian\Documents\Micromeria_test\inputs\samples.txt"

    mergedout_path = Path(mergedout_path_str)
    output_qualityscores_path = Path(output_path_str)

    # print("Extracting Quality Scores from files in " + str(mergedout_path) + " \n")
    # get_quality_scores_new(mergedout_path, output_qualityscores_path, 1)

    #get_quality_scores(mergedout_path, output_path, 1)

    # allelesout_path = Path(allelesout_path_str)
    # json_input_path = output_path / "quality_scores.json"
    # samplelist_path = inputs_path / "samples.txt"
    # outputpath = Path(r"C:\Users\Sebastian\Documents\Micromeria_test\output_likelihoods")
    # outputpath_multiple = Path(r"C:\Users\Sebastian\Documents\Micromeria_test\output_likelihoods_multiple")

    mergedout_path = Path(mergedout_path_str)
    output_qualityscores_path = Path(output_path_str)
    allelesout_path = Path(allelesout_path_str)
    samplelist_path = inputs_path / "samples.txt"
    outputpath_multiple = Path(r"C:\Users\Sebastian\Documents\Micromeria_test\variants_likelihoods")

    calculate_likelihoods_diploid(mergedout_path, output_qualityscores_path, allelesout_path, samplelist_path, outputpath_multiple, 0.7, 1, True, 15, 5)


    return 0



def calculate_likelihoods_diploid_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict, performance : bool, number_cores : int, base_positions_number : int):
    #input paths
    mergedout_path = Path(paramsdict["Outputfolder"] + '/MergedOut')
    allelesout_path = Path(paramsdict["Outputfolder"] + '/AllelesOut')
    samples_dict, number_lines = get_samples(paramsdict["Samplefile"])
    consensusthreshold = float(paramsdict["Consensusthreshold"])
    indexcomboposition = int(paramsdict["Indexcomboposition"])

    #output paths:
    qualities_path = Path(paramsdict["Outputfolder"] + '/QualityScores')
    variants_path = Path(paramsdict["Outputfolder"] + '/Variants_Likelihoods')
    corrected_path = Path(paramsdict["Outputfolder"] + '/Corrected')
    
    #Calling likelihood calculation (diploid)
    # textbox_pipeline.insert('end-1c', "\nCalculating likelihoods to determine sequence variants. \n")
    # calculate_likelihoods_diploid(mergedout_path, qualities_path, allelesout_path, samples_dict, variants_path, consensusthreshold, indexcomboposition, performance, number_cores, base_positions_number)
    # joinSamplesSameMarker(variants_path, corrected_path)
    # textbox_pipeline.insert('end-1c', "\nFinished calculating likelihoods to determine sequence variants. \n")

    textbox_pipeline.insert('end-1c', "\nSorry.\nCalling alleles based on genotype likelihoods is currently broken. Fix will come soon.\n")



def joinSamplesSameMarker(variants_path : Path, corrected_path : Path):
    loci_list = []
    for fastafile in variants_path.iterdir():
        if not(fastafile.suffix == ".fasta"):
            continue
        locus = "_".join(fastafile.name.split('_')[0:2])
        if (locus not in loci_list):
            loci_list.append(locus)

    for locus in loci_list:
        print(f"Adding all Consensussequences for Locus {locus} into one file. \n")
        output_fasta_path = corrected_path / (locus + '_together_Corr.fasta')
        with open(output_fasta_path, 'w') as output_fasta:
            for file in variants_path.iterdir():
                if (file.stem.startswith(locus+"_") and file.suffix == ".fasta"):
                    #input_fasta_path = Path(consensusout_path + '/' + file)
                    with open(file) as input_fasta:
                        for line in input_fasta:
                            output_fasta.write(line)




def calc_helper(prob : float):
    if prob <= 0:
        return -math.inf
    return math.log(prob)

def get_quality_scores(mergedoutfilepath : Path, qualityscores_outputfilepath : Path, sites : dict):
    out = {}
    for header, data in parse_fastq(mergedoutfilepath).items():
        out[header] = {}
        quality = data["quality"]
        length = len(data["sequence"])

        for i, char_el in enumerate(quality):
            if (i in sites.keys()):
                out[header][i] = {}
                out[header][i]["Original"] = char_el
                out[header][i]["Unicode"] = ord(char_el) - 33
                coverted_quality = float(10**((-out[header][i]["Unicode"])/10))
                out[header][i]["BaseErrorProbability"] = coverted_quality
                mismatch_prob = coverted_quality / 3
                match_prob = 1 - coverted_quality
                out[header][i]["CalcInfo"] = (mismatch_prob, match_prob, calc_helper(mismatch_prob), calc_helper(match_prob))
    
    with open(qualityscores_outputfilepath, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4, ensure_ascii=False)

    return out



def construct_genotype_options_diploid(bases : list, sites : list):
    possible_genotypes = ["".join(genotype) for genotype in product(bases, repeat = len(sites))]
    genotype_pairs = combinations_with_replacement(possible_genotypes, 2)
    return possible_genotypes, genotype_pairs

def construct_genotype_options_diploid_new(sites : dict):
    possible_genotypes = list(product(*sites.values())) #product() gives cartesian product of all sublists
    return (possible_genotypes, combinations_with_replacement(possible_genotypes, 2)) #combinations_with_replacements gives all pairs (hence why 2 as an argument) from all given genotypes



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
            if (read[i] != genotype[i]):
                site_log_probs.append(qualities[i][2])
            else:
                site_log_probs.append(qualities[i][3])

        allele_log_prob = sum(site_log_probs)
        allele_log_probs.append(math.log(0.5) + allele_log_prob)

    return logsumexp(allele_log_probs)


# def calculate_probability_diploid_old(genotype_tuple : tuple, read : str, number_sites : int, qualities : list):
#     allele_log_probs = []
#     for genotype in genotype_tuple: #only 2
#         site_log_probs = []
#         for i in range(0, number_sites, 1):
#             base_error_probability = float(10**((-qualities[i])/10))
#             if (read[i] != genotype[i]):
#                 prob = base_error_probability/3
#             else:
#                 prob = 1-base_error_probability
#             if (prob == 0):
#                 site_log_probs.append(-math.inf)
#             else:
#                 site_log_probs.append(math.log(prob))

#         allele_log_prob = sum(site_log_probs)
#         allele_log_probs.append(math.log(0.5) + allele_log_prob)


#     return logsumexp(allele_log_probs)





def find_sites(fastafile : Path, consensusthreshold : float, base_positions_number_max : int):
    sites = {}
    consensus_bases = {}
    fasta_dict = parse_fasta(fastafile)

    #check if file has sequences with different lengths:
    seq_length_fixed = len(list(fasta_dict.values())[0])
    different_lengths = [seq for header, seq in fasta_dict.items() if (len(seq) != seq_length_fixed)]
    if (different_lengths):
        raise Exception("Different Sequence Lengths in the file " + fastafile.name + " \n")

    for i in range(0, seq_length_fixed, 1):
        calc = []
        for header, sequence in fasta_dict.items():
            calc.append(sequence[i])
        frequencies = Counter(calc)
        if (not any((count/len(fasta_dict) >= consensusthreshold for count in frequencies.values()))):
            #sites[i] = list(frequencies.keys())
            #sites[i] = frequencies
            sites[i] = {}
            sites[i]["MaxCount"] = max(frequencies.values())
            sites[i]["BasesCounts"] = list(frequencies.items())
            sites[i]["Bases"] = list(frequencies.keys())
        for base, count in frequencies.items():
            if ((count/len(fasta_dict) >= consensusthreshold)):
                consensus_bases[i] = base
                break
        # else:
        #     for base, count in frequencies.items():
        #         if ((count/len(fasta_dict) >= consensusthreshold)):
        #             consensus_bases[i] = base
        #             break

    return seq_length_fixed, consensus_bases, sites

    
def calculate_likelihoods_diploid(mergedout_path : Path, output_qualityscores_path : Path, allelesout_path : Path, samples_dict : dict, outputpath_likelihoods : Path, consensusthreshold : float, indexcomboposition : int, performance : bool, number_cores : int, base_positions_number : int): 
    #make outputfolders for likelihoods and quality scores if they dont exist
    output_qualityscores_path.mkdir(parents=True, exist_ok=True)
    outputpath_likelihoods.mkdir(parents=True, exist_ok=True)

    #determine likelihoods for each fasta in allelesout and save in corrected folder
    for fastafile in allelesout_path.iterdir():
        fastaname = fastafile.stem
        if not(fastafile.suffix == ".fasta"):
            continue
        locus = "_".join(fastaname.split('_')[0:2])
        sample = fastaname.split('_')[2]
        length = fastaname.split('_')[4]
        if (not(sample in samples_dict["reverse"])):
            print("File " + fastafile.name + " will be skipped because sample " + sample + " cannot be found in samplesheet. \n\n")
            continue
        indexcombo = samples_dict["reverse"][sample]

        print("Processing file " + fastafile.name + "\n\n")


        print(locus)
        print(sample)
        print(length)
        print(indexcombo)


        
        dict_likelihoods = {
            "locus" : locus,
            "sample" : sample,
            "length" : length,
            "NumberSequences" : 0,
            "sites" : {}, # {site : bases}
            "Genotypes" : {}
        }

        #Find all possible base sites for the fasta file where no base reaches a frequency equal to consensusthreshold
        seq_length_fixed, consensus_bases, sites = find_sites(fastafile, consensusthreshold, base_positions_number)
        dict_likelihoods["sites"] = sites
        print("File " + fastafile.name + " we find " + str(len(sites)) + " base positions for 'N's. \n\n")


        print(sites)

        #sites_bases = {position : rest["Bases"] for position, rest in sites.items()}
        max_counts_sorted_ascending = [rest["MaxCount"] for position, rest in sites.items()]
        max_counts_sorted_ascending.sort()

        #print(sites_bases)
        print(max_counts_sorted_ascending)

        #only take the first base_positions_number max_counts
        count = 0
        max_counts_sorted_ascending_limited = []
        while ((count < base_positions_number) and (count < len(max_counts_sorted_ascending))):
            max_counts_sorted_ascending_limited.append(max_counts_sorted_ascending[count])
            count += 1
        
        
        #delete position keys if their max_count is not in max_counts_sorted_ascending_limited
        sites_new = {}
        for position, rest in sites.items():
            if (rest["MaxCount"] in max_counts_sorted_ascending_limited):
                sites_new[position] = rest
        
        print("New dict bases: \n")
        print(sites_new)

        #delete position keys from consensusbases:
        consensus_bases_new = {}
        for position, base in consensus_bases.items():
            if (position not in sites_new):
                consensus_bases_new[position] = base

        sites_bases = {position : rest["Bases"] for position, rest in sites_new.items()}

        mergedoutfilepath = Path(mergedout_path / (indexcombo + "_joined.fastq"))
        qualityscores_outputfilepath = Path(output_qualityscores_path / (locus + "_" + sample + "_" + str(length) + "_qualityscores.json"))
        quality_scores_dict = get_quality_scores(mergedoutfilepath, qualityscores_outputfilepath, sites_new)
        #print(print("For file " + fastafile.name + " we find our qualities for the base positions. \n\n"))

    

        #Given the number of sites found for the fasta file and the given nucleotides, determine all possible genotypes (for diploid we have genotype pairs)
        possible_genotypes, genotype_pairs_diploid = construct_genotype_options_diploid_new(sites_bases)

        number_possible_genotype_pairs = len(possible_genotypes) * (len(possible_genotypes) + 1) // 2
        print("File " + fastafile.name + " has " + str(len(possible_genotypes)) + " possible genotypes and " + str(number_possible_genotype_pairs) + " possible diploid genotype pairs. \n\n")


        #parsing the fasta file
        fasta_dict = parse_fasta(fastafile)
        dict_likelihoods["NumberSequences"] = len(fasta_dict.keys())
        
        #Iterating over all genotype pairs calculating likelihoods for each genotype pair
        likelihood_results = []
        if (performance):
            pool = multiprocessing.Pool(processes=number_cores)
            try:
                args_list = [(genotype_pair_diploid, fasta_dict, quality_scores_dict, sites_new) for genotype_pair_diploid in genotype_pairs_diploid]
                results = pool.starmap_async(calculate_likelihood_per_genotype, args_list)
                likelihood_results = results.get()
            except KeyboardInterrupt:
                print("\nInterrupted by user. Terminating workers...")
                pool.terminate() # Kill workers immediately
                pool.join()      # Clean up resources
                return # or sys.exit(1)
            else:
                pool.close()
                pool.join()
        else:
            for genotype_pair_diploid in genotype_pairs_diploid:
                likelihood_results.append(calculate_likelihood_per_genotype(genotype_pair_diploid, fasta_dict, quality_scores_dict, sites_new))
        
        # print(likelihood_results)

        #Converting log likelihoods into likelihoods and eliminate cancellation (operation between 2 very similar numbers with digits beyond the computers highest accuracy) with helper functions
        max_log_likelihood = -math.inf
        for likelihood_result in likelihood_results:
            dict_likelihoods["Genotypes"][likelihood_result[0]] = {}
            if (likelihood_result[1] > max_log_likelihood):
                max_log_likelihood = likelihood_result[1]
        
        for likelihood_result in likelihood_results:
            dict_likelihoods["Genotypes"][likelihood_result[0]]["LogLikelihood"] = likelihood_result[1]
            dict_likelihoods["Genotypes"][likelihood_result[0]]["RelativeLogLikelihood"] = likelihood_result[1] - max_log_likelihood
            dict_likelihoods["Genotypes"][likelihood_result[0]]["RelativeLikelihood"] = math.exp(dict_likelihoods["Genotypes"][likelihood_result[0]]["RelativeLogLikelihood"])

        #Sorting genotype likelihoods in order for the highest likelihood to be at the top.
        dict_likelihoods["Genotypes"] = dict(sorted(dict_likelihoods["Genotypes"].items(), key=lambda x: x[1]["RelativeLikelihood"], reverse=True))

        out_path = outputpath_likelihoods / (locus + "_" + sample + "_" + length + "_likelihoods.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(dict_likelihoods, f, indent=4, ensure_ascii=False)

        correct_likelihood_genotype = list(dict_likelihoods["Genotypes"].keys())[0]
        correct_likelihood_value = list(dict_likelihoods["Genotypes"].values())[0]
        relativelikelihood = correct_likelihood_value["RelativeLikelihood"]

        

        fastq_path = outputpath_likelihoods / (locus + "_" + sample + "_" + length + "_likelihoods.fasta")
        with open(fastq_path, "w") as outputfile:
            header1 = locus + "_" + sample + "_Al_" + length + "_C_" + str(relativelikelihood) + "_0"
            outputfile.write('>' + header1 + "\n")

            print("NOW \n")
            print(len(sites_new))
            print(len(consensus_bases_new))
            print(len(sites))
            print(len(consensus_bases))
            print(seq_length_fixed)

            counter_seq = 0
            correct_likelihood_genotype_first = correct_likelihood_genotype.split(",")[0]
            for i in range(0, seq_length_fixed, 1):
                if (i in sites_new.keys()):
                    outputfile.write(correct_likelihood_genotype_first[counter_seq])
                    counter_seq += 1
                else:
                    outputfile.write(consensus_bases_new[i])
            outputfile.write("\n")

            header2 = locus + "_" + sample + "_Al_" + length + "_C_" + str(relativelikelihood) + "_1"
            outputfile.write('>' + header2 + "\n")
            
            counter_seq = 0
            correct_likelihood_genotype_second = correct_likelihood_genotype.split(",")[1]
            for i in range(0, seq_length_fixed, 1):
                if (i in sites_new.keys()):
                    outputfile.write(correct_likelihood_genotype_second[counter_seq])
                    counter_seq += 1
                else:
                    outputfile.write(consensus_bases_new[i])
            
            outputfile.write("\n")
            

    

def calculate_likelihood_per_genotype(genotype_pair_diploid : tuple, fasta_dict : dict, quality_scores_dict : dict, sites : dict):
    genotype_pair_diploid_str = ",".join(["".join([base for base in pair]) for pair in genotype_pair_diploid])
    #print(genotype_pair_diploid_str)
    #genotype_pair_log_likelihood_terms = []
    genotype_log_likelihood = 0.0
    for header, sequence in fasta_dict.items():
        header_merged = "@M" + header #Merged files have header beginning with @M, AllelesOut have header but with > instead of @M
        qualities = [rest["CalcInfo"] for site, rest in quality_scores_dict[header_merged].items()]
        observed_bases = "".join([sequence[site] for site in sites.keys()])
        #genotype_pair_log_likelihood_terms.append(calculate_probability_diploid(genotype_pair_diploid, observed_bases, len(sites.keys()), qualities))
        genotype_log_likelihood += calculate_probability_diploid(genotype_pair_diploid, observed_bases, len(sites.keys()), qualities)

    return (genotype_pair_diploid_str, genotype_log_likelihood)

if __name__ == "__main__":
    main()