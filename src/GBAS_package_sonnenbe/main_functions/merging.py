import os, re, multiprocessing, subprocess
from pathlib import Path
import customtkinter as ctk

from GBAS_package_sonnenbe.helper_functions.zip_unzip_file import zip_file, unzip_file


def main():

    return 0


def runUsearch_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict, executablesdict : dict, performance : bool, number_cores : int, zipping : bool):
    textbox_pipeline.insert("end", "Starting Merging.\n")
    QC_folder = Path(paramsdict["Outputfolder"] + '/QC')
    Usearch_folder = Path(paramsdict["Outputfolder"] + '/MergedOut')
    runUsearch(QC_folder, Usearch_folder, paramsdict, executablesdict, performance, number_cores, zipping)
    textbox_pipeline.insert("end", "Finished Merging.\n")


def runUsearch_CLI(paramsdict : dict, executablesdict : dict, performance : bool, number_cores : int, zipping : bool):
    print("\n\nStarting Merging.\n\n")
    QC_folder = Path(paramsdict["Outputfolder"] + '/QC')
    Usearch_folder = Path(paramsdict["Outputfolder"] + '/MergedOut')
    runUsearch(QC_folder, Usearch_folder, paramsdict, executablesdict, performance, number_cores, zipping)
    print("\n\nFinished Merging.\n\n")

def runUsearch(QCfolderpath : Path, MergedOutfolderpath : Path, paramsdict : dict, executablesdict : dict, performance : bool, number_cores : int, zipping : bool):
        try:
            if (performance):
                with multiprocessing.Pool(processes = number_cores) as pool:
                    processes = []
                    args_list = [(filepath, QCfolderpath, MergedOutfolderpath, paramsdict, executablesdict, zipping) for filepath in QCfolderpath.iterdir()]
                    results = pool.starmap_async(usearch_per_file, args_list)
                    processes = results.get()
            else:
                for filepath in QCfolderpath.iterdir():
                    usearch_per_file(filepath, QCfolderpath, MergedOutfolderpath, paramsdict, executablesdict, zipping)
        except Exception as e:
            print(f"Error when trying to run Usearch ! \nException: {e} \n")


def usearch_per_file(file : Path, QCfolderpath : Path, MergedOutfolderpath : str, paramsdict : dict, executablesdict : dict, zipping : bool):
    if (zipping):
        unzip_file(file)
    if file.name.endswith("QTpaired.fastq") and "R1" in file.name:
    #if file.endswith('QTpaired.fastq') and "R1" in file:
        R1 = str(QCfolderpath / file.name)
        R2 = str(Path(R1.replace("_R1_", "_R2_")))
        # R1 = str(Path(QCfolderpath + '/' + file)) # get path of R1 input file
        # R2 = R1.replace("_R1_", "_R2_") # get path of R2 input file
        #out = str(Path(MergedOutfolderpath + '/' + file.split('_')[int(paramsdict["Indexcomboposition"])-1] + '_joined.fastq')) # get path of file to save merge reads
        out = str(MergedOutfolderpath / (file.name.split('_')[int(paramsdict["Indexcomboposition"]) - 1] + "_joined.fastq")) # get path of file to save merge reads
        #exe = str(Path(paramsdict["Bin"] + '/' + os.path.basename(os.path.normpath(executablesdict["Files"]["UsearchWindows"]))))
        if (paramsdict["Operatingsystem"].lower() == "windows"):
            exe = str(Path(executablesdict["Files"]["UsearchWindows"]))
        else:
            exe = str(Path(executablesdict["Files"]["UsearchLinux"]))
        code = exe + ' -fastq_mergepairs ' + R1 + ' -reverse ' + R2 + ' -fastqout ' + out + ' -fastq_pctid 80 -fastq_maxdiffs 40'
        print('running: ' + code) # print code
        subprocess.call(code, shell=True)

        if (zipping):
            zip_file(Path(R1))
            zip_file(Path(R2))
            zip_file(Path(out))


if __name__ == "__main__":
    main()