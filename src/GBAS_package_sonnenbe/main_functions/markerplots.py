from pathlib import Path
import customtkinter as ctk
import json, csv, subprocess, os, sys

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
matplotlib.use("Agg")

from GBAS_package_sonnenbe.helper_functions.filter_matrix import filtering


def main():
    
    return 0


def runMarkerplots_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict, primers_dict : dict, samples_dict : dict, filtering_param : float):
    markerstatistics_path = Path(paramsdict["Outputfolder"] + '/MarkerStatistics')
    markerstatistics_path_json = Path(paramsdict["Outputfolder"] + '/MarkerStatistics/markerstatistics.json')
    markerplots_path = Path(paramsdict["Outputfolder"] + '/Markerplots')
    markerstatistics_path_dupl_json = Path(paramsdict["Outputfolder"] + '/MarkerStatistics/markerstatistics_dupl.json')
    markerplots_dupl_path = Path(paramsdict["Outputfolder"] + '/Markerplots_dupl')
    min_count = int(paramsdict["Mincount"])
    consensusthreshold = float(paramsdict["Consensusthreshold"])
    lengthwindow = paramsdict["Lengthwindow"]
    textbox_pipeline.insert('end-1c', "\nStarting Markerplots! \n")
    if (paramsdict["Ploidy"] == "diploid"):
        runMarkerplots_diploid(markerstatistics_path_json, markerplots_path, "markerplots", primers_dict, min_count, consensusthreshold, lengthwindow)
        if (primers_dict["primersboundaries"]):
            runMarkerplots_diploid(markerstatistics_path_dupl_json, markerplots_dupl_path, "markerplots_dupl", primers_dict, min_count, consensusthreshold, lengthwindow)
    elif (paramsdict["Ploidy"] == "haploid"):
        runMarkerplots_haploid(markerstatistics_path_json, markerplots_path, "markerplots", primers_dict, min_count, consensusthreshold, lengthwindow)
    
    markerplots_path_json = Path(paramsdict["Outputfolder"] + '/Markerplots/markermatrix.json')
    markerplots_path_excel = Path(paramsdict["Outputfolder"] + '/Markerplots/markermatrix.csv')
    markerplots_path_excel_cleaned = Path(paramsdict["Outputfolder"] + '/Markerplots/markermatrix_cleaned.csv')
    markerplots_path_excel_filtered = Path(paramsdict["Outputfolder"] + '/Markerplots/markermatrix_cleaned_filtered.csv')
    makematrix(markerplots_path_json, markerplots_path_excel, paramsdict["Ploidy"], primers_dict, samples_dict)
    makematrix_cleaned(markerplots_path_json, markerplots_path_excel_cleaned, paramsdict["Ploidy"], primers_dict, samples_dict)
    filtering(markerplots_path_excel_cleaned, markerplots_path_excel_filtered, filtering_param)
    textbox_pipeline.insert('end-1c', "\n Markerplots finished! \n")



