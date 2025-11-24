from GBAS_package_sonnenbe.helper_functions.parse_primerfile import get_primers
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
import csv

def main():

    inputfolderpath = Path("E:\\Work_Paper_GUI\\PIC\\test_folder")
    outputfolderpath = Path("E:\\Work_Paper_GUI\\PIC\\output")
    calculate_PIC(inputfolderpath, outputfolderpath)


    return 0


def calculate_PIC(inputfolderpath : Path, outputfolderpath : Path):
    PIC_dict = {}
    for folderpath in inputfolderpath.iterdir():
        if (folderpath.is_dir()):
            project = folderpath.name
            PIC_dict[project] = {}
            PIC_dict[project]["Markers"] = {}

            primerpath = folderpath / "primers.txt"
            primers_dict = get_primers(primerpath)
            primer_list = [primer for primer, rest in primers_dict["primers"].items()]

            helper_dict = {}
            helper_dict["Markers"] = {}
            helper_dict["Markers"]["Allele"] = {}
            helper_dict["Markers"]["Length"] = {}
            for primer in primer_list:
                PIC_dict[project]["Markers"][primer] = {}
                PIC_dict[project]["Markers"][primer]["AlleleBased"] = {}
                PIC_dict[project]["Markers"][primer]["AlleleBased"]["TotalNumberAlleles"] = {}
                PIC_dict[project]["Markers"][primer]["AlleleBased"]["AlleleFrequencies"] = {}
                PIC_dict[project]["Markers"][primer]["LengthBased"] = {}
                PIC_dict[project]["Markers"][primer]["LengthBased"]["TotalNumberAlleles"] = {}
                PIC_dict[project]["Markers"][primer]["LengthBased"]["AlleleFrequencies"] = {}
                helper_dict["Markers"]["Allele"][primer] = []
                helper_dict["Markers"]["Length"][primer] = []

            length_matrices_path = folderpath / "length_matrices"
            allele_matrices_path = folderpath / "allele_matrices"


            for allele_matrix_path in allele_matrices_path.iterdir():
                if (allele_matrix_path.suffix == ".csv"):
                    df = pd.read_csv(allele_matrix_path, sep=r"[;,|\t]", engine="python")
                elif (allele_matrix_path.suffix == ".xlsx"):
                    df = pd.read_excel(allele_matrix_path) #sheet_name="Barcording_database"
                else:
                    print("\nThis is not excel fileformat!\n")
                    return
                
                print(df)
                primer_headers = [header.strip() for header in list(df.columns)]
                for _, row in df.iterrows():
                    for primer in primer_list:
                        values = [int(value) for key, value in row.items() if primer in key]
                        helper_dict["Markers"]["Allele"][primer].extend(values)

            for primer in primer_list:
                total_alleles = sum([1 for value in helper_dict["Markers"]["Allele"][primer] if (value > 0)])
                PIC_dict[project]["Markers"][primer]["AlleleBased"]["TotalNumberAlleles"] = total_alleles
                sum_freqs = 0.0
                if (total_alleles > 0):
                    unique_vals = list(set(helper_dict["Markers"]["Allele"][primer]))
                    for val in unique_vals:
                        if (not(val > 0)):
                            continue
                        value_count = sum([1 for value in helper_dict["Markers"]["Allele"][primer] if ((value == val))])
                        value_freq = value_count/total_alleles
                        value_freq_sq = value_freq**2
                        PIC_dict[project]["Markers"][primer]["AlleleBased"]["AlleleFrequencies"][val] = value_freq
                        #print(value_freq_sq)
                        sum_freqs = sum_freqs + value_freq_sq

                    #print(sum_freqs)
                    PIC_dict[project]["Markers"][primer]["AlleleBased"]["AlleleFrequencies"] = dict(sorted(PIC_dict[project]["Markers"][primer]["AlleleBased"]["AlleleFrequencies"].items(), key=lambda x: int(x[0])))
                    PIC_dict[project]["Markers"][primer]["AlleleBased"]["PIC"] = 1 - sum_freqs
                else:
                    PIC_dict[project]["Markers"][primer]["AlleleBased"]["PIC"] = 0
            

            for length_matrix_path in length_matrices_path.iterdir():
                if (length_matrix_path.suffix == ".csv"):
                    df = pd.read_csv(length_matrix_path, sep=r"[;,|\t]", engine="python")
                elif (length_matrix_path.suffix == ".xlsx"):
                    df = pd.read_excel(length_matrix_path) #sheet_name="Barcording_database"
                else:
                    print("\nThis is not excel fileformat!\n")
                    return
                
                df = df.replace({"empty": "0","too little reads": "0"})
                print(df)
                primer_headers = [header.strip() for header in list(df.columns)]
                for _, row in df.iterrows():
                    for primer in primer_list:
                        values = [int(str(value).split("_")[0].strip()) for key, value in row.items() if primer in key]
                        helper_dict["Markers"]["Length"][primer].extend(values)

            print("NOW\n")
            print(helper_dict["Markers"]["Length"])
            for primer in primer_list:
                total_alleles = sum([1 for value in helper_dict["Markers"]["Length"][primer] if (value > 0)])
                PIC_dict[project]["Markers"][primer]["LengthBased"]["TotalNumberAlleles"] = total_alleles
                sum_freqs = 0.0
                if (total_alleles > 0):
                    unique_vals = list(set(helper_dict["Markers"]["Length"][primer]))
                    for val in unique_vals:
                        if (not(val > 0)):
                            continue
                        #print(val)
                        value_count = sum([1 for value in helper_dict["Markers"]["Length"][primer] if ((value == val))])
                        value_freq = value_count/total_alleles
                        value_freq_sq = value_freq**2
                        PIC_dict[project]["Markers"][primer]["LengthBased"]["AlleleFrequencies"][val] = value_freq
                        #print(value_freq_sq)
                        sum_freqs = sum_freqs + value_freq_sq

                    #print(sum_freqs)
                    PIC_dict[project]["Markers"][primer]["LengthBased"]["AlleleFrequencies"] = dict(sorted(PIC_dict[project]["Markers"][primer]["LengthBased"]["AlleleFrequencies"].items(), key=lambda x: int(x[0])))
                    PIC_dict[project]["Markers"][primer]["LengthBased"]["PIC"] = 1 - sum_freqs
                else:
                    PIC_dict[project]["Markers"][primer]["LengthBased"]["PIC"] = 0

    dict_additional = {}
    n = 5

    for project, rest in PIC_dict.items():
        dict_additional[project] = {}
        dict_additional[project]["Best " + str(5) + " performing markers (SequenceBased)"] = {}
        dict_additional[project]["Best " + str(5) + " performing markers (LengthBased)"] = {}

        dict_additional[project]["Highest " + str(5) + " PIC increases from LengthBased to SequenceBased"] = {}

        PIC_values = [(primer, rest["AlleleBased"]["PIC"]) for primer, rest in PIC_dict[project]["Markers"].items()]
        PIC_values_sorted_sequencebased = sorted(PIC_values, key=lambda x : x[1], reverse=True)

        PIC_values = [(primer, rest["LengthBased"]["PIC"]) for primer, rest in PIC_dict[project]["Markers"].items()]
        PIC_values_sorted_lengthbased = sorted(PIC_values, key=lambda x : x[1], reverse=True)

        PIC_values_differences = [(primer, (rest["AlleleBased"]["PIC"], rest["LengthBased"]["PIC"], rest["AlleleBased"]["PIC"]-rest["LengthBased"]["PIC"])) for primer, rest in PIC_dict[project]["Markers"].items()]
        PIC_values_sorted_differences = sorted(PIC_values_differences, key=lambda x : x[1][2], reverse=True)

        for i in range(0, 5, 1):
            dict_additional[project]["Best " + str(5) + " performing markers (SequenceBased)"][PIC_values_sorted_sequencebased[i][0]] = PIC_values_sorted_sequencebased[i][1]
            dict_additional[project]["Best " + str(5) + " performing markers (LengthBased)"][PIC_values_sorted_lengthbased[i][0]] = PIC_values_sorted_lengthbased[i][1]

            dict_additional[project]["Highest " + str(5) + " PIC increases from LengthBased to SequenceBased"][PIC_values_sorted_differences[i][0]] = {}
            dict_additional[project]["Highest " + str(5) + " PIC increases from LengthBased to SequenceBased"][PIC_values_sorted_differences[i][0]]["PIC Lengthbased"] = PIC_values_sorted_differences[i][1][1]
            dict_additional[project]["Highest " + str(5) + " PIC increases from LengthBased to SequenceBased"][PIC_values_sorted_differences[i][0]]["PIC Sequencebased"] = PIC_values_sorted_differences[i][1][0]
            dict_additional[project]["Highest " + str(5) + " PIC increases from LengthBased to SequenceBased"][PIC_values_sorted_differences[i][0]]["PIC Difference"] = PIC_values_sorted_differences[i][1][2]





    PIC_json_path = outputfolderpath / 'PIC_results.json'
    with open(PIC_json_path, 'w') as json_output:
        json.dump(PIC_dict, json_output, indent = 4)

    PIC_json_additional_path = outputfolderpath / 'PIC_additional_info.json'
    with open(PIC_json_additional_path, 'w') as json_output:
        json.dump(dict_additional, json_output, indent = 4)
    

    with open(PIC_json_path, "r") as f:
        data = json.load(f)
    
    for folderpath in inputfolderpath.iterdir():
        if (folderpath.is_dir()):
            project = folderpath.name

            markers = data[project]["Markers"]
            marker_names = list(markers.keys())
            allele_pics = [markers[m]["AlleleBased"]["PIC"]  for m in marker_names]
            length_pics = [markers[m]["LengthBased"]["PIC"] for m in marker_names]

            x = np.arange(len(marker_names))
            width = 0.35

            fig, ax = plt.subplots(figsize=(12, 5))

            ax.bar(x - width/2, allele_pics, width, label="Allele-based PIC")
            ax.bar(x + width/2, length_pics, width, label="Length-based PIC")

            ax.set_xticks(x)
            ax.set_xticklabels(marker_names, rotation=45, ha="right")
            ax.set_ylabel("PIC value")
            ax.set_title(f"Allele vs Length-based PIC – Project {project}")
            ax.set_ylim(0, 1)
            ax.legend()

            plt.tight_layout()

            savepath = outputfolderpath / f"{project}_PIC_histogram.png"
            plt.savefig(savepath, dpi=200)
            plt.close(fig)

            print(f"Saved PIC histogram for project '{project}' to {savepath}")
            

