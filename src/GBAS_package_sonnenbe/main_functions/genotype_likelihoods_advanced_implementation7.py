from pathlib import Path

import json, math, multiprocessing

import numpy as np

from GBAS_package_sonnenbe.helper_functions.parse_fastq import parse_fastq
from GBAS_package_sonnenbe.helper_functions.parse_fasta import parse_fasta
from GBAS_package_sonnenbe.helper_functions.parse_samplefile import get_samples

from itertools import product, combinations_with_replacement

from collections import Counter




def main():

    print("Extracting Quality Scores.\n")

    inputs_path_str = r"C:\Users\Sebastian\Documents\Micromeria_test\inputs"
    inputs_path = Path(inputs_path_str)

    mergedout_path_str = r"C:\Users\Sebastian\Documents\Micromeria_test\outputs\output_2samples_2primers\MergedOut"
    output_path_str = r"C:\Users\Sebastian\Documents\Micromeria_test\output_quality_scores"
    allelesout_path_str = r"C:\Users\Sebastian\Documents\Micromeria_test\outputs\output_2samples_2primers\AllelesOut" #AllelesOut_test #AllelesOut_test2
    
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
    outputpath_multiple = Path(r"C:\Users\Sebastian\Documents\Micromeria_test\Corrected")

    calculate_likelihoods(mergedout_path, output_qualityscores_path, allelesout_path, samplelist_path, outputpath_multiple, 0.7, 1, True, 15)


    return 0


quality_scores_mappings = {

}

#Quality scores mappings (symbol to the Quality Score Q), Phred 33 Encoding
# quality_scores = {
#     "!": 0, "\"": 1, "#": 2, "$": 3, "%": 4, "&": 5,
#     "'": 6, "(": 7, ")": 8, "*": 9, "+": 10, ",": 11,
#     "-": 12, ".": 13, "/": 14, "0": 15, "1": 16, "2": 17,
#     "3": 18, "4": 19, "5": 20, "6": 21, "7": 22, "8": 23,
#     "9": 24, ":": 25, ";": 26, "<": 27, "=": 28, ">": 29,
#     "?": 30, "@": 31, "A": 32, "B": 33, "C": 34, "D": 35,
#     "E": 36, "F": 37, "G": 38, "H": 39, "I": 40
# }


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
            #out["Indexcombos"][indexcombo]["Sequences"][header]["Length"] = length
            list_qualities_converted = []
            for char in quality:
                list_qualities_converted.append(ord(char) - 33) #ord() gets the unicode for the given characters, if its an ASCII character than it givs the ASCII number (0-128)
            out["Indexcombos"][indexcombo]["Sequences"][header] = (length, list_qualities_converted)
    
    output_path.mkdir(parents=True, exist_ok=True)

    out_path = output_path / "quality_scores.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4, ensure_ascii=False)


# def get_quality_scores_new(mergedout_path : Path, output_qualityscores_path : Path, indexcomboposition : int):
#     out = {"Indexcombos" : {}}

#     for fastqfile in mergedout_path.iterdir():
#         if not(fastqfile.suffix == ".fastq"):
#             continue

#         indexcombo = fastqfile.name.split("_")[indexcomboposition-1]
#         out["Indexcombos"][indexcombo]  = {}
#         out["Indexcombos"][indexcombo]["Sequences"]  = {}
#         print("Getting Quality scores for sample " + indexcombo + "...\n")
#         for header, data in parse_fastq(fastqfile).items():
#             quality = data["quality"]
#             length = len(data["sequence"])

#             out["Indexcombos"][indexcombo]["Sequences"][header] = {}
#             #out["Indexcombos"][indexcombo]["Sequences"][header]["Length"] = length
#             list_qualities_converted = []
#             for char in quality:
#                 list_qualities_converted.append(ord(char) - 33) #ord() gets the unicode for the given characters, if its an ASCII character than it givs the ASCII number (0-128)
#             out["Indexcombos"][indexcombo]["Sequences"][header] = (length, list_qualities_converted)
    
#     output_path.mkdir(parents=True, exist_ok=True)

#     out_path = output_path / "quality_scores.json"
#     with open(out_path, "w", encoding="utf-8") as f:
#         json.dump(out, f, indent=4, ensure_ascii=False)


def calc_helper(prob : float):
    if prob <= 0:
        return -math.inf
    return math.log(prob)

def get_quality_scores_new(mergedoutfilepath : Path, qualityscores_outputfilepath : Path, sites : dict):
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


def calculate_probability_diploid_old(genotype_tuple : tuple, read : str, number_sites : int, qualities : list):
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





