# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 23:13:28 2025

@author: Sebastian
"""

import os, re, multiprocessing, subprocess
from pathlib import Path
import customtkinter as ctk

from GBAS_package_sonnenbe.helper_functions.zip_unzip_file import zip_file

def main():
    
    return 0


def checkInputDir(rawdatafolderpath : str, indexcombolist : list, indexcomboposition : int) -> dict:
    FilesData = {}
    for subdir, dirs, files in os.walk(os.path.normpath(rawdatafolderpath)): #instead of: for fastq in os.listdir(self.raw_data_dir):
        for fastq in files: 
            #print(fastq)
            indexcombo = fastq.split('_')[indexcomboposition-1]
            if indexcombo in indexcombolist:
                if (indexcombo not in FilesData.keys()):
                    FilesData[indexcombo] = []
                FilesData[indexcombo].append(os.path.normpath(subdir + "/" + fastq))
    #print(FilesData)
    return FilesData


def runTrimomatic_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict, executablesdict : dict, rawsamplenames : list, performance : bool, number_cores : int, zipping : bool):
    QC_folder = Path(paramsdict["Outputfolder"] + '/QC')
    FilesData = checkInputDir(paramsdict["Rawdata"], rawsamplenames, int(paramsdict["Indexcomboposition"]))
    textbox_pipeline.insert("end", "\nStarting Quality Trimming.\n")
    runTrimomatic(FilesData, paramsdict, executablesdict, str(QC_folder), performance, number_cores, zipping)
    textbox_pipeline.insert("end", "Finished Quality Trimming.\n")

def runTrimomatic_CLI(paramsdict : dict, executablesdict : dict, rawsamplenames : list, performance : bool, number_cores : int, zipping : bool):
    QC_folder = Path(paramsdict["Outputfolder"] + '/QC')
    FilesData = checkInputDir(paramsdict["Rawdata"], rawsamplenames, int(paramsdict["Indexcomboposition"]))
    print("\n\nStarting Quality Trimming.\n\n")
    runTrimomatic(FilesData, paramsdict, executablesdict, str(QC_folder), performance, number_cores, zipping)
    print("end", "\n\nFinished Quality Trimming.\n\n")

def runTrimomatic(FilesData : dict, paramsdict : dict, executablesdict : dict, outputpath : str, performance : bool, number_cores : int, zipping : bool):
    binpath = paramsdict["Bin"]
    try:
        if (performance):
            with multiprocessing.Pool(processes = number_cores) as pool:
                processes = []
                args_list = [(indexcombo, files, outputpath, paramsdict, executablesdict, zipping) for indexcombo, files in FilesData.items()]
                results = pool.starmap_async(trimmo_per_file, args_list) #chunksize=chunk_size
                processes = results.get()
        else:
            for indexcombo, files in FilesData.items():
                trimmo_per_file(indexcombo, files, outputpath, paramsdict, executablesdict, zipping)
    except Exception as e:
        print(f"Error when trying to run Trimmomatic ! \nException: {e} \n")



def trimmo_per_file(indexcombo : str, files : list, outputpath : str, paramsdict : dict, executablesdict : dict, zipping):
    files.sort() # get R1 and R2 list and sort them to make sure that R1 always shows first
    R1 = files[0] # get path of R1 input file
    R2 = files[1]
    outFileR1 = re.split(r'[\\/]', R1)[-1].split('.')[0]
    outFileR2 = re.split(r'[\\/]', R2)[-1].split('.')[0]

    R1paired = str(Path(outputpath + "/" + outFileR1 + "_QTpaired.fastq"))
    R1unpaired = str(Path(outputpath + "/" + outFileR1 + "_QTunpaired.fastq"))
    R2paired = str(Path(outputpath + "/" + outFileR2 + "_QTpaired.fastq"))
    R2unpaired = str(Path(outputpath + "/" + outFileR2 + "_QTunpaired.fastq"))

    binpath = paramsdict["Bin"]
    Trimmdir = str(executablesdict["Folders"]["Trimmodir"].name)
    Trimmexecutable = str(executablesdict["Files"]["Trimmomatic"].name)
    Adaptersdir = str(executablesdict["Folders"]["Adaptersdir"].name)
    Adaptersfilename = str(executablesdict["Additional"]["Adapterfile"].name)

    exe = str(Path(binpath + "/" + Trimmdir + "/" + Trimmexecutable))
    adapterpath = str(Path("bin/" + Trimmdir + "/" + Adaptersdir + "/" + Adaptersfilename))

    code = 'java -jar ' + exe + ' PE ' + R1 + ' ' + R2 + ' ' + R1paired + ' ' + R1unpaired + ' ' + R2paired + ' ' + R2unpaired + ' ILLUMINACLIP:' + adapterpath + ':2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20'
    print('running: ' + code)
    subprocess.call(code, shell=True)

    if (zipping):
        zip_file(Path(R1unpaired))
        zip_file(Path(R1paired))
        zip_file(Path(R2unpaired))
        zip_file(Path(R2paired))


if __name__ == "__main__":
    main()