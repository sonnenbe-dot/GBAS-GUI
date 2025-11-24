import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.messagebox, os, platform, json
import customtkinter as ctk
from pathlib import Path

from GBAS_package_sonnenbe.helper_functions.parse_samplefile import get_samples
from GBAS_package_sonnenbe.helper_functions.parse_primerfile import get_primers
from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import is_valid
from GBAS_package_sonnenbe.helper_functions.parse_executables import check_executables
from GBAS_package_sonnenbe.helper_functions.parse_rawdata import get_rawdata
from GBAS_package_sonnenbe.helper_functions.parse_samplefile import get_samples, get_samples_duplicates, get_rawsamples_list
from GBAS_package_sonnenbe.helper_functions.get_combatibility import samples_to_process
from GBAS_package_sonnenbe.helper_functions.parse_primerfile import get_primers

def main():


    return 0



def status_window(topwindow : tk, paramsdict : dict, executables_dict : dict, params_list : list, list_not_mandatory : list, list_mandatory : list, on_done):
    new_window = tk.Toplevel(topwindow)
    new_window.title("Workspace Status")
    new_window.geometry(f"{1400}x{700}")
    new_window.focus_set()


    text_widget = tk.Text(new_window, wrap=tk.WORD, height=20, width=50, font=("Helvetica", 18))
    scrollbar = tk.Scrollbar(new_window, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
        
    #text_widget.insert(tk.END, long_text)
    #text_widget.grid(0, 0, fill=tk.BOTH, expand=True, padx=20, pady=20)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget.tag_config("bold", font=("Helvetica", 18, "bold"))


    long_text = ""
    long_text += "\n\n"
    long_text += "Operating System" + " : " + str(paramsdict["Operatingsystem"].lower()) + "\n\n"
    long_text += "\n\nBin Folderpath: \n\n"
    long_text += "Bin: " + str(paramsdict["Bin"]) + "\n"

    long_text += "\n\nPath to all external executables: \n\n"
    flag = check_executables(executables_dict)
    for key, value in executables_dict["Files"].items():
        long_text += str(key) + ": \t " + str(value) + "\n"
    for key, value in executables_dict["Additional"].items():
        long_text += str(key) + ": \t " + str(value) + "\n"
    if (is_valid(str(paramsdict["Bin"])) and flag):
        long_text += "\nExecutables correctly set! \n\n"
    else:
        long_text += "\nExecutables not correctly set or missing! \n\n"
    
    long_text += "\n\nMandatory input filepaths: \n\n"
    inputs_mandatory_flag = True
    inputs_non_mandatory_flag = True
    for param in list_mandatory:
        long_text += param + " : " + str(paramsdict[param]) + "\n\n"
        if (not(is_valid(str(paramsdict[param])))):
            print(param)
            inputs_mandatory_flag = False
    long_text += "\n\nNon-Mandatory input filepaths: \n\n"
    for param in list_not_mandatory:
        long_text += param + " : " + str(paramsdict[param]) + "\n\n"
        if (not(is_valid(str(paramsdict[param])))):
            inputs_non_mandatory_flag = False
    
    text_widget.insert("end", long_text)

    if (inputs_mandatory_flag):
        text_widget.insert("end", "\n Mandatory Inputfiles correctly set! \n\n", "bold")
    else:
        text_widget.insert("end", "\n Mandatory Inputfiles NOT correctly set! \n\n", "bold")

    if (inputs_non_mandatory_flag):
        text_widget.insert("end", "\n Non-Mandatory Inputfiles correctly set! \n\n")
    else:
        text_widget.insert("end", "\n Non-Mandatory Inputfiles not correctly set! \n\n")


    if (inputs_mandatory_flag):

        flag_duplicate = False
        rawfile_dict, rawfile_number = get_rawdata(paramsdict["Rawdata"], paramsdict["Indexcomboposition"])
        text_widget.insert("end", "\n\n Rawdatafolder contains " + str(rawfile_number) + " files. \n")
        text_widget.insert("end", "\n Rawdatafolder contains " + str(len(rawfile_dict)) + " samples. \n\n")
        text_widget.insert("end", "\n Each sample must contain only 2 files (Forward and Reverse) : ")
        #print(rawfile_dict)
        duplicate_rawsamples = [key for key, count in rawfile_dict.items() if (count > 2)]
        if (not(duplicate_rawsamples)):
            text_widget.insert("end", "Correct! \n\n\n", "bold")
        else:
            flag_duplicate = True
            text_widget.insert("end", "Not Correct! \n\n", "bold")
            text_widget.insert("end", "There are duplicate samples in rawdata folder: \n")
            for duplicate_rawsample in duplicate_rawsamples:
                text_widget.insert("end", duplicate_rawsample + "\n")
            text_widget.insert("end", "\n\n")

        
        samples_dict, number_lines = get_samples(paramsdict["Samplefile"])
        samplesleft_dict, samplesright_dict = get_samples_duplicates(samples_dict)
        text_widget.insert("end", "\n\n Samplefile contains " + str(number_lines) + " lines. \n")
        text_widget.insert("end", "\n\n Samplefile contains " + str(len(samples_dict["forward"])) + " unique raw samplenames on left column . \n")
        text_widget.insert("end", "\n\n Samplefile contains " + str(len(samples_dict["reverse"])) + " unique new samplenames on right column . \n")
        text_widget.insert("end", "\n\n Samplefile must not contain duplicate names: ")
        duplicate_samplesleft = [key for key, count in samplesleft_dict.items() if (count > 1)]
        duplicate_samplesright = [key for key, count in samplesright_dict.items() if (count > 1)]
        if (not(duplicate_samplesleft) and not(duplicate_samplesright)):
            text_widget.insert("end", "Correct! \n\n\n", "bold")
        else:
            flag_duplicate = True
            text_widget.insert("end", "Not Correct! \n\n", "bold")
            text_widget.insert("end", "There are duplicate samplenames in samplefile: \n")
            for duplicate_sample in duplicate_samplesleft:
                text_widget.insert("end", duplicate_sample + " appears " + str(samplesleft_dict[duplicate_sample]) + " times. \n")
            for duplicate_sample in duplicate_samplesright:
                text_widget.insert("end", duplicate_sample + " appears " + str(samplesright_dict[duplicate_sample]) + " times. \n")
            text_widget.insert("end", "\n\n")
        
        if (not(flag_duplicate)):
            text_widget.insert("end", "\n\n Based on the samplefile and the files in rawdata folder we will be able to process ")
            rawfilenames = [key for key, count in rawfile_dict.items()]
            #samplenames_old = [key for key, count in samples_dict["forward"].items()]
            samplenames_old = get_rawsamples_list(samples_dict)
            #print(rawfilenames)
            number = samples_to_process(rawfilenames, samplenames_old)
            text_widget.insert("end", str(number), "bold")
            text_widget.insert("end", " files from the rawdata folder! \n\n\n")
        
        primers_flag = True
        primers_dict = get_primers(paramsdict["Primerfile"])
        text_widget.insert("end", "\n\n Primerfile contains " + str(len(primers_dict["primers"])) + " primers. \n\n")
        if (not(primers_dict["primers"])):
            text_widget.insert("end", "\n\n Primerfile contains no primers and pipeline cannot process anything! \n\n")
        if (primers_dict["primersboundaries"]):
            text_widget.insert("end", "\n\n Primerfile also contains primers with set length boundaries: \n")
            for primer, boundaries in primers_dict["primersboundaries"].items():
                text_widget.insert("end", "\n" + primer + ": " + str(boundaries) + " : \n")
        
        if (not(flag_duplicate) and not(primers_flag)):
            text_widget.insert("end", "\n\n\n Pipeline is ")
            text_widget.insert("end", "Not Ready ", "bold")
            text_widget.insert("end", "to start due to above issues! \n\n\n")
        else:
            text_widget.insert("end", "\n\n\n Pipeline is ")
            text_widget.insert("end", "Ready ", "bold")
            text_widget.insert("end", "to start! \n\n\n")

        

    else:
         text_widget.insert("end", "\n\n\n Pipeline is ")
         text_widget.insert("end", "Not Ready ", "bold")
         text_widget.insert("end", "to start due to above issues! \n\n\n")
    





    # for param in params_list:
    #     if (param == "Operatingsystem"):
    #         long_text += param + " : " + str(paramsdict[param].lower()) + "\n\n"
    #         continue
    #     if (param in list_mandatory):
    #         long_text += param + " : " + str(paramsdict[param]) + "\n\n"
    #         if (not(is_valid(str(paramsdict[param])))):
    #             inputs_flag = False
    #     elif (param in list_not_mandatory):
    #         long_text += param + " : " + str(paramsdict[param]) + "\n\n"


        
    # for key, value in executables_dict.items():
    #     if (key != "Trimmodir" or key != "" or key != "Adaptersdir"):
    #         long_text += str(key) + ": \t " + str(value) + "\n"
    # print(is_valid(str(paramsdict["Bin"])))
    # print(flag_executables)
    

    # text_widget = tk.Text(new_window, wrap=tk.WORD, height=20, width=50, font=("Helvetica", 18))
    # scrollbar = tk.Scrollbar(new_window, command=text_widget.yview)
    # text_widget.config(yscrollcommand=scrollbar.set)
        
    # text_widget.insert(tk.END, long_text)
    # #text_widget.grid(0, 0, fill=tk.BOTH, expand=True, padx=20, pady=20)
    # text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
    # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    #new_window.bind('<Return>', lambda event: new_window.destroy())

    # new_window.protocol("WM_DELETE_WINDOW", closing(new_window, on_done))
    # new_window.bind('<Return>', lambda event: closing(new_window, on_done))

    new_window.protocol("WM_DELETE_WINDOW", lambda: closing(new_window, on_done))
    new_window.bind("<Return>", lambda e: closing(new_window, on_done))
    
def closing(new_window, on_done):
    try:
        on_done("Pipeline has not started:")
    finally:
        new_window.destroy()