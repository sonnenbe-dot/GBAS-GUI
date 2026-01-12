from pathlib import Path
import customtkinter as ctk
import json, os, sys, subprocess

from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import is_valid
from GBAS_package_sonnenbe.helper_functions.parse_fasta import parse_fasta
from GBAS_package_sonnenbe.helper_functions.parse_samplefile import get_samples
from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import is_valid
from GBAS_package_sonnenbe.helper_functions.convert_excel_to_json import convert_excel_to_json_dict, write_dict_to_json

from GBAS_package_sonnenbe.main_functions.extract_lengths import extract_locinames_from_matrix, extract_samplenames_from_matrix

def main():

    return 0



def run_Allele_Call_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict):
    allelesoutpath = Path(paramsdict["Outputfolder"] + "/AllelesOut")
    correctedpath = Path(paramsdict["Outputfolder"] + "/Corrected")
    allelecallpath = Path(paramsdict["Outputfolder"] + "/AlleleCall")
    length_matrix_json_path = Path(paramsdict["Outputfolder"] + '/MarkerPlots/markermatrix.json')
    loci_list = extract_locinames_from_matrix(length_matrix_json_path)
    sample_list = extract_samplenames_from_matrix(length_matrix_json_path)
    samples_dict, number_lines = get_samples(paramsdict["Samplefile"])
    allelist_path = Path(paramsdict["Allelelist"])
    metadata_path = Path(paramsdict["Metadata"])
    textbox_pipeline.insert('end-1c', "\nStarting Allele Call! \n")
    run_Allele_Call(correctedpath, allelecallpath, loci_list, sample_list, samples_dict, allelist_path, metadata_path, textbox_pipeline)
    textbox_pipeline.insert('end-1c', "\nFinished Allele Call! \n")



def run_Allele_Call_CLI(paramsdict : dict):
    allelesoutpath = Path(paramsdict["Outputfolder"] + "/AllelesOut")
    correctedpath = Path(paramsdict["Outputfolder"] + "/Corrected")
    allelecallpath = Path(paramsdict["Outputfolder"] + "/AlleleCall")
    length_matrix_json_path = Path(paramsdict["Outputfolder"] + '/MarkerPlots/markermatrix.json')
    loci_list = extract_locinames_from_matrix(length_matrix_json_path)
    sample_list = extract_samplenames_from_matrix(length_matrix_json_path)
    samples_dict, number_lines = get_samples(paramsdict["Samplefile"])
    allelist_path = Path(paramsdict["Allelelist"])
    metadata_path = Path(paramsdict["Metadata"])
    print("\nStarting Allele Call! \n")
    run_Allele_Call_CLI_more(correctedpath, allelecallpath, loci_list, sample_list, samples_dict, allelist_path, metadata_path)
    print("\nFinished Allele Call! \n")



def run_Allele_Call_CLI_more(correctedpath : Path, allelecallpath : Path, loci_list : list, sample_list : list, samples_dict : dict, allelist_path : Path, metadata_path : Path):
    allelesdict = {}
    if (is_valid(str(allelist_path))):
        print("\nValid Allelelist, Listbased Call! \n")
        print("\nStarting Listbased AlleleCall!\n")
        if (allelist_path.suffix == ".txt"):
            allelesdict = parse_allelelist_txt(allelist_path)
        elif (allelist_path.suffix == ".json"):
            allelesdict = parse_allelelist_json(allelist_path)
        else:
            print("\nNo correct fileformat for allelelist!\n")
        
        number_loci = len(allelesdict.keys())
        allelesequences = [sequence for locus, data in allelesdict.items() for sequence in data[1]]
        number_allelesequences = len(allelesequences)
        print("Allelelist contains " + str(number_loci) + " loci and in total " + str(number_allelesequences) + " alleles. \n")
        

    else:
        print("\nNo Allelelist Given, Denovo Call!\n")

    alleles_dict_complete, number_new_alleles, number_new_loci, number_old_loci_added = Complete_AlleleList_All(correctedpath, allelesdict)

    print(str(number_new_alleles) + " new alleles found!")
    print(str(number_new_loci) + " new loci added!")

    CallAlleles(alleles_dict_complete, correctedpath, allelecallpath, sample_list, loci_list, samples_dict, metadata_path)