def find_sites(fastafile : Path, consensusthreshold : float):
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
            sites[i] = list(frequencies.keys())
        else:
            for base, count in frequencies.items():
                if ((count/len(fasta_dict) >= consensusthreshold)):
                    consensus_bases[i] = base
                    break

    return seq_length_fixed, consensus_bases, sites
    
def calculate_likelihoods(mergedout_path : Path, output_qualityscores_path : Path, allelesout_path : Path, samplelist_path : Path, outputpath_likelihoods : Path, consensusthreshold : float, indexcomboposition : int, performance : bool, number_cores : int):
    # quality_scores = {}
    # with open(json_input_dict, "r") as f:
    #     quality_scores = json.load(f)
    
    samples_dict, number_lines = get_samples(str(samplelist_path))
    
    output_qualityscores_path.mkdir(parents=True, exist_ok=True)
    outputpath_likelihoods.mkdir(parents=True, exist_ok=True)

    for fastafile in allelesout_path.iterdir():
        if not(fastafile.suffix == ".fasta"):
            continue
        locus = "_".join(fastafile.name.split('_')[0:2])
        sample = fastafile.name.split('_')[2]
        length = fastafile.name.split('_')[4]
        indexcombo = samples_dict["reverse"][sample]
        print(locus)
        print(sample)

        print("Processing file " + fastafile.name + "\n\n")

        
        dict_likelihoods = {
            "locus" : locus,
            "sample" : sample,
            "length" : length,
            "sites" : {}, # {site : bases}
            "Genotypes" : {}
        }

        # if (not(locus in dict_likelihoods)):
        #     dict_likelihoods[locus] = {}

        # if (not(sample in dict_likelihoods[locus])):
        #     dict_likelihoods[locus][sample] = {}

        # dict_likelihoods[locus][sample]["Genotypes"] = {}

        #Find all possible base sites for the fasta file where no base reaches a frequency equal to consensusthreshold
        seq_length_fixed, consensus_bases, sites = find_sites(fastafile, consensusthreshold)
        dict_likelihoods["sites"] = sites
        print(print("File " + fastafile.name + " we find " + str(len(sites)) + " base positions for 'N's. \n\n"))
        print(sites)

        mergedoutfilepath = Path(mergedout_path / (indexcombo + "_joined.fastq"))
        qualityscores_outputfilepath = Path(output_qualityscores_path / (locus + "_" + sample + "_" + str(length) + "_qualityscores.json"))
        quality_scores_dict = get_quality_scores_new(mergedoutfilepath, qualityscores_outputfilepath, sites)
        print(print("For file " + fastafile.name + " we find our qualities for the base positions. \n\n"))
        #print(quality_scores_dict)

    

        #Given the number of sites found for the fasta file and the given nucleotides, determine all possible genotypes (for diploid we have genotype pairs)
        possible_genotypes, genotype_pairs_diploid = construct_genotype_options_diploid_new(sites)

        number_possible_genotype_pairs = len(possible_genotypes) * (len(possible_genotypes) + 1) // 2
        print("File " + fastafile.name + " has " + str(len(possible_genotypes)) + " possible genotypes and " + str(number_possible_genotype_pairs) + " possible diploid genotype pairs. \n\n")


        #parsing the fasta file
        fasta_dict = parse_fasta(fastafile)

        max_log_likelihood = -math.inf

        likelihood_results = []
        if (performance):
            with multiprocessing.Pool(processes = number_cores) as pool:
                args_list = [(genotype_pair_diploid, fasta_dict, quality_scores_dict, sites) for genotype_pair_diploid in genotype_pairs_diploid]
                results = pool.starmap_async(calculate_likelihood_per_genotype, args_list)
                likelihood_results = results.get()
        else:
            for genotype_pair_diploid in genotype_pairs_diploid:
                likelihood_results.append(calculate_likelihood_per_genotype(genotype_pair_diploid, fasta_dict, quality_scores_dict, sites))
        
        # print(likelihood_results)

        max_log_likelihood = -math.inf
        for likelihood_result in likelihood_results:
            dict_likelihoods["Genotypes"][likelihood_result[0]] = {}
            if (likelihood_result[1] > max_log_likelihood):
                max_log_likelihood = likelihood_result[1]
        
        for likelihood_result in likelihood_results:
            dict_likelihoods["Genotypes"][likelihood_result[0]]["LogLikelihood"] = likelihood_result[1]
            dict_likelihoods["Genotypes"][likelihood_result[0]]["RelativeLogLikelihood"] = likelihood_result[1] - max_log_likelihood
            dict_likelihoods["Genotypes"][likelihood_result[0]]["RelativeLikelihood"] = math.exp(dict_likelihoods["Genotypes"][likelihood_result[0]]["RelativeLogLikelihood"])


        #dict_likelihoods["Genotypes"] = [for key, rest in dict_likelihoods["Genotypes"].items()]
        dict_likelihoods["Genotypes"] = dict(sorted(dict_likelihoods["Genotypes"].items(), key=lambda x: x[1]["RelativeLikelihood"], reverse=True))

        out_path = outputpath_likelihoods / (locus + "_" + sample + "_" + length + "_likelihoods.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(dict_likelihoods, f, indent=4, ensure_ascii=False)

        correct_likelihood_genotype = list(dict_likelihoods["Genotypes"].keys())[0]
        correct_likelihood_value = list(dict_likelihoods["Genotypes"].values())[0]

        print(dict_likelihoods["Genotypes"])

        fastq_path = outputpath_likelihoods / (locus + "_" + sample + "_" + length + "_corrected.json")
        with open(fastq_path, "w") as outputfile:
            header1 = locus + "_" + sample + "_Al_" + length + "_C_" + str(correct_likelihood_value) + "_0"
            outputfile.write('>' + header1[1:] + "\n")

            counter_seq = 0
            correct_likelihood_genotype_first = correct_likelihood_genotype.split(",")[0]
            for i in range(0, seq_length_fixed, 1):
                if (i in sites.keys()):
                    outputfile.write(correct_likelihood_genotype_first[counter_seq])
                    counter += 1
                else:
                    outputfile.write(consensus_bases[i])
            outputfile.write("\n")

            header2 = locus + "_" + sample + "_Al_" + length + "_C_" + str(correct_likelihood_value) + "_1"
            outputfile.write('>' + header2[1:] + "\n")
            
            counter_seq = 0
            correct_likelihood_genotype_second = correct_likelihood_genotype.split(",")[1]
            for i in range(0, seq_length_fixed, 1):
                if (i in sites.keys()):
                    outputfile.write(correct_likelihood_genotype_second[counter_seq])
                    counter += 1
                else:
                    outputfile.write(consensus_bases[i])
            
            # outputfile.write('>' + header[1:] + '\n' + sequence + '\n')




        # counter = 0
        # for genotype_pair_diploid in genotype_pairs_diploid:
        #     #print(genotype_pair_diploid)
        #     genotype_pair_diploid_str = ",".join(["".join([base for base in pair]) for pair in genotype_pair_diploid])
        #     print(genotype_pair_diploid_str)
        #     dict_likelihoods["Genotypes"][genotype_pair_diploid_str] = {}
        #     #genotype_pair_log_likelihood_terms = []
        #     genotype_log_likelihood = 0.0
        #     for header, sequence in fasta_dict.items():
        #         header_merged = "@M" + header #Merged files have header beginning with @M, AllelesOut have header but with > instead of @M
        #         qualities = [rest["CalcInfo"] for site, rest in quality_scores_dict[header_merged].items()]
        #         #qualities = [quality_scores_dict[header_merged][1][site] for site in sites.keys()]
        #         observed_bases = "".join([sequence[site] for site in sites.keys()])
        #         #genotype_pair_log_likelihood_terms.append(calculate_probability_diploid(genotype_pair_diploid, observed_bases, len(sites.keys()), qualities))
        #         genotype_log_likelihood += calculate_probability_diploid(genotype_pair_diploid, observed_bases, len(sites.keys()), qualities)
        #     print(counter)
        #     counter += 1

        #     #genotype_log_likelihood = sum(genotype_pair_log_likelihood_terms)

        #     dict_likelihoods["Genotypes"][genotype_pair_diploid_str]["LogLikelihood"] = genotype_log_likelihood

        #     log_likelihoods = [data["LogLikelihood"] for data in dict_likelihoods["Genotypes"].values()]

        #     #max_log_likelihood = max(log_likelihoods)

        #     if (genotype_log_likelihood > max_log_likelihood):
        #         max_log_likelihood = genotype_log_likelihood

        # for genotype_name, data in dict_likelihoods["Genotypes"].items():
        #     rel_log_likelihood = data["LogLikelihood"] - max_log_likelihood
        #     data["RelativeLogLikelihood"] = rel_log_likelihood
        #     data["RelativeLikelihood"] = math.exp(rel_log_likelihood)


        # out_path = output_path / (locus + "_" + sample + "_" + length + "_likelihoods.json")
        # with open(out_path, "w", encoding="utf-8") as f:
        #     json.dump(dict_likelihoods, f, indent=4, ensure_ascii=False)
    

def calculate_likelihood_per_genotype(genotype_pair_diploid : tuple, fasta_dict : dict, quality_scores_dict : dict, sites : dict):
    genotype_pair_diploid_str = ",".join(["".join([base for base in pair]) for pair in genotype_pair_diploid])
    print(genotype_pair_diploid_str)
    #dict_likelihoods["Genotypes"][genotype_pair_diploid_str] = {}
    genotype_pair_log_likelihood_terms = []
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