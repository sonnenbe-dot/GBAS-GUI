import os, multiprocessing, json
from pathlib import Path
import customtkinter as ctk

from GBAS_package_sonnenbe.helper_functions.parse_fasta import parse_fasta

def main():
    
    return 0


def runLengthstatistics_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict, primersdict : dict, performance : bool, number_cores : int):
    separatout_path = Path(paramsdict["Outputfolder"] + '/SeparatOut')
    markerstatistics_path = Path(paramsdict["Outputfolder"] + '/MarkerStatistics')
    textbox_pipeline.insert('end-1c', "\nStarting Markerstatistics! \n")
    runLengthstatistics(separatout_path, markerstatistics_path, primersdict, performance, number_cores)
    dict_path = Path(markerstatistics_path / "markerstatistics.json")
    runLengthstatistics_duplicates(dict_path, markerstatistics_path)
    textbox_pipeline.insert('end-1c', "\nFinished Markerstatistics! \n")
    

def runLengthstatistics_CLI(paramsdict : dict, primersdict : dict, performance : bool, number_cores : int):
    separatout_path = Path(paramsdict["Outputfolder"] + '/SeparatOut')
    markerstatistics_path = Path(paramsdict["Outputfolder"] + '/MarkerStatistics')
    print("\n\nStarting Markerstatistics! \n\n")
    runLengthstatistics(separatout_path, markerstatistics_path, primersdict, performance, number_cores)
    dict_path = Path(markerstatistics_path / "markerstatistics.json")
    runLengthstatistics_duplicates(dict_path, markerstatistics_path)
    print("\n\nFinished Markerstatistics! \n\n")

def runLengthstatistics_duplicates(dict_path_input : Path, outputpath : Path):
    markerstatistics_dict = {}
    dict_path = Path(outputpath / "markerstatistics_dupl.json")
    with open(dict_path_input) as json_file:
        markerstatistics_dict = json.load(json_file)
    
    dict_statistics_duplicates = {}
    for locus, rest in  markerstatistics_dict.items():
        if (not("LengthBoundaries" in rest)):
            continue
        locus_original = locus.replace("dupl", "")
        dict_statistics_duplicates[locus_original] = {}
        dict_statistics_duplicates[locus_original]["Samples"] = rest["Samples"]
        dict_statistics_duplicates[locus] = {}
        dict_statistics_duplicates[locus]["LengthBoundaries"] = rest["LengthBoundaries"]
        dict_statistics_duplicates[locus]["Samples"] = rest["Samples"]
    
    with open(dict_path, "w", encoding="utf-8") as f:
        json.dump(dict_statistics_duplicates, f, indent=4, ensure_ascii=False)



def runLengthstatistics(inputpath : Path, outputpath : Path, primersdict : dict, performance : bool, number_cores : int):
    dict_path = Path(outputpath / "markerstatistics.json")
    #dict_path = Path(outputpath / "markerstatistics_duplicates.json")
    dict_statistics = {}
    dict_statistics_duplicates = {}
    for filepath in inputpath.iterdir():
        if (not(filepath.is_file()) and not(filepath.suffix == ".fasta")):
            continue
        filename_parts = filepath.stem.split("_")
        samplename = filename_parts[0]
        primername = "_".join(filename_parts[1:])
        if (primername not in dict_statistics):
            dict_statistics[primername] = {}
            primername_original = primername
            if (primername in primersdict["primersboundaries"]):
                dict_statistics[primername]["LengthBoundaries"] = primersdict["primersboundaries"][primername] 
                # primername_original = primername.replace("dupl", "")
                # dict_statistics_duplicates[primername_original] = {}
                # dict_statistics_duplicates[primername] = {}
                # dict_statistics_duplicates[primername]["LengthBoundaries"] = primersdict["primersboundaries"][primername] 
            
            dict_statistics[primername]["Samples"] = {}
            # dict_statistics_duplicates[primername_original]["Samples"] = {}
            # dict_statistics_duplicates[primername]["Samples"] = {}
        if (samplename not in dict_statistics[primername]["Samples"]):
            dict_statistics[primername]["Samples"][samplename] = {}
            # dict_statistics_duplicates[primername]["Samples"][samplename] = {}
        dict_statistics[primername]["Samples"][samplename]["Lengths-Counts"] = {}
        for header, sequence in parse_fasta(filepath).items():
            if (len(sequence) not in dict_statistics[primername]["Samples"][samplename]["Lengths-Counts"]):
                dict_statistics[primername]["Samples"][samplename]["Lengths-Counts"][len(sequence)] = 0
            dict_statistics[primername]["Samples"][samplename]["Lengths-Counts"][len(sequence)] += 1
    
        dict_statistics[primername]["Samples"][samplename]["Lengths-Counts"] = dict(sorted(dict_statistics[primername]["Samples"][samplename]["Lengths-Counts"].items(), key=lambda x:x[1], reverse=True))
    
    with open(dict_path, "w", encoding="utf-8") as f:
        json.dump(dict_statistics, f, indent=4, ensure_ascii=False)