def run_Allele_Call(correctedpath : Path, allelecallpath : Path, loci_list : list, sample_list : list, samples_dict : dict, allelist_path : Path, metadata_path : Path, textbox_pipeline : ctk.CTkTextbox):
    allelesdict = {}
    if (is_valid(str(allelist_path))):
        textbox_pipeline.insert('end-1c', "\nValid Allelelist, Listbased Call! \n")
        print("\nStarting Listbased AlleleCall!\n")
        if (allelist_path.suffix == ".txt"):
            allelesdict = parse_allelelist_txt(allelist_path)
        elif (allelist_path.suffix == ".json"):
            allelesdict = parse_allelelist_json(allelist_path)
        else:
            print("\nNo correct fileformat for allelelist!\n")
        
        number_loci = len(allelesdict.keys())
        allelesequences = [sequence for locus, data in allelesdict.items() for sequence in data[1]]
        number_allelesequences = len(allelesequences)
        print("Allelelist contains " + str(number_loci) + " loci and in total " + str(number_allelesequences) + " alleles. \n")
        

    else:
        print("\nNo Allelelist Given, Denovo Call!\n")

    alleles_dict_complete, number_new_alleles, number_new_loci, number_old_loci_added = Complete_AlleleList_All(correctedpath, allelesdict)

    print(str(number_new_alleles) + " new alleles found!")
    print(str(number_new_loci) + " new loci added!")

    CallAlleles(alleles_dict_complete, correctedpath, allelecallpath, sample_list, loci_list, samples_dict, metadata_path)