def runMarkerplots_CLI(paramsdict : dict, primers_dict : dict, samples_dict : dict, filtering_param : float):
    markerstatistics_path = Path(paramsdict["Outputfolder"] + '/MarkerStatistics')
    markerstatistics_path_json = Path(paramsdict["Outputfolder"] + '/MarkerStatistics/markerstatistics.json')
    markerplots_path = Path(paramsdict["Outputfolder"] + '/Markerplots')
    markerstatistics_path_dupl_json = Path(paramsdict["Outputfolder"] + '/MarkerStatistics/markerstatistics_dupl.json')
    markerplots_dupl_path = Path(paramsdict["Outputfolder"] + '/Markerplots_dupl')
    min_count = int(paramsdict["Mincount"])
    consensusthreshold = float(paramsdict["Consensusthreshold"])
    lengthwindow = paramsdict["Lengthwindow"]
    print("\nStarting Markerplots! \n")
    if (paramsdict["Ploidy"] == "diploid"):
        runMarkerplots_diploid(markerstatistics_path_json, markerplots_path, "markerplots", primers_dict, min_count, consensusthreshold, lengthwindow)
        if (primers_dict["primersboundaries"]):
            runMarkerplots_diploid(markerstatistics_path_dupl_json, markerplots_dupl_path, "markerplots_dupl", primers_dict, min_count, consensusthreshold, lengthwindow)
    elif (paramsdict["Ploidy"] == "haploid"):
        runMarkerplots_haploid(markerstatistics_path_json, markerplots_path, "markerplots", primers_dict, min_count, consensusthreshold, lengthwindow)
    
    markerplots_path_json = Path(paramsdict["Outputfolder"] + '/Markerplots/markermatrix.json')
    markerplots_path_excel = Path(paramsdict["Outputfolder"] + '/Markerplots/markermatrix.csv')
    markerplots_path_excel_cleaned = Path(paramsdict["Outputfolder"] + '/Markerplots/markermatrix_cleaned.csv')
    markerplots_path_excel_filtered = Path(paramsdict["Outputfolder"] + '/Markerplots/markermatrix_cleaned_filtered.csv')
    makematrix(markerplots_path_json, markerplots_path_excel, paramsdict["Ploidy"], primers_dict, samples_dict)
    makematrix_cleaned(markerplots_path_json, markerplots_path_excel_cleaned, paramsdict["Ploidy"], primers_dict, samples_dict)
    filtering(markerplots_path_excel_cleaned, markerplots_path_excel_filtered, filtering_param)
    print("\n Markerplots finished! \n")

def makematrix_cleaned(lengthmatrixjsonpath : Path, markerplots_path_excel : Path, ploidy : str, primersdict : dict, samples_dict : dict):
    markermatrix_dict = {}
    with open(lengthmatrixjsonpath) as json_file:
        markermatrix_dict = json.load(json_file)
    loci_list = [locus for locus in primersdict["primers"].keys()]
    if (ploidy == "diploid"):
        loci_list = []
        for locus in markermatrix_dict.keys():
            loci_list.append(locus)
            loci_list.append(locus)
    sample_list = [locus for locus in samples_dict["reverse"].keys()]
    
    print(loci_list)
    print(sample_list)
    
    loci_list = ["samples"] + loci_list
    with open(markerplots_path_excel, 'w', newline='') as outcsv:
        csvwriter = csv.writer(outcsv, delimiter=';')
        csvwriter.writerow(loci_list)
        for sample in sample_list:
            row = []
            if (sample in markermatrix_dict[locus]["Samples"]):
                row.append(sample)
                for locus in markermatrix_dict.keys():
                    if (not(markermatrix_dict[locus]["Samples"][sample]["LengthAlleles"])):
                        row.append(0)
                        if (ploidy == "diploid"):
                            row.append(0)
                    for length, count in markermatrix_dict[locus]["Samples"][sample]["LengthAlleles"].items():
                        # if (markermatrix_dict[locus]["Samples"][sample]["Information"] == "Needs Manual Check"):
                        #     length = str(length) + "_man_check"
                        row.append(str(length))
                        if (ploidy == "diploid"):
                            if (len(markermatrix_dict[locus]["Samples"][sample]["LengthAlleles"]) == 1):
                                row.append(str(length))
                csvwriter.writerow(row)



