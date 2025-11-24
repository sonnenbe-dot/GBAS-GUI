# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 00:33:01 2025

@author: Sebastian
"""

import os, multiprocessing
from pathlib import Path
import customtkinter as ctk

from GBAS_package_sonnenbe.helper_functions.parse_fastq import parse_fastq
from GBAS_package_sonnenbe.helper_functions.calc_helpers import rev_comp, mismatch

def main():
    
    return 0


def runDemultiplexing_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict, primersdict : dict, samplesdict : dict, performance : bool, number_cores : int):
    usearchoutput_path = Path(paramsdict["Outputfolder"] + '/MergedOut')
    separatout_path = Path(paramsdict["Outputfolder"] + '/SeparatOut')
    textbox_pipeline.insert('end-1c', "\nStarting Demultiplexing! \n")
    runDemultiplexing(usearchoutput_path, separatout_path, primersdict, samplesdict, int(paramsdict["Maxmismatch"]), int(paramsdict["Minlength"]), int(paramsdict["Indexcomboposition"]), performance, number_cores)
    textbox_pipeline.insert('end-1c', "\nFinished Demultiplexing! \n")

def runDemultiplexing(MergedOutfolderpath : Path, Separatoutfolderpath : Path, primerdict : dict, sampledict : dict, maxmismatch : int, minlength : int, indexcomboposition : int, performance : bool, number_cores : int):
    try:
        if (performance):
            with multiprocessing.Pool(processes = number_cores) as pool:
                processes = []
                args_list = [(fastqfile, MergedOutfolderpath, Separatoutfolderpath, primerdict, sampledict, maxmismatch, minlength, indexcomboposition) for fastqfile in MergedOutfolderpath.iterdir()]
                results = pool.starmap_async(demultiplex_per_file, args_list)
                processes = results.get()
        else:
            for fastqfile in MergedOutfolderpath.iterdir():
                demultiplex_per_file(fastqfile, MergedOutfolderpath, Separatoutfolderpath, primerdict, sampledict, maxmismatch, minlength, indexcomboposition)
    except Exception as e:
            print(f"Error when trying to run Demultiplexing ! \nException: {e} \n")

def demultiplex_per_file(fastqfile : Path, MergedOutfolderpath : Path, Separatoutfolderpath : Path, primerdict : dict, sampledict : dict, maxmismatch : int, minlength : int, indexcomboposition : int):
    indexcombo = fastqfile.name.split("_")[indexcomboposition-1]
    samplenew = sampledict["forward"][indexcombo]
    print('processing sample ' + samplenew + ' (old name: ' + str(indexcombo) + ') ...')
    for locus, primers in primerdict["primers"].items():
        primerF = primers[0]
        primerR = rev_comp(primers[1])
        print('processing primer '+ locus)
        out = Path(Separatoutfolderpath / (samplenew + '_' + locus + '.fasta'))
        fastq_path = Path(MergedOutfolderpath / fastqfile)
        with open(out, "w") as outputfile:
            for header, data in parse_fastq(fastq_path).items():
                sequence = data["sequence"]
                motifF=str(sequence[:len(primerF)])
                motifR=str(sequence[-len(primerR):])
                flag = False
                if (motifF == primerF and motifR == primerR):
                    flag = True
                elif (motifF == primerF and int(mismatch(motifR, primerR)) <= int(maxmismatch)):
                    flag = True
                elif (int(mismatch(motifF, primerF)) <= int(maxmismatch) and motifR == primerR):
                    flag = True
                elif int(mismatch(motifF, primerF)) <= int(maxmismatch) and int(mismatch(motifR, primerR)) <= int(maxmismatch):
                    flag = True
                if (flag):
                    if (locus in primerdict["primersboundaries"]):
                        for boundary in primerdict["primersboundaries"][locus]:
                            if (len(sequence) >= boundary[0] and len(sequence) <= boundary[1]):
                                outputfile.write('>' + header[1:] + '\n' + sequence + '\n')
                                break
                    elif (len(sequence) >= int(minlength)):
                        outputfile.write('>' + header[1:] + '\n' + sequence + '\n')






if __name__ == "__main__":
    main()