def CallAlleles(complete_alleles_dict : dict, correctedpath : Path, allelecallpath : Path, sample_list : list, loci_list : list, sampledict : dict, metadata_path : Path):
    metadata_dict = {}
    if (is_valid(str(metadata_path))):
        metadata_dict = convert_excel_to_json_dict(metadata_path, "sample")
    #print(metadata_dict)

    allele_dict_json = {} #allele list in json format
    allele_matrix_json = {} #allele matrix in json format
    loci_for_matrix = []
    locus_already_written = []
    markers_more_than2 = []

    out_dict = {'samples' : '\t'}
    seq_list_unique_entire = []
    for sample in sample_list:
        new_sample = sampledict["linksreverse"][sample]
        out_dict[new_sample] = ''
        #allele_matrix_json[new_sample] = {} #for json matrix
    
    file_list = []
    for file in correctedpath.iterdir():
        file_list.append(file.name)
    sorted_filenames = sorted(file_list, key=lambda file : loci_list.index(file.split('_')[0] + '_' + file.split('_')[1]))

    #print(sorted_filenames)

    output_allelelist_path = allelecallpath / 'allelle_list.txt'
    output_allelelist_path_fasta = allelecallpath / 'allelle_list.fasta'
    with open(output_allelelist_path, 'w') as allele_list:
        with open(output_allelelist_path_fasta, 'w') as allele_list_fasta:
            for file in sorted_filenames:
                #Iterate through all files from the corrected folder
                locus = file.split('_')[0] + '_' + file.split('_')[1] # get locus
                loci_for_matrix.append(locus)
                locus_already_written.append(locus) ####
                out_dict['samples'] += (locus + '\t')*2 #saves the current locus in the dictionary
                print("\nGet Alleles Dict for Locus " + locus +  "\n")
                alleles_dict = complete_alleles_dict[locus]

                if (locus not in allele_dict_json):
                    allele_dict_json[locus] = {}
                    
                alleles_dict = dict(sorted(alleles_dict.items(), key=lambda item: int(item[0])))

                file_path = correctedpath / file
                parsed_fasta = parse_fasta(file_path) #Get all sequences from one fasta file of the corrected folder
                names_alleles, list_numbers = Define_genotypes(alleles_dict, parsed_fasta)

                #names_alleles is a dict with sample names as keys and and a list of values all corresponding alleles (saved through the indices as a list)
                allele_list.write(locus + '\n')
                for allele, allele_seq in alleles_dict.items(): #alleles_dict in the form index : sequence, one index can have 2 sequences
                    for seq in allele_seq:
                        seq_list_unique_entire.append(seq)
                        allele_list.write(allele + ':\t' + seq + '\n')
                        allele_list_fasta.write('>' + locus + ':' + allele + '\n')
                        allele_list_fasta.write(seq + '\n')
                            
                        allele_dict_json[locus][seq] = {}
                        allele_dict_json[locus][seq]["ID"] = str(allele)
                        allele_dict_json[locus][seq]["Length"] = len(seq)
                        allele_dict_json[locus][seq]["Read"] = seq
                            
                allele_list.write('\\\n')

                for sample in sample_list:
                    new_sample = sampledict["linksreverse"][sample]
                    if (new_sample not in allele_matrix_json):
                        allele_matrix_json[new_sample] = {}
                        allele_matrix_json[new_sample]["Metadata"] = {}
                        allele_matrix_json[new_sample]["Loci"] = {}

                    if (new_sample in metadata_dict):
                        #allele_matrix_json[new_sample]["Metadata"] = {}
                        for header, value in metadata_dict[new_sample].items():
                            allele_matrix_json[new_sample]["Metadata"][header] = value
       
                    if (locus not in allele_matrix_json[new_sample]["Loci"]):
                        allele_matrix_json[new_sample]["Loci"][locus] = {}
                        allele_matrix_json[new_sample]["Loci"][locus]["Alleles"] = {}
                    
                    if sample in names_alleles:
                        alleles = names_alleles[sample] #get all allele indices for this sample name
                        alleles.sort() #sorting according to keys which are the sample names
                        # if two alleles saves it as heterozygote
                        if len(alleles) == 2:
                            genotype = '\t'.join(alleles)
                        # if more report the genotype as ambiguous and mark genotype for manual control. It does not aply anymore
                        elif len(alleles) > 2:
                            markers_more_than2.append(locus)
                            print('locus ' + locus + ' for sample ' +  sample + '\thas ' + str(len(alleles)) + ' alleles: ' + str(alleles))
                            genotype = 'MC\tMC'
                        # if one saves as homozygote
                        else:
                            genotype = '\t'.join(alleles*2)
                            #print(genotype)

                        for allele in alleles:
                            if allele in complete_alleles_dict[locus].keys(): 
                                #allele_matrix_json[new_sample][locus][allele] = complete_alleles_dict[locus][allele][0]
                                seq = complete_alleles_dict[locus][allele][0]
                                allele_matrix_json[new_sample]["Loci"][locus]["Alleles"][seq] = {}
                                allele_matrix_json[new_sample]["Loci"][locus]["Alleles"][seq]["ID"] = str(allele)
                                allele_matrix_json[new_sample]["Loci"][locus]["Alleles"][seq]["Length"] = len(seq)
                                allele_matrix_json[new_sample]["Loci"][locus]["Alleles"][seq]["Read"] = seq
                    
                    else:
                        genotype = '0\t0'
                    #new_sample = sampledict[sample]
                    out_dict[new_sample] += '\t' + genotype #it saves the genotypes in the dictionary
                
            print("\nFinished getting gynotypes for all samples!\n")
            for locus in complete_alleles_dict:
                if locus not in locus_already_written:
                    alleles_dict = complete_alleles_dict[locus]
                    alleles_dict = dict(sorted(alleles_dict.items(), key=lambda item: int(item[0])))
                    allele_list.write(locus + '\n')
                        
                    allele_dict_json[locus] = {}
                        
                    for allele, allele_seq in alleles_dict.items(): #alleles_dict in the form index : sequence, one index can have 2 sequences
                        for seq in allele_seq:
                            seq_list_unique_entire.append(seq)
                            allele_list.write(allele + ':\t' + seq + '\n')
                            allele_list_fasta.write('>' + locus + ':' + allele + '\n')
                            allele_list_fasta.write(seq + '\n')
                                
                            allele_dict_json[locus][seq] = {}
                            allele_dict_json[locus][seq]["ID"] = str(allele)
                            allele_dict_json[locus][seq]["Length"] = len(seq)
                            allele_dict_json[locus][seq]["Read"] = seq
                                
                    allele_list.write('\\\n')
    
    matrix_path = allelecallpath / 'matrix.txt'
    with open(matrix_path, 'w') as matrix_out:
        matrix_out.write('samples' + out_dict['samples'] + '\n')
        #saves the matrix the genotypes
        for sample in sample_list:
            new_sample = sampledict["linksreverse"][sample]
            matrix_out.write(new_sample + out_dict[new_sample] + '\n')
        
        
    allelelist_json_path = allelecallpath / 'allelle_list.json'
    with open(allelelist_json_path, 'w') as json_output:
        json.dump(allele_dict_json, json_output, indent = 4)
    
    complete_json_path = allelecallpath / 'matrix.json'
    with open(complete_json_path, 'w') as json_output: #, encoding='utf-8'
        json.dump(allele_matrix_json, json_output, indent = 4)
    
    print("\nFinished Allele Call!\n")
    if matrix_path.exists():
        if sys.platform.startswith("win"):
            os.startfile(matrix_path)
        elif (sys.platform == "linux"):
            subprocess.run(["xdg-open", str(matrix_path)])


def Define_genotypes(alleles_dict_per_locus : dict, fasta_parsed : dict):
    result = {}
    list_numbers = []
    for head, seq in fasta_parsed.items():
        number = 0
        name = head.split('_')[2] # get sample name
        seqDeGap = seq.replace('-', '') # degap sequences in case of aligned files
        for allele, allele_seq in alleles_dict_per_locus.items():
            # compare with sequences
            if (seqDeGap in allele_seq):
                number += 1
                # save information per sample
                alleles_to_dict = result.get(name, []) + [allele]
                result[name] = alleles_to_dict
                #break
        list_numbers.append(number)
        #print(number)   
    return result, list_numbers