def makematrix(lengthmatrixjsonpath : Path, markerplots_path_excel : Path, ploidy : str, primersdict : dict, samples_dict : dict):
    markermatrix_dict = {}
    with open(lengthmatrixjsonpath) as json_file:
        markermatrix_dict = json.load(json_file)
    loci_list = [locus for locus in primersdict["primers"].keys()]
    if (ploidy == "diploid"):
        loci_list = []
        for locus in markermatrix_dict.keys():
            loci_list.append(locus)
            loci_list.append(locus)
    sample_list = [locus for locus in samples_dict["reverse"].keys()]
    
    print(loci_list)
    print(sample_list)
    
    loci_list = ["samples"] + loci_list
    with open(markerplots_path_excel, 'w', newline='') as outcsv:
        csvwriter = csv.writer(outcsv, delimiter=';')
        csvwriter.writerow(loci_list)
        for sample in sample_list:
            row = []
            if (sample in markermatrix_dict[locus]["Samples"]):
                row.append(sample)
                for locus in markermatrix_dict.keys():
                    if (not(markermatrix_dict[locus]["Samples"][sample]["LengthAlleles"])):
                        value = ""
                        if (markermatrix_dict[locus]["Samples"][sample]["Information"] == "Empty File"):
                            value = "empty"
                        if (markermatrix_dict[locus]["Samples"][sample]["Information"] == "Empty File"):
                            value = "Too Little Read Count"
                        else:
                            value = "0"
                        row.append(value)
                        if (ploidy == "diploid"):
                            row.append(value)
                    for length, count in markermatrix_dict[locus]["Samples"][sample]["LengthAlleles"].items():
                        if (markermatrix_dict[locus]["Samples"][sample]["Information"] == "Needs Manual Check"):
                            length = str(length) + "_man_check"
                        row.append(str(length))
                        if (ploidy == "diploid"):
                            if (len(markermatrix_dict[locus]["Samples"][sample]["LengthAlleles"]) == 1):
                                row.append(str(length))
                csvwriter.writerow(row)




def runMarkerplots_haploid():
    pass    