def calculate_PIC2(inputfolderpath : Path, outputfolderpath : Path):
    PIC_dict = {}
    for folderpath in inputfolderpath.iterdir():
        if (folderpath.is_dir()):
            project = folderpath.name
            PIC_dict[project] = {}
            PIC_dict[project]["Markers"] = {}


            primerpath = folderpath / "primers.txt"
            primers_dict = get_primers(primerpath)
            primer_list = [primer for primer, rest in primers_dict["primers"].items()]
            print("\n\n")
            print(primer_list)

            for primer in primer_list:
                PIC_dict[project]["Markers"][primer] = {}

            length_matrices_path = folderpath / "length_matrices"
            allele_matrices_path = folderpath / "allele_matrices"

            for length_matrix_path in length_matrices_path.iterdir():
                if ("LengthBased" not in PIC_dict[project]["Markers"][primer]):
                    PIC_dict[project]["Markers"][primer]["LengthBased"] = {}
                if (length_matrix_path.suffix == ".csv"):
                    df = pd.read_csv(length_matrix_path, sep=r"[;,|\t]", engine="python")
                elif (length_matrix_path.suffix == ".xlsx"):
                    df = pd.read_excel(length_matrix_path) #sheet_name="Barcording_database"
                else:
                    print("\nThis is not excel fileformat!\n")
                    return
                
                df = df.replace({"empty": "0","too little reads": "0"})
                df = df.applymap(lambda x: x.split("_")[0] if isinstance(x, str) and "_" in x else x)
                
                primer_headers = [header.strip() for header in list(df.columns)]
                #primer_headers = list(set([str(header).strip() for header in list(df.columns)]))

                print(primer_headers)
                if ("AlleleFrequencies" not in PIC_dict[project]["Markers"][primer]["LengthBased"]):
                    PIC_dict[project]["Markers"][primer]["LengthBased"]["AlleleFrequencies"] = {}
                list_values = []
                for _, row in df.iterrows(): #ignoring row indexes with _
                    #print(row)
                    for primer in primer_list:
                        values = [int(value) for key, value in row.items() if primer in key]
                        print(values)
                        list_values.extend(values)
                total_alleles = sum([1 for value in list_values if (value > 0)])
                sum_freqs = 0
                for val in list_values:
                    value_count = sum([1 for value in list_values if (value == val)])
                    value_freq = value_count/total_alleles
                    PIC_dict[project]["Markers"][primer]["LengthBased"]["AlleleFrequencies"][val] = value_freq
                    sum_freqs += value_freq**2

                PIC_dict[project]["Markers"][primer]["LengthBased"]["PIC"] = 1 - sum_freqs


    allelelist_json_path = outputfolderpath / 'PIC_results.json'
    with open(allelelist_json_path, 'w') as json_output:
        json.dump(PIC_dict, json_output, indent = 4)


if __name__ == "__main__":
    main()