# def get_lengthstatistics2(outputfolderpath : str, inputpath : str, markerstatisticsfolderpath : str, primersdict : dict):
#     if (len(primersdict["primersboundaries"].keys()) > 0):
#         duplicate_folder = os.path.normpath(outputfolderpath + '/MarkerStatisticsBoundaries')
#         try:
#             print("Boundaries are set in primerfile, saved in its own folder! \n")
#             os.mkdir(duplicate_folder)
#         except OSError:
#             print ("Creation of the directory %s failed because it's already there." % duplicate_folder) # if it fail it produces this error message
#         else:
#             print ("Successfully created the directory %s " % duplicate_folder)
#     for file in os.listdir(os.path.normpath(separatoutfolderpath)):
#         print('get length profile from file ' + file + "\n")
#         filename = os.path.splitext(file)[0].split('_')
#         samplename = filename[0]
#         marker = '_'.join(filename[1:])

#         input_file_path = os.path.normpath(separatoutfolderpath + '/' + file)
#         output_file_path = os.path.normpath(markerstatisticsfolderpath + '/' + marker + '_' + samplename + '_.Statistics')
#         getLengthProfilePerSample(input_file_path, output_file_path, marker, samplename, primersdict)
        
#         if (marker in primersdict["primersboundaries"] and ("dupl" in marker)):
#             marker_original = "".join(marker.split("dupl"))
#             # pattern = r'dupl[1-9]|dupl10'
#             # marker_original = re.sub(pattern, '', marker)
#             print(marker)
#             print(marker_original)
#             #file_original = re.sub(pattern, '', file)
#             file_original = "".join(file.split("dupl"))
#             print(file)
#             print(file_original)
#             output_file_path_dupl = os.path.normpath(duplicate_folder + '/' + marker_original + '_' + samplename + '_.Statistics')
#             input_file_path = os.path.normpath(separatoutfolderpath + '/' + file_original)
#             getLengthProfilePerSample(input_file_path, output_file_path_dupl, marker_original, samplename, primersdict)
#             #list_original_markers.append(marker_original)
#             print(output_file_path_dupl)
                
#             output_file_path_dupl = os.path.normpath(duplicate_folder + '/' + marker + '_' + samplename + '_.Statistics')
#             input_file_path = os.path.normpath(separatoutfolderpath + '/' + file)
#             getLengthProfilePerSample(input_file_path, output_file_path_dupl, marker, samplename, primersdict)
#             print(output_file_path_dupl)

# def getLengthProfilePerSample(fasta_path : str, out_path : str, marker : str, sample : str, primersdict : dict):
#     result = {} #{length : count}
#     result_reverse = {} #{count : length}
#     count_total = 0
#     count_list = []
#     length_list = []
#     try:
#         for header, sequence in parse_fasta(fasta_path).items():
#             seq_length = len(sequence)
#             length_list.append(seq_length)
#             if (seq_length not in result.keys()):
#                 result[seq_length] = 0
#             result[seq_length] += 1
        
#         for length, count in result.items():
#             count_list.append(count)
#             if (count not in result_reverse.keys()):
#                 result_reverse[count] = []
#             result_reverse[count].append(length)
        
#         count_list = list(set(count_list))
#         count_list.sort()
#         length_list = list(set(length_list))
#         length_list.sort()

#         with open(out_path, 'w') as output_file:
#             if (marker in primersdict["primersboundaries"]):
#                 for count in count_list:
#                     lengths = result_reverse[count]
#                     lengths.sort()
#                     for length in lengths:
#                         line = str(length) + ' ' + str(count)
#                         for boundary in primersdict["primersboundaries"][marker]:
#                             line += ' ' + str(boundary[0]) + ' ' + str(boundary[1])
#                         output_file.write(line + ' \n')
#             else:
#                 for count in count_list:
#                     lengths = result_reverse[count]
#                     lengths.sort()
#                     for length in lengths:
#                         output_file.write(str(length) + ' ' + str(count) + '\n')
#     except Exception as e:
#         print(f"Error when trying to process fastafile {os.path.basename(os.path.normpath(fasta_path))} ! \nException: {e} \n")


if __name__ == "__main__":
    main()