def runMarkerplots_diploid(markerstatistics_path_json : Path, markerplots_path : Path, markerplots_name : str, primersdict : dict, min_count : int, consensusthreshold : float, lengthwindow : str):
    statistics_dict = {}
    with open(markerstatistics_path_json) as json_file:
        statistics_dict = json.load(json_file)

    plots_per_page = 6
    markerplots_path_pdf = Path(markerplots_path / (markerplots_name + ".pdf"))
    #markerplots_path_pdf = Path(markerplots_path / "markerplots.pdf")
    markerplots_json = Path(markerplots_path / "markermatrix.json")
    counter = 1

    lengthwindow_min = int(lengthwindow.split(",")[0].strip())
    lengthwindow_max = int(lengthwindow.split(",")[1].strip())
    with PdfPages(markerplots_path_pdf) as pdf:
        length_matrix_dict = {}

        fig = None
        axes = None
        ax_idx = 0
        for primer, rest in statistics_dict.items():
            if (primer not in length_matrix_dict):
                length_matrix_dict[primer] = {}
                if (primer in primersdict["primersboundaries"]):
                    length_matrix_dict[primer]["LengthBoundaries"] = primersdict["primersboundaries"][primer] 
                length_matrix_dict[primer]["Samples"] = {}

            primer_parts = primer.split("_")
            if (len(primer_parts) < 2):
                print("Primer " + primer + " is not in correct format!: primername + _ + primermotif. \n")
                continue
            primername = primer_parts[0]
            primer_motif = primer_parts[1]
            repsiz = len(primer_motif)
            for sample, rest2 in rest["Samples"].items():
                if (sample not in length_matrix_dict[primer]["Samples"]):
                    length_matrix_dict[primer]["Samples"][sample] = {}
                length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"] = {}
                length_matrix_dict[primer]["Samples"][sample]["Information"] = ""

                total_count = sum(rest2["Lengths-Counts"].values())
                # if (total_count == 0):
                #     continue

                min_length = 0
                max_length = 0
                max_length2 = 0
                max_count = 0
                max_count_relative = 0
                max_count2 = 0
                max_count2_relative = 0
                number_counts = 0
                lengths = []
                lengths_sorted = []
                counts = []
                count_freqs = []

                if (total_count != 0):

                    lengths_counts = list(rest2["Lengths-Counts"].items())
                    lengths_counts_sorted = sorted(lengths_counts, key=lambda x : x[1], reverse=True)

                    lengths = [int(k) for k in rest2["Lengths-Counts"].keys()]
                    counts = [int(k) for k in rest2["Lengths-Counts"].values()]

                    lengths_sorted = [int(length) for length, count in lengths_counts_sorted]
                    counts_sorted  = [int(count)  for length, count in lengths_counts_sorted]
                    number_counts = len(counts_sorted)
                    count_freqs = [(int(count)/int(total_count))*100 for count in counts_sorted]

                    max_count = counts_sorted[0]
                    max_count_relative = count_freqs[0]
                    min_count = counts_sorted[-1]
                    min_count_relative = count_freqs[-1]
                    max_length = lengths_sorted[0]
                    min_length = lengths_sorted[-1]

                    
                    if (number_counts > 1):
                        max_count2 = counts_sorted[1]
                        max_count2_relative = count_freqs[1]
                        max_length2 = lengths_sorted[1]
                    else:
                        max_count2 = max_count
                        max_count2_relative = max_count_relative
                        max_length2 = max_length
                
                b1 = max_count - max_count2
                b2 = (max_count2*2)
                #b3 = (1-(max_count+max_count2))
                b3 = (total_count - (max_count+max_count2))

                if (fig is None or ax_idx == 0):
                    fig, axes = plt.subplots(plots_per_page, 1, figsize=(7, 18))
                    #xes = list(axes) if isinstance(axes, (list, tuple)) else [axes]
                    ax_idx = 0

                ax = axes[ax_idx]
                ax.set_title(f"Marker: {primer}, Sample: {sample}", pad=18)
                ax.bar(lengths_sorted, count_freqs, width=0.1, color="black", edgecolor="black")
                for x, y in zip(lengths, count_freqs):
                    ax.text(x, y + 0.5, f"{x}", ha="center", va="bottom", fontsize=8, color="black")


                if ((max_count > min_count) and (number_counts > 1)):
                    #first case one length highly abundant - homozygous because of baryzentric coordinates
                    if ((b1 >= b2) & (b1 >= b3)):
                        length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length] = max_count
                        length_matrix_dict[primer]["Samples"][sample]["Information"] = "Homozygous"
                        #print("Reached1")
                        ax.text(0.5, 1.02, "Homozygous, read length and count is: " + str(max_length) + ": " + str(max_count) + " Total Count: " + str(total_count), transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="blue")
                        ax.bar(max_length, max_count_relative, width=0.1, color="blue", edgecolor="blue")
                        ax.text(x=max_length, y=max_count_relative + 0.5, s=str(max_length), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                        if ("LengthBoundaries" in rest):
                            text_to_add = "Length Boundaries: "
                            for boundary in rest["LengthBoundaries"]:
                                text_to_add += "[" + str(boundary[0]) + "," + str(boundary[1]) + "], "
                            ax.text(0.5, -0.3, text_to_add, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="black")
                    elif (repsiz != 0):
                        #print("Reached2")
                        #second case: heterozygous, most abundant and second most abundant larger than b1 and b3, difference in length according to repeat length, second highest allele longer than highest
                        if ((b2 >= b1) and (b2 >= b3) and ((abs(max_length2-max_length)) >= repsiz) and ((max_length2-max_length) > 0) and ((abs(max_length2-max_length)) % repsiz == 0)):
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length] = max_count
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length2] = max_count2
                            length_matrix_dict[primer]["Samples"][sample]["Information"] = "Heterozygous"
                            #print("Reached3")
                            ax.text(0.5, 1.02, "Heterozygous, read length and count is: " + str(max_length) + ": " + str(max_count) + "and " + str(max_length2) + ": " + str(max_count2) + ", Total Count: " + str(total_count), transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="green")
                            ax.bar(max_length, max_count_relative, width=0.1, color="green", edgecolor="green")
                            ax.bar(max_length2, max_count2_relative, width=0.1, color="green", edgecolor="green")
                            ax.text(x=max_length, y=max_count_relative + 0.5, s=str(max_length), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            ax.text(x=max_length2, y=max_count2_relative + 0.5, s=str(max_length2), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            if ("LengthBoundaries" in rest):
                                text_to_add = "Length Boundaries: "
                                for boundary in rest["LengthBoundaries"]:
                                    text_to_add += "[" + str(boundary[0]) + "," + str(boundary[1]) + "], "
                                ax.text(0.5, -0.3, text_to_add, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="black")
                        #third case - heterozygous, diff most abundant and second most in length more than 1 x repeat size (exclusion stutter), difference exactly integer x repeat size
                        elif ((b2 >= b1) and (b2 >= b3) and (abs(max_length2-max_length) > repsiz) and (abs(max_length2-max_length) % repsiz == 0)):
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length] = max_count
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length2] = max_count2
                            length_matrix_dict[primer]["Samples"][sample]["Information"] = "Heterozygous"
                            #print("Reached4")
                            ax.text(0.5, 1.02, "Heterozygous, read length and count is: " + str(max_length) + ": " + str(max_count) + "and " + str(max_length2) + ": " + str(max_count2) + ", Total Count: " + str(total_count), transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="red")
                            ax.bar(max_length, max_count_relative, width=0.1, color="red", edgecolor="red")
                            ax.bar(max_length2, max_count2_relative, width=0.1, color="red", edgecolor="red")
                            ax.text(x=max_length, y=max_count_relative + 0.5, s=str(max_length), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            ax.text(x=max_length2, y=max_count2_relative + 0.5, s=str(max_length2), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            if ("LengthBoundaries" in rest):
                                text_to_add = "Length Boundaries: "
                                for boundary in rest["LengthBoundaries"]:
                                    text_to_add += "[" + str(boundary[0]) + "," + str(boundary[1]) + "], "
                                ax.text(0.5, -0.3, text_to_add, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="black")
                        # fourth case - point mutations that are minimum size of 60% max peak but don't match repeat size, HERE change due to FILTER
                        elif ((b2 >= b1) & (b2 >= b3) & ((max_count2/total_count) > (0.6*max_count/total_count)) and ((abs(max_length2-max_length)) % repsiz != 0)):
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length] = max_count
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length2] = max_count2
                            length_matrix_dict[primer]["Samples"][sample]["Information"] = "Possibly heterozygous point mutation"
                            #print("Reached5")
                            ax.text(0.5, 1.02, "Possibly heterozygous point mutation, read length and count is: " + str(max_length) + ": " + str(max_count) + "and " + str(max_length2) + ": " + str(max_count2) + ", Total Count: " + str(total_count), transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="green")
                            ax.bar(max_length, max_count_relative, width=0.1, color="red", edgecolor="red")
                            ax.bar(max_length2, max_count2_relative, width=0.1, color="red", edgecolor="red")
                            ax.text(x=max_length, y=max_count_relative + 0.5, s=str(max_length), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            ax.text(x=max_length2, y=max_count2_relative + 0.5, s=str(max_length2), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            if ("LengthBoundaries" in rest):
                                text_to_add = "Length Boundaries: "
                                for boundary in rest["LengthBoundaries"]:
                                    text_to_add += "[" + str(boundary[0]) + "," + str(boundary[1]) + "], "
                                ax.text(0.5, -0.3, text_to_add, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="black")
                        # fifth case - only one repeat size difference but second largest peak is minimum size of 0.75 % of the largest one, 
                        elif ((b2 >= b1) and (b2 >= b3) and ((max_count2/total_count) > (0.75*max_count/total_count)) and (abs(max_length2-max_length) == repsiz)):
                            #print("Reached6")
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length] = max_count
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length2] = max_count2
                            length_matrix_dict[primer]["Samples"][sample]["Information"] = "Heterozygous"
                            ax.text(0.5, 1.02, "Heterozygous, read length and count is: " + str(max_length) + ": " + str(max_count) + "and " + str(max_length2) + ": " + str(max_count2) + ", Total Count: " + str(total_count), transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="black")
                            ax.bar(max_length, max_count_relative, width=0.1, color="red", edgecolor="red")
                            ax.bar(max_length2, max_count2_relative, width=0.1, color="red", edgecolor="red")
                            ax.text(x=max_length, y=max_count_relative + 0.5, s=str(max_length), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            ax.text(x=max_length2, y=max_count2_relative + 0.5, s=str(max_length2), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            if ("LengthBoundaries" in rest):
                                text_to_add = "Length Boundaries: "
                                for boundary in rest["LengthBoundaries"]:
                                    text_to_add += "[" + str(boundary[0]) + "," + str(boundary[1]) + "], "
                                ax.text(0.5, -0.3, text_to_add, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="black")
                        else:
                            #print("Reached6")
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length] = max_count
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length2] = max_count2
                            length_matrix_dict[primer]["Samples"][sample]["Information"] = "Needs manual check"
                            ax.text(0.5, 1.02, "Needs manual check, read length and count is: " + str(max_length) + ": " + str(max_count) + "and " + str(max_length2) + ": " + str(max_count2) + ", Total Count: " + str(total_count), transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="black")
                            ax.bar(max_length, max_count_relative, width=0.1, color="red", edgecolor="red")
                            ax.bar(max_length2, max_count2_relative, width=0.1, color="red", edgecolor="red")
                            ax.text(x=max_length, y=max_count_relative + 0.5, s=str(max_length), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            ax.text(x=max_length2, y=max_count2_relative + 0.5, s=str(max_length2), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            if ("LengthBoundaries" in rest):
                                text_to_add = "Length Boundaries: "
                                for boundary in rest["LengthBoundaries"]:
                                    text_to_add += "[" + str(boundary[0]) + "," + str(boundary[1]) + "], "
                                ax.text(0.5, -0.3, text_to_add, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="black")
                    elif (repsiz == 0):
                        if ((b2 >= b1) and (b2 >= b3) and ((max_count2/total_count) > ((0.6 * max_count2)/total_count))):
                            #print("Reached7")
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length] = max_count
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length2] = max_count2
                            length_matrix_dict[primer]["Samples"][sample]["Information"] = "Possibly heterozygous point mutation"
                            ax.text(0.5, 1.02, "Possibly heterozygous point mutation, read length and count is: " + str(max_length) + ": " + str(max_count) + "and " + str(max_length2) + ": " + str(max_count2) + ", Total Count: " + str(total_count), transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="green")
                            ax.bar(max_length, max_count_relative, width=0.1, color="red", edgecolor="red")
                            ax.bar(max_length2, max_count2_relative, width=0.1, color="red", edgecolor="red")
                            ax.text(x=max_length, y=max_count_relative + 0.5, s=str(max_length), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            ax.text(x=max_length2, y=max_count2_relative + 0.5, s=str(max_length2), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            if ("LengthBoundaries" in rest):
                                text_to_add = "Length Boundaries: "
                                for boundary in rest["LengthBoundaries"]:
                                    text_to_add += "[" + str(boundary[0]) + "," + str(boundary[1]) + "], "
                                ax.text(0.5, -0.3, text_to_add, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="black")
                        else:
                            #print("Reached8")
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length] = max_count
                            length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length2] = max_count2
                            length_matrix_dict[primer]["Samples"][sample]["Information"] = "Needs Manual Check"
                            ax.text(0.5, 1.02, "Needs manual check, read length and count is: " + str(max_length) + ": " + str(max_count) + "and " + str(max_length2) + ": " + str(max_count2) + ", Total Count: " + str(total_count), transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="black")
                            ax.bar(max_length, max_count_relative, width=0.1, color="red", edgecolor="red")
                            ax.bar(max_length2, max_count2_relative, width=0.1, color="red", edgecolor="red")
                            ax.text(x=max_length, y=max_count_relative + 0.5, s=str(max_length), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            ax.text(x=max_length2, y=max_count2_relative + 0.5, s=str(max_length2), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                            if ("LengthBoundaries" in rest):
                                text_to_add = "Length Boundaries: "
                                for boundary in rest["LengthBoundaries"]:
                                    text_to_add += "[" + str(boundary[0]) + "," + str(boundary[1]) + "], "
                                ax.text(0.5, -0.3, text_to_add, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="black")

                elif ((max_count > min_count) and (number_counts == 1)):
                    #print("Reached10")
                    length_matrix_dict[primer]["Samples"][sample]["LengthAlleles"][max_length] = max_count
                    length_matrix_dict[primer]["Samples"][sample]["Information"] = "Homozygous, only one read length present"
                    ax.text(0.5, 1.02, "Homozygous, only one read length present: " + str(max_length) + ": " + str(max_count) + " Total Count: " + str(total_count), transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="black")
                    ax.bar(max_length, max_count_relative, width=0.1, color="red", edgecolor="blue")
                    ax.text(x=max_length, y=max_count_relative + 0.5, s=str(max_length), ha="center", va="bottom", fontsize=8, color="black", weight="bold")
                    if ("LengthBoundaries" in rest):
                        text_to_add = "Length Boundaries: "
                        for boundary in rest["LengthBoundaries"]:
                            text_to_add += "[" + str(boundary[0]) + "," + str(boundary[1]) + "], "
                        ax.text(0.5, -0.3, text_to_add, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="black")
                elif (total_count == 0):
                    ax.text(0.5, 1.02, "Empty file", transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="black")
                    #ax.axis("off")
                    length_matrix_dict[primer]["Samples"][sample]["Information"] = "Empty File"
                    if ("LengthBoundaries" in rest):
                        text_to_add = "Length Boundaries: "
                        for boundary in rest["LengthBoundaries"]:
                            text_to_add += "[" + str(boundary[0]) + "," + str(boundary[1]) + "], "
                        ax.text(0.5, -0.3, text_to_add, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="black")
                else:
                    ax.text(0.5, 1.02, "Too little read count", transform=ax.transAxes, ha="center", va="bottom", fontsize=9, color="black")
                    length_matrix_dict[primer]["Samples"][sample]["Information"] = "Too Little Read Count"
                    if ("LengthBoundaries" in rest):
                        text_to_add = "Length Boundaries: "
                        for boundary in rest["LengthBoundaries"]:
                            text_to_add += "[" + str(boundary[0]) + "," + str(boundary[1]) + "], "
                        ax.text(0.5, -0.3, text_to_add, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="black")



                #else:
                    #ax.bar(lengths, count_freqs, width=0.1, color="steelblue", edgecolor="black")

                #ax.bar(lengths, count_freqs, width=0.1, color="steelblue", edgecolor="black")
                ax.set_xlim(lengthwindow_min - 0.01 * lengthwindow_min, lengthwindow_max - 0.01 * lengthwindow_max)
                ax.set_ylim(0, 105)
                ax.set_xlabel("Allele Length")
                ax.set_ylabel("Count Frequency (%)")

                ax_idx += 1

                if (ax_idx == plots_per_page):
                    fig.tight_layout()
                    pdf.savefig(fig)
                    plt.close(fig)
                    fig = None
                    axes = None
                    ax_idx = 0
        
        if (fig is not None and ax_idx > 0):
            for empty_ax in axes[ax_idx:]:
                empty_ax.axis("off")
            fig.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)
    
    with open(markerplots_json, "w", encoding="utf-8") as f:
        json.dump(length_matrix_dict, f, indent=4, ensure_ascii=False)
    
    if markerplots_path_pdf.exists():
        if sys.platform.startswith("win"):
            os.startfile(markerplots_path_pdf)
        elif (sys.platform == "linux"):
            subprocess.run(["xdg-open", str(markerplots_path_pdf)])




if __name__ == "__main__":
    main()