def Complete_AlleleList_All(correctedpath : Path, allelesdict : dict):
    complete_allelelist_dict = {}
    number_new_alleles = 0
    number_new_loci = 0
    number_old_loci_added = 0
    for file in correctedpath.iterdir():
        locus = file.name.split('_')[0] + '_' + file.name.split('_')[1]
        parsed_fasta = parse_fasta(file)
        #CaseA: A locus of current run is not found in the old allelelist, will be added along with all sequences from the corresponding corrected file!
        if (locus not in allelesdict):
            print('locus ' + locus + ' not present in allele list and will be added to new allelelist!\n')
            alleles_dict, count_new_alleles = get_allele_dict(parsed_fasta)
            complete_allelelist_dict[locus] = alleles_dict
            number_new_loci += 1
            number_new_alleles += count_new_alleles
        else:
            #CaseB: Locus from current run appears in old allelelist. New alleledict will be built, taking the allelesequences from the old and adding all new sequences while giving them a new index
            alleles_tuple = allelesdict[locus]
            old_allelesdict = alleles_tuple[0]
            old_alleleslist = alleles_tuple[1]
            new_alleles_dict, new_alleles_list, count_new_alleles = get_new_allele_dict_per_locus(old_allelesdict, old_alleleslist, parsed_fasta)
            complete_allelelist_dict[locus] = new_alleles_dict
            number_new_alleles += count_new_alleles
    print("Added " + str(number_new_loci) + " and " + str(number_new_alleles) + " new allele sequences! \n")
    old_locus_added_list = []
    for locus in allelesdict:
        if locus not in complete_allelelist_dict:
            number_old_loci_added += 1
            old_locus_added_list.append(locus)
            complete_allelelist_dict[locus] = allelesdict[locus][0]
    print("Added " + str(number_old_loci_added) + " loci from old allelelist to new allelelist! \n")
        
    allelesequences = [sequence for locus, data in complete_allelelist_dict.items() for index, sequence in data.items()]
    print("New Alleleist contains {} loci and {} Allelesequences".format(len(complete_allelelist_dict.keys()), len(allelesequences)))

    return complete_allelelist_dict, number_new_alleles, number_new_loci, number_old_loci_added


def get_new_allele_dict_per_locus(old_allelesdict : dict, old_alleleslist : list, parsed_fasta : dict) ->dict:
    new_alleles_dict = old_allelesdict
    new_allelelist = old_alleleslist
    allele_Number = len(new_alleles_dict)
    count_new_alleles = 0
    for header, sequence in parsed_fasta.items():
        sequence = sequence.replace('-', '')
        if not(sequence in new_allelelist):
            print("Finding new sequence")
            count_new_alleles += 1
            allele_Number += 1 # make new allele name
            new_alleles_dict[str(allele_Number)] = [sequence] # add new allele and corresponding sequence to dictionary
            new_allelelist.append(sequence) # add new sequence to sequence list
    return new_alleles_dict, new_allelelist, count_new_alleles

def get_allele_dict(fastadict : dict) -> dict:
    alleles_dict = {}
    seq_list = [seq for name, seq in fastadict.items()] #get all sequences from that parsed fasta, name is just the header
    seq_list = list(set(seq_list))
    seq_list.sort()
    alleles_dict = {str(allele): [seq] for (allele, seq) in enumerate(seq_list, 1)} #allele is here a number, starts on 1 and gives each sequence a number starting from 1
    return alleles_dict, len(alleles_dict.keys()) #


def parse_allelelist_json(allelelistpath : Path) -> dict:
    pass

def parse_allelelist_txt(allelelistpath : Path) ->dict:
    results_dict = {}
    allele_dict = {}
    allele_sequences_list = []

    with open(allelelistpath, "r") as allelelist:
        locus = None
        for line in allelelist:
            line = line.rstrip('\r\n')
            if (len(line.split('_')) == 2):
                locus = '_'.join(line.split('_')[:2])
                allele_dict = {}
                allele_sequences_list = []
            elif (line == '\\' or line == '' or line == "/"):
                results_dict[locus] = (allele_dict, allele_sequences_list)
            else:
                linelist = line.split('\t')
                alleleindex = linelist[0].rstrip(':').rstrip('\r\n').rstrip()
                allelesequence = linelist[1].strip().replace('-', '')
                if (alleleindex != "MC"):
                    if (alleleindex not in allele_dict):
                        allele_dict[alleleindex] = []
                    allele_dict[alleleindex].append(allelesequence)
                    allele_sequences_list.append(allelesequence)

    return results_dict



if __name__ == "__main__":
    main()