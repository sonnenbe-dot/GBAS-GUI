from GBAS_package_sonnenbe.helper_functions.parse_primerfile import get_primers
from GBAS_package_sonnenbe.helper_functions.filter_matrix import filtering

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


def calculate_PIC_webbased(dict_projects : dict):
    pass


def calculate_PIC(inputfolderpath : Path, outputfolderpath : Path, filtering_param : float):
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
                filtered_matrix_path = allele_matrices_path / (allele_matrix_path.stem + "_filtered.csv")
                # print(allele_matrix_path.name)
                # print("\nCHECK HERE!!\n")
                # print(allele_matrix_path.suffix)
                if(allele_matrix_path.name.startswith("~$")):
                   continue
                filtering(allele_matrix_path, filtered_matrix_path, filtering_param)

                if (filtered_matrix_path.suffix == ".csv"):
                    df = pd.read_csv(filtered_matrix_path, sep=r"[;,|\t]", engine="python")
                elif (filtered_matrix_path.suffix == ".xlsx"):
                    df = pd.read_excel(filtered_matrix_path) #sheet_name="Barcording_database"
                else:
                    print("\nThis is not excel fileformat!\n")
                    return

                if filtered_matrix_path.exists():
                    filtered_matrix_path.unlink()
                
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
                filtered_matrix_path = length_matrices_path / (length_matrix_path.stem + "_filtered.csv")
                if(length_matrix_path.name.startswith("~$")):
                   continue
                filtering(length_matrix_path, filtered_matrix_path, filtering_param)

                if (filtered_matrix_path.suffix == ".csv"):
                    df = pd.read_csv(filtered_matrix_path, sep=r"[;,|\t]", engine="python")
                elif (filtered_matrix_path.suffix == ".xlsx"):
                    df = pd.read_excel(filtered_matrix_path) #sheet_name="Barcording_database"
                else:
                    print("\nThis is not excel fileformat!\n")
                    return
                
                if filtered_matrix_path.exists():
                    filtered_matrix_path.unlink()
                
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
                
                PIC_dict[project]["Markers"][primer]["PIC SequenceBased - PIC Lengthbased"] = PIC_dict[project]["Markers"][primer]["AlleleBased"]["PIC"] - PIC_dict[project]["Markers"][primer]["LengthBased"]["PIC"]



    dict_additional = {}
    n = 5
    
    for project, rest in PIC_dict.items():
        primers = [primer for primer in PIC_dict[project]["Markers"].keys()]
        PIC_excel_path = outputfolderpath / ("PIC_results" + str(project) + ".csv")
        with open(PIC_excel_path, 'w', newline='') as outcsv:
            csvwriter = csv.writer(outcsv, delimiter=';')
            csvwriter.writerow(["Markers", "LengthBasedPic", "SequenceBasedPic", "PIC SequenceBased - PIC Lengthbased"])
            for primer in primers:
                csvwriter.writerow([primer] + [rest["Markers"][primer]["LengthBased"]["PIC"]] + [rest["Markers"][primer]["AlleleBased"]["PIC"]] + [rest["Markers"][primer]["PIC SequenceBased - PIC Lengthbased"]])

    for project, rest in PIC_dict.items():
        dict_additional[project] = {}
        dict_additional[project]["Best " + str(5) + " performing markers (SequenceBased)"] = {}
        dict_additional[project]["Best " + str(5) + " performing markers (LengthBased)"] = {}

        dict_additional[project]["Highest " + str(5) + " PIC increases from LengthBased to SequenceBased"] = {}

        PIC_values = [(primer, (rest["AlleleBased"]["PIC"], rest["LengthBased"]["PIC"], rest["AlleleBased"]["PIC"]-rest["LengthBased"]["PIC"])) for primer, rest in PIC_dict[project]["Markers"].items()]
        PIC_values_sorted_sequencebased = sorted(PIC_values, key=lambda x : x[1], reverse=True)

        PIC_values = [(primer, (rest["AlleleBased"]["PIC"], rest["LengthBased"]["PIC"], rest["AlleleBased"]["PIC"]-rest["LengthBased"]["PIC"])) for primer, rest in PIC_dict[project]["Markers"].items()]
        PIC_values_sorted_lengthbased = sorted(PIC_values, key=lambda x : x[1], reverse=True)

        PIC_values_differences = [(primer, (rest["AlleleBased"]["PIC"], rest["LengthBased"]["PIC"], rest["AlleleBased"]["PIC"]-rest["LengthBased"]["PIC"])) for primer, rest in PIC_dict[project]["Markers"].items()]
        PIC_values_sorted_differences = sorted(PIC_values_differences, key=lambda x : x[1][2], reverse=True)

        for i in range(0, 5, 1):
            dict_additional[project]["Best " + str(5) + " performing markers (SequenceBased)"][PIC_values_sorted_sequencebased[i][0]] = {}
            dict_additional[project]["Best " + str(5) + " performing markers (SequenceBased)"][PIC_values_sorted_sequencebased[i][0]]["PIC Sequencebased"] = PIC_values_sorted_sequencebased[i][1][0]
            dict_additional[project]["Best " + str(5) + " performing markers (SequenceBased)"][PIC_values_sorted_sequencebased[i][0]]["PIC Lengthbased"] = PIC_values_sorted_sequencebased[i][1][1]
            dict_additional[project]["Best " + str(5) + " performing markers (SequenceBased)"][PIC_values_sorted_sequencebased[i][0]]["PIC Difference"] = PIC_values_sorted_sequencebased[i][1][2]

            dict_additional[project]["Best " + str(5) + " performing markers (LengthBased)"][PIC_values_sorted_lengthbased[i][0]] = {}
            dict_additional[project]["Best " + str(5) + " performing markers (LengthBased)"][PIC_values_sorted_lengthbased[i][0]]["PIC Sequencebased"] = PIC_values_sorted_lengthbased[i][1][0]
            dict_additional[project]["Best " + str(5) + " performing markers (LengthBased)"][PIC_values_sorted_lengthbased[i][0]]["PIC Lengthbased"] = PIC_values_sorted_lengthbased[i][1][1]
            dict_additional[project]["Best " + str(5) + " performing markers (LengthBased)"][PIC_values_sorted_lengthbased[i][0]]["PIC Difference"] = PIC_values_sorted_lengthbased[i][1][2]

            dict_additional[project]["Highest " + str(5) + " PIC increases from LengthBased to SequenceBased"][PIC_values_sorted_differences[i][0]] = {}
            dict_additional[project]["Highest " + str(5) + " PIC increases from LengthBased to SequenceBased"][PIC_values_sorted_differences[i][0]]["PIC Sequencebased"] = PIC_values_sorted_differences[i][1][0]
            dict_additional[project]["Highest " + str(5) + " PIC increases from LengthBased to SequenceBased"][PIC_values_sorted_differences[i][0]]["PIC Lengthbased"] = PIC_values_sorted_differences[i][1][1]
            dict_additional[project]["Highest " + str(5) + " PIC increases from LengthBased to SequenceBased"][PIC_values_sorted_differences[i][0]]["PIC Difference"] = PIC_values_sorted_differences[i][1][2]





    PIC_json_path = outputfolderpath / 'PIC_results.json'
    with open(PIC_json_path, 'w') as json_output:
        json.dump(PIC_dict, json_output, indent = 4)

    PIC_json_additional_path = outputfolderpath / 'PIC_additional_info.json'
    with open(PIC_json_additional_path, 'w') as json_output:
        json.dump(dict_additional, json_output, indent = 4)
    

    with open(PIC_json_path, "r") as f:
        data = json.load(f)

    with open(PIC_json_additional_path, "r") as f:
        data_best = json.load(f)
    
    for folderpath in inputfolderpath.iterdir():
        if (folderpath.is_dir()):
            project = folderpath.name

            markers = data[project]["Markers"]
            #marker_names = list(markers.keys())
            markers = data[project]["Markers"]
            marker_names = []
            for marker, rest in data[project]["Markers"].items():
                if (rest["AlleleBased"]["PIC"] == 0.0 or rest["LengthBased"]["PIC"] == 0.0):
                    continue
                marker_names.append(marker)
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
            ax.set_title(f"WAI vs AL PIC – Project {project}")
            ax.set_ylim(0, 1)
            ax.legend()

            plt.tight_layout()

            savepath = outputfolderpath / f"{project}_PIC_histogram.png"
            plt.savefig(savepath, dpi=200)
            plt.close(fig)

            print(f"Saved PIC histogram for project '{project}' to {savepath}")

    
    
    all_labels = []       
    allele_all = []
    length_all = []
    project_boundaries = []

    current_pos = 0
    for folderpath in inputfolderpath.iterdir():
        if folderpath.is_dir():
            project = folderpath.name

            markers = data[project]["Markers"]
            marker_names = []
            for marker, rest in data[project]["Markers"].items():
                if (rest["AlleleBased"]["PIC"] == 0.0 or rest["LengthBased"]["PIC"] == 0.0):
                    continue
                marker_names.append(marker)
            #marker_names = list(markers.keys())

            allele_pics = [markers[m]["AlleleBased"]["PIC"] for m in marker_names]
            length_pics = [markers[m]["LengthBased"]["PIC"] for m in marker_names]

            project_boundaries.append((current_pos, project))

            for m, a, l in zip(marker_names, allele_pics, length_pics):
                all_labels.append(f"{project} – {m}")
                allele_all.append(a)
                length_all.append(l)
                current_pos += 1

            all_labels.append("")
            allele_all.append(0)
            length_all.append(0)
            current_pos += 1

    all_labels.pop()
    allele_all.pop()
    length_all.pop()

    x = np.arange(len(all_labels))
    width = 0.4

    fig, ax = plt.subplots(figsize=(max(12, len(x) * 0.4), 6))

    ax.bar(x - width/2, allele_all, width, label="WAI PIC")
    ax.bar(x + width/2, length_all, width, label="AL PIC")

    ax.set_xticks(x)
    ax.set_xticklabels(all_labels, rotation=60, ha="right")
    ax.set_ylabel("PIC value")
    ax.set_ylim(0, 1)
    ax.set_title("WAI vs AL PIC – All Projects")
    ax.legend()

    # Add vertical separators between projects
    for pos, project in project_boundaries[1:]:
        ax.axvline(pos - 0.5, linestyle="--", linewidth=1)

    plt.tight_layout()

    savepath = outputfolderpath / "ALL_PROJECTS_PIC_histogram.png"
    plt.savefig(savepath, dpi=200)
    plt.close(fig)

    print(f"Saved combined PIC histogram to {savepath}")







    project_names = []
    allele_data = []
    length_data = []

    for folderpath in inputfolderpath.iterdir():
        if not folderpath.is_dir():
            continue

        project = folderpath.name
        markers = data[project]["Markers"]

        allele_vals = []
        length_vals = []

        for marker, rest in markers.items():
            a = rest["AlleleBased"]["PIC"]
            l = rest["LengthBased"]["PIC"]

            # Skip invalid markers
            if (a == 0.0 or l == 0.0):
                continue

            allele_vals.append(a)
            length_vals.append(l)

        # Skip empty projects
        if allele_vals:
            project_names.append(project)
            allele_data.append(allele_vals)
            length_data.append(length_vals)

    # -------------------------------------------------
    # Define x positions
    # -------------------------------------------------
    n_projects = len(project_names)
    gap = 1.6

    positions_allele = []
    positions_length = []
    project_centers = []

    current_x = 0.0
    for _ in range(n_projects):
        pos_l = current_x 
        pos_a = current_x + 0.6
        # pos_a = current_x
        # pos_l = current_x + 0.6

        positions_allele.append(pos_a)
        positions_length.append(pos_l)
        project_centers.append((pos_a + pos_l) / 2)

        current_x += gap

    fig, ax = plt.subplots(figsize=(max(10, n_projects * 2.2), 6))

    ax.boxplot(
        allele_data,
        positions=positions_allele,
        widths=0.5,
        patch_artist=True,
        showfliers=False,
        boxprops=dict(facecolor="lightblue", alpha=0.6),
        medianprops=dict(color="black"),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        zorder=2
    )

    ax.boxplot(
        length_data,
        positions=positions_length,
        widths=0.5,
        patch_artist=True,
        showfliers=False,
        boxprops=dict(facecolor="lightgreen", alpha=0.6),
        medianprops=dict(color="black"),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        zorder=2
    )

    for x, vals in zip(positions_allele, allele_data):
        ax.scatter(
            np.random.normal(x, 0.045, size=len(vals)),
            vals,
            s=25,
            alpha=0.75,
            color="tab:blue",
            zorder=3
        )

    for x, vals in zip(positions_length, length_data):
        ax.scatter(
            np.random.normal(x, 0.045, size=len(vals)),
            vals,
            s=25,
            alpha=0.75,
            color="tab:green",
            zorder=3
        )

    for i in range(1, n_projects):
        ax.axvline(
            (positions_length[i - 1] + positions_allele[i]) / 2,
            linestyle="--",
            linewidth=1,
            color="gray",
            zorder=1
        )

    ax.set_xticks(project_centers)
    ax.set_xticklabels(project_names, rotation=45, ha="right")

    ax.set_ylabel("PIC value")
    ax.set_ylim(0, 1)
    ax.set_title("WAI vs AL PIC per Project")

    legend_handles = [
        plt.Line2D([0], [0], color="lightblue", lw=8, label="WAI PIC"),
        plt.Line2D([0], [0], color="lightgreen", lw=8, label="AL PIC"),
    ]
    #ax.legend(handles=legend_handles)
    ax.legend(
        handles=legend_handles,
        loc="upper left",
        bbox_to_anchor=(0.02, 0.98)
    )

    plt.tight_layout()

    savepath = outputfolderpath / "all_projects_PIC_boxplot.png"
    plt.savefig(savepath, dpi=200)
    plt.close(fig)

    print(f"Saved combined PIC boxplot to {savepath}")














    
    # Storage for the final combined plot
    project_marker_labels = []
    diffs_all = []
    project_boundaries = []

    project_names = []
    for folderpath in inputfolderpath.iterdir():
        if folderpath.is_dir():

            project = folderpath.name
            project_names.append(project)

            # if project not in data:
            #     continue

            markers = data[project]["Markers"]
            #marker_names = list(markers.keys())

            marker_names = []
            for marker, rest in data[project]["Markers"].items():
                if (rest["PIC SequenceBased - PIC Lengthbased"] == 0.0):
                    continue
                marker_names.append(marker)

            start_idx = len(project_marker_labels)

            diffs = [markers[m]["PIC SequenceBased - PIC Lengthbased"] for m in marker_names]

            # Build labels like "Buvi – Bv1_AATA"
            for m in marker_names:
                project_marker_labels.append(f"{project} – {m}")

            diffs_all.extend(diffs)

            end_idx = len(project_marker_labels)
            project_boundaries.append((start_idx, end_idx, project))

    # # Now plot everything horizontally
    # y = np.arange(len(project_marker_labels))
    # height = 0.4  # Thickness of bars

    # fig, ax = plt.subplots(figsize=(12, max(6, len(y) * 0.4)))

    # ax.barh(y - height/2, diffs_all, height, label= "PIC-Diffs")

    # ax.set_yticks(y)
    # ax.set_yticklabels(project_marker_labels)
    # ax.set_xlabel("PIC Diff")
    # ax.set_title("Allele vs Length-based PIC for ALL Projects")
    # ax.set_xlim(0, 1)
    # ax.legend(loc="lower right")

    # plt.tight_layout()

    # savepath = outputfolderpath / "ALL_PROJECTS_PIC_horizontal.png"
    # plt.savefig(savepath, dpi=240)
    # plt.close(fig)

    # print(f"Saved combined PIC plot to {savepath}")

    # Now plot everything horizontally
    
    y = np.arange(len(project_marker_labels))
    height = 0.6  # thickness of bars

    fig, ax = plt.subplots(figsize=(12, max(6, len(y) * 0.4)))

    ax.barh(y, diffs_all, height, label="PIC (Sequence-based - Length-based)")

    # zero line to see negative vs positive
    ax.axvline(0, color="black", linewidth=1)

    # separate projects with horizontal lines / light shading
    for i, (start, end, project) in enumerate(project_boundaries):
        # light background strip per project (optional but nice)
        if i % 2 == 0:
            ax.axhspan(start - 0.5, end - 0.5, alpha=0.05)
        # separator line above each project except the first
        if i > 0:
            ax.axhline(start - 0.5, color="grey", linestyle="--", linewidth=0.7, alpha=0.7)

    ax.set_yticks(y)
    ax.set_yticklabels(project_marker_labels)
    ax.set_xlabel("PIC difference (Sequence-based - Length-based)")
    title_text = "PIC differences for Projects:"
    for i, project in enumerate(project_names,1):
        title_text += project
        if (i == len(project_names)):
            title_text += "."
        else:
             title_text += ", "
    ax.set_title(title_text)

    # x-limits symmetric around 0 so negatives show nicely
    min_diff = min(diffs_all)
    max_diff = max(diffs_all)
    max_abs = max(abs(min_diff), abs(max_diff))
    ax.set_xlim(-max_abs * 1.1, max_abs * 1.1)

    ax.legend(loc="lower right")

    plt.tight_layout()

    savepath = outputfolderpath / "ALL_PROJECTS_PIC_diffs_horizontal.png"
    plt.savefig(savepath, dpi=240)
    plt.close(fig)

    print(f"Saved combined PIC diff plot to {savepath}")






    # Storage for the final combined plot for best markers
    project_marker_labels = []
    diffs_all = []
    project_boundaries = []

    project_names = []
    for folderpath in inputfolderpath.iterdir():
        if folderpath.is_dir():
            project = folderpath.name
            project_names.append(project)

            # if project not in data:
            #     continue

            markers = data_best[project]["Highest 5 PIC increases from LengthBased to SequenceBased"]
            #marker_names = list(markers.keys())

            marker_names = []
            for marker, rest in data_best[project]["Highest 5 PIC increases from LengthBased to SequenceBased"].items():
                if (rest["PIC Difference"] == 0.0):
                    continue
                marker_names.append(marker)

            start_idx = len(project_marker_labels)

            diffs = [markers[m]["PIC Difference"] for m in marker_names]
            diffs_sorted = sorted(diffs, reverse=True)

            # Build labels like "Buvi – Bv1_AATA"
            for m in marker_names:
                project_marker_labels.append(f"{project} – {m}")

            diffs_all.extend(diffs_sorted)

            end_idx = len(project_marker_labels)
            project_boundaries.append((start_idx, end_idx, project))

    y = np.arange(len(project_marker_labels))
    height = 0.6  # thickness of bars

    fig, ax = plt.subplots(figsize=(12, max(6, len(y) * 0.4)))

    ax.barh(y, diffs_all, height, label="PIC Difference")

    # zero line to see negative vs positive
    ax.axvline(0, color="black", linewidth=1)

    # separate projects with horizontal lines / light shading
    for i, (start, end, project) in enumerate(project_boundaries):
        # light background strip per project (optional but nice)
        if i % 2 == 0:
            ax.axhspan(start - 0.5, end - 0.5, alpha=0.05)
        # separator line above each project except the first
        if i > 0:
            ax.axhline(start - 0.5, color="grey", linestyle="--", linewidth=0.7, alpha=0.7)

    ax.set_yticks(y)
    ax.set_yticklabels(project_marker_labels)
    ax.set_xlabel("PIC difference (AL - WAI)")
    title_text = "PIC differences for Projects:"
    for i, project in enumerate(project_names,1):
        title_text += project
        if (i == len(project_names)):
            title_text += "."
        else:
             title_text += ", "
    ax.set_title(title_text)

    # x-limits symmetric around 0 so negatives show nicely
    min_diff = min(diffs_all)
    max_diff = max(diffs_all)
    max_abs = max(abs(min_diff), abs(max_diff))
    ax.set_xlim(-max_abs * 1.1, max_abs * 1.1)

    ax.legend(loc="lower right")

    plt.tight_layout()

    savepath = outputfolderpath / "ALL_PROJECTS_PIC_diffs_horizontal_best.png"
    plt.savefig(savepath, dpi=240)
    plt.close(fig)

    print(f"Saved combined PIC diff plot to {savepath}")


        
            

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