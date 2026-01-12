# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 00:33:01 2025

@author: Sebastian
"""

import os, multiprocessing
from pathlib import Path
import customtkinter as ctk
import numpy as np

from GBAS_package_sonnenbe.helper_functions.parse_fastq import parse_fastq
from GBAS_package_sonnenbe.helper_functions.calc_helpers import rev_comp, mismatch, mismatch_binary

def main():
    
    return 0


def runDemultiplexing_GUI(textbox_pipeline : ctk.CTkTextbox, paramsdict : dict, primersdict : dict, samplesdict : dict, performance : bool, number_cores : int):
    usearchoutput_path = Path(paramsdict["Outputfolder"] + '/MergedOut')
    separatout_path = Path(paramsdict["Outputfolder"] + '/SeparatOut')
    textbox_pipeline.insert('end-1c', "\nStarting Demultiplexing! \n")
    runDemultiplexing(usearchoutput_path, separatout_path, primersdict, samplesdict, int(paramsdict["Maxmismatch"]), int(paramsdict["Minlength"]), int(paramsdict["Indexcomboposition"]), performance, number_cores)
    textbox_pipeline.insert('end-1c', "\nFinished Demultiplexing! \n")


def runDemultiplexing_CLI(paramsdict : dict, primersdict : dict, samplesdict : dict, performance : bool, number_cores : int):
    usearchoutput_path = Path(paramsdict["Outputfolder"] + '/MergedOut')
    separatout_path = Path(paramsdict["Outputfolder"] + '/SeparatOut')
    print("\n\nStarting Demultiplexing! \n\n")
    runDemultiplexing(usearchoutput_path, separatout_path, primersdict, samplesdict, int(paramsdict["Maxmismatch"]), int(paramsdict["Minlength"]), int(paramsdict["Indexcomboposition"]), performance, number_cores)
    print("\n\nFinished Demultiplexing! \n\n")

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
    if (indexcombo in sampledict["forward"]):
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








dna_lookup = np.zeros(128, dtype=np.uint8)

# Standard Bases
dna_lookup[ord('A')] = 1; dna_lookup[ord('C')] = 2
dna_lookup[ord('G')] = 4; dna_lookup[ord('T')] = 8
dna_lookup[ord('-')] = 16 

# Ambiguous Bases (Sum of their parts)
dna_lookup[ord('R')] = 1 | 4         # A or G
dna_lookup[ord('Y')] = 2 | 8         # C or T
dna_lookup[ord('S')] = 2 | 4         # G or C
dna_lookup[ord('W')] = 1 | 8         # A or T
dna_lookup[ord('K')] = 4 | 8         # G or T
dna_lookup[ord('M')] = 1 | 2         # A or C
dna_lookup[ord('B')] = 2 | 4 | 8     # Not A
dna_lookup[ord('D')] = 1 | 4 | 8     # Not C
dna_lookup[ord('H')] = 1 | 2 | 8     # Not G
dna_lookup[ord('V')] = 1 | 2 | 4     # Not T
dna_lookup[ord('N')] = 15            # Any
dna_lookup[ord('I')] = 15            # Inosine -> Any




def demultiplex_per_file_binary(fastqfile : Path, MergedOutfolderpath : Path, Separatoutfolderpath : Path, primerdict : dict, sampledict : dict, maxmismatch : int, minlength : int, indexcomboposition : int):
    indexcombo = fastqfile.name.split("_")[indexcomboposition-1]
    if (not(indexcombo in sampledict["forward"])):
        return
    
    samplenew = sampledict["forward"][indexcombo]
    print('processing sample ' + samplenew + ' (old name: ' + str(indexcombo) + ') ...')
    fastq_path = Path(MergedOutfolderpath / fastqfile)

    open_file_handles = {}

    for header, data in parse_fastq(fastq_path).items():
        sequence = data["sequence"]
        for locus, primers in primerdict["primers"].items():
            primerF = primers[0]
            primerR = rev_comp(primers[1])
            #print('processing primer '+ locus)
            out = Path(Separatoutfolderpath / (samplenew + '_' + locus + '.fasta'))

            motifF=str(sequence[:len(primerF)])
            motifR=str(sequence[-len(primerR):])

            pass_check = False

            if mismatch_binary(motifF, primerF, dna_lookup) > int(maxmismatch):
                continue 
            if mismatch_binary(motifR, primerR, dna_lookup) > int(maxmismatch):
                continue
            
            if (locus in primerdict["primersboundaries"]):
                for boundary in primerdict["primersboundaries"][locus]:
                    if (len(sequence) >= boundary[0] and len(sequence) <= boundary[1]):
                        pass_check = True
                        #outputfile.write('>' + header[1:] + '\n' + sequence + '\n')
                        break
            elif (len(sequence) >= int(minlength)):
                #outputfile.write('>' + header[1:] + '\n' + sequence + '\n')
                pass_check = True
            
            if (not pass_check):
                continue
            
            if locus not in open_file_handles:
                out_path = Separatoutfolderpath / (samplenew + '_' + locus + '.fasta')
                open_file_handles[locus] = open(out_path, "w")
                
                # Write immediately to the open file
            open_file_handles[locus].write('>' + header[1:] + '\n' + sequence + '\n')

    
    for f in open_file_handles.values():
        f.close()

            # with open(out, "w") as outputfile:
            #     flag = False
            #     if (motifF == primerF and motifR == primerR):
            #         flag = True
            #     elif (motifF == primerF and int(mismatch_binary(motifR, primerR, dna_lookup)) <= int(maxmismatch)):
            #         flag = True
            #     elif (int(mismatch_binary(motifF, primerF, dna_lookup)) <= int(maxmismatch) and motifR == primerR):
            #         flag = True
            #     elif int(mismatch_binary(motifF, primerF, dna_lookup)) <= int(maxmismatch) and int(mismatch_binary(motifR, primerR, dna_lookup)) <= int(maxmismatch):
            #         flag = True
            #     if (flag):
            #         if (locus in primerdict["primersboundaries"]):
            #             for boundary in primerdict["primersboundaries"][locus]:
            #                 if (len(sequence) >= boundary[0] and len(sequence) <= boundary[1]):
            #                     outputfile.write('>' + header[1:] + '\n' + sequence + '\n')
            #                     break
            #         elif (len(sequence) >= int(minlength)):
            #             outputfile.write('>' + header[1:] + '\n' + sequence + '\n')






def demultiplex_per_file_binary1(fastqfile : Path, MergedOutfolderpath : Path, Separatoutfolderpath : Path, primerdict : dict, sampledict : dict, maxmismatch : int, minlength : int, indexcomboposition : int):
    indexcombo = fastqfile.name.split("_")[indexcomboposition-1]
    if (indexcombo in sampledict["forward"]):
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
                    elif (motifF == primerF and int(mismatch_binary(motifR, primerR, dna_lookup)) <= int(maxmismatch)):
                        flag = True
                    elif (int(mismatch_binary(motifF, primerF, dna_lookup)) <= int(maxmismatch) and motifR == primerR):
                        flag = True
                    elif int(mismatch_binary(motifF, primerF, dna_lookup)) <= int(maxmismatch) and int(mismatch_binary(motifR, primerR, dna_lookup)) <= int(maxmismatch):
                        flag = True
                    if (flag):
                        if (locus in primerdict["primersboundaries"]):
                            for boundary in primerdict["primersboundaries"][locus]:
                                if (len(sequence) >= boundary[0] and len(sequence) <= boundary[1]):
                                    outputfile.write('>' + header[1:] + '\n' + sequence + '\n')
                                    break
                        elif (len(sequence) >= int(minlength)):
                            outputfile.write('>' + header[1:] + '\n' + sequence + '\n')




def demultiplex_per_file_binary2(fastqfile : Path, MergedOutfolderpath : Path, Separatoutfolderpath : Path, primerdict : dict, sampledict : dict, maxmismatch : int, minlength : int, indexcomboposition : int):
    indexcombo = fastqfile.name.split("_")[indexcomboposition-1]

    fastq_path = MergedOutfolderpath / fastqfile
    all_headers = []
    all_seqs = []
    
    # Assuming parse_fastq returns {header: {sequence: "ATCG"}}
    # We pre-filter by global minlength to save RAM
    for h, d in parse_fastq(fastq_path).items():
        if len(d["sequence"]) >= int(minlength):
            all_headers.append(h)
            all_seqs.append(d["sequence"])
    
    for locus, primers in primerdict["primers"].items():
        primerF = primers[0]
        primerR = rev_comp(primers[1])
        
        lenF = len(primerF)
        lenR = len(primerR)


    if (indexcombo in sampledict["forward"]):
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