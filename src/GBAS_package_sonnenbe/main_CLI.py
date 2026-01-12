import os, argparse, json, re, shutil
from pathlib import Path
import platform, threading, multiprocessing, time, subprocess
import psutil
from typing import Tuple

from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import parse_parameterfile, check_paramsdict, new_paramsdict
from GBAS_package_sonnenbe.helper_functions.input_checks import check_inputs

from GBAS_package_sonnenbe.helper_functions.parse_samplefile import get_samples, get_rawsamples_list #get_bin_executables
from GBAS_package_sonnenbe.helper_functions.make_outputs import make_output_folders
from GBAS_package_sonnenbe.helper_functions.parse_primerfile import get_primers
from GBAS_package_sonnenbe.helper_functions.timer_class import Timer

from GBAS_package_sonnenbe.main_functions.trimmomatic import runTrimomatic_CLI
from GBAS_package_sonnenbe.main_functions.merging import runUsearch_CLI
from GBAS_package_sonnenbe.main_functions.demultiplexing import runDemultiplexing_CLI
from GBAS_package_sonnenbe.main_functions.markerstatistics import runLengthstatistics_CLI
from GBAS_package_sonnenbe.main_functions.markerplots import runMarkerplots_CLI

from GBAS_package_sonnenbe.main_functions.extract_lengths import run_Length_Extraction_CLI
from GBAS_package_sonnenbe.main_functions.consensus_all import RunConsensusAll_CLI
from GBAS_package_sonnenbe.main_functions.allele_determination import RunVariants_Determination_CLI
from GBAS_package_sonnenbe.main_functions.allele_calling import run_Allele_Call_CLI

def main():

    ###Testing on Spruce subset###

    # current_workspace = Path.cwd()
    
    # test_workspace = current_workspace / ("testfolder"/"spruce_test")

    # parameters = [("Outputfolder", str(test_workspace / "output")), ("Bin", str(current_workspace / "bin")), ("Rawdata", str(test_workspace / ("inputs/rawdata"))), ("Primerfile", str(test_workspace / ("inputs/primers_EPIC_and_SSR.txt"))), ("Samplefile", str(test_workspace / ("inputs/samplesheet.txt"))), ("Metadata", str(test_workspace / ("inputs/metadata.xlsx"))), ("Allelelist", "None"), ("Database", "database.db"), ("Maxmismatch", 2), ("Mincount", 20), ("Minlength", 290), ("Consensusthreshold", 0.7), ("Lengthwindow", "310, 600"), ("Filtering", 0.8), ("Ploidy", "diploid"), ("Operatingsystem", platform.system()), ("Uniqueidentifier", "default"), ("Indexcomboposition", 1), ("NumberCores", multiprocessing.cpu_count()-1)]
    # parameters_list = ["Outputfolder", "Bin", "Rawdata", "Primerfile", "Samplefile", "Metadata", "Allelelist", "Database", "Maxmismatch", "Mincount", "Minlength", "Consensusthreshold", "Lengthwindow", "Filtering", "Ploidy", "Operatingsystem", "Uniqueidentifier", "Indexcomboposition", "NumberCores"]


    # check_params = check_paramsdict(self.paramsdict, self.parameters_list)

    return 0



def prepare_params(parameters : list, parameters_list : list) -> Tuple[bool, dict]:
    params_dict = new_paramsdict(parameters)
    check_params = check_paramsdict(params_dict, parameters_list)
    return check_params, params_dict

def prepare_executables(paramsdict : dict) -> dict:
    executablesdict = {
            "Folders" : {
                "Trimmodir" : Path(Path(paramsdict["Bin"]) / "Trimmomatic-0.39"),
                "Adaptersdir" : Path(Path(paramsdict["Bin"]) / "Trimmomatic-0.39" / "adapters")
            },
            "Files" : {
                "Trimmomatic" : Path(Path(paramsdict["Bin"]) / "Trimmomatic-0.39" / "trimmomatic-0.39.jar"),
                "UsearchLinux" : Path(Path(paramsdict["Bin"]) / "usearch11.0.667_i86linux32"),
                "UsearchWindows" : Path(Path(paramsdict["Bin"]) / "usearch11.0.667_win32.exe")
            },
            "Additional" : {
                "Adapterfile" : Path(Path(paramsdict["Bin"]) / "Trimmomatic-0.39" / "adapters" / "TrueSeqAdaptersInUsage.fa")
            }
    }
    return executablesdict


def run_GBAS_CLI(paramsdict : dict, executablesdict, parameters_list, list_mandatory, performance, zipping):

    try:
        flag_inputs = check_inputs(paramsdict, executablesdict, parameters_list, list_mandatory)
    except Exception as e:
        flag_inputs = False
        print(f"Error when parsing inputs for the check:\n{e}\n")
    
    samples_dict, number_lines = get_samples(paramsdict["Samplefile"])
    rawsamplenames = get_rawsamples_list(samples_dict)
    primers_dict = get_primers(paramsdict["Primerfile"])
    logs = {"Parallel" : performance,
            "NumberCores" : paramsdict["NumberCores"],
            "QualityTrimmimg" : {},
            "Merging" : {},
            "Demultiplexing" : {},
            "LengthCounts" : {},
            "Markerplots" : {},
            "ConsensusSeqs" : {},
            "NCorrection" : {},
            "AlleleCall" : {},
            "RamUsage" : {},
            "Total" : {}
    }

    outputfolders_list1 = ['QC', 'SeparatOut', 'MergedOut', 'MarkerStatistics', 'MarkerStatisticsDuplicates',  'AlleleLenghtCounts', 'MarkerPlots', 'Markerplots_dupl']
    outputfolders_list2 = ['AllelesOut', 'ConsensusOut', 'ConsensusTogether', 'Corrected', 'AlleleCall', 'AdditionalInfo']

    make_output_folders(Path(paramsdict["Outputfolder"]), outputfolders_list1)

    t = Timer()



    runTrimomatic_CLI(paramsdict, executablesdict, rawsamplenames, performance, int(paramsdict["NumberCores"]), zipping)
    logs["QualityTrimmimg"]["Time"] = t.lap()
    print(f"\nTime spent: {logs['QualityTrimmimg']['Time']:.4g}.\n")

    runUsearch_CLI(paramsdict, executablesdict, performance, int(paramsdict["NumberCores"]), zipping)
    logs["Merging"]["Time"] = t.lap()
    print("end", "\nTime spent: " + str(logs['Merging']['Time']) + ".\n")

    runDemultiplexing_CLI(paramsdict, primers_dict, samples_dict, performance, int(paramsdict["NumberCores"]))
    logs["Demultiplexing"]["Time"] = t.lap()
    print("\nTime spent: " + str(logs['Demultiplexing']['Time']) + ".\n")

    runLengthstatistics_CLI(paramsdict, primers_dict, performance, int(paramsdict["NumberCores"]))
    logs["LengthCounts"]["Time"] = t.lap()
    print("\nTime spent: " + str(logs['LengthCounts']['Time']) + ".\n")

    runMarkerplots_CLI(paramsdict, primers_dict, samples_dict, float(paramsdict["Filtering"]))
    logs["Markerplots"]["Time"] = t.lap()
    print("\nTime spent: " + str(logs['Markerplots']['Time']) + ".\n")

        


    print('end-1c', "\n\nTotal Time spent: " + str(t.total()) + "s \n\n")
    logs["Total"]["Time"] = t.total()

    logs_path = Path(paramsdict["Outputfolder"]) / "logs_script1.json"
    with open(logs_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)




def run_GBAS_CLI_memory_part1(paramsdict: dict, executablesdict, parameters_list, list_mandatory, performance, zipping):

    try:
        flag_inputs = check_inputs(paramsdict, executablesdict, parameters_list, list_mandatory)
    except Exception as e:
        flag_inputs = False
        print(f"Error when parsing inputs for the check:\n{e}\n")
    
    samples_dict, number_lines = get_samples(paramsdict["Samplefile"])
    rawsamplenames = get_rawsamples_list(samples_dict)
    primers_dict = get_primers(paramsdict["Primerfile"])
    
    # Initializing Logs
    logs = {
        "Parallel": performance,
        "NumberCores": paramsdict["NumberCores"],
        "QualityTrimmimg": {},
        "Merging": {},
        "Demultiplexing": {},
        "LengthCounts": {},
        "Markerplots": {},
        "LengthExtraction" : {},
        "ConsensusSeqs": {},
        "NCorrection": {},
        "AlleleCall": {},
        "RamUsage": {}, # You can store total script max here if desired
        "Total": {}
    }

    outputfolders_list1 = ['QC', 'SeparatOut', 'MergedOut', 'MarkerStatistics', 'MarkerStatisticsDuplicates',  'AlleleLenghtCounts', 'MarkerPlots', 'Markerplots_dupl']
    outputfolders_list2 = ['AllelesOut', 'ConsensusOut', 'ConsensusTogether', 'Corrected', 'AlleleCall', 'AdditionalInfo']

    make_output_folders(Path(paramsdict["Outputfolder"]), outputfolders_list1)

    t = Timer()

    # --- Step 1: Quality Trimming ---
    print("Starting Quality Trimming...")
    with PeakMemoryTracker() as mem:
        runTrimomatic_CLI(paramsdict, executablesdict, rawsamplenames, performance, int(paramsdict["NumberCores"]), zipping)
        logs["QualityTrimmimg"]["RamUsage_MB"] = round(mem.max_mem_mb, 2)
        
    logs["QualityTrimmimg"]["Time"] = t.lap()
    print(f"Time spent: {logs['QualityTrimmimg']['Time']:.4g}s. Max RAM: {logs['QualityTrimmimg']['RamUsage_MB']} MB\n")

    # --- Step 2: Merging (Usearch) ---
    print("Starting Merging...")
    with PeakMemoryTracker() as mem:
        runUsearch_CLI(paramsdict, executablesdict, performance, int(paramsdict["NumberCores"]), zipping)
        logs["Merging"]["RamUsage_MB"] = round(mem.max_mem_mb, 2)

    logs["Merging"]["Time"] = t.lap()
    print(f"Time spent: {logs['Merging']['Time']}s. Max RAM: {logs['Merging']['RamUsage_MB']} MB\n")

    # --- Step 3: Demultiplexing ---
    print("Starting Demultiplexing...")
    with PeakMemoryTracker() as mem:
        runDemultiplexing_CLI(paramsdict, primers_dict, samples_dict, performance, int(paramsdict["NumberCores"]))
        logs["Demultiplexing"]["RamUsage_MB"] = round(mem.max_mem_mb, 2)

    logs["Demultiplexing"]["Time"] = t.lap()
    print(f"Time spent: {logs['Demultiplexing']['Time']}s. Max RAM: {logs['Demultiplexing']['RamUsage_MB']} MB\n")

    # --- Step 4: Length Statistics ---
    print("Starting Length Statistics...")
    with PeakMemoryTracker() as mem:
        runLengthstatistics_CLI(paramsdict, primers_dict, performance, int(paramsdict["NumberCores"]))
        logs["LengthCounts"]["RamUsage_MB"] = round(mem.max_mem_mb, 2)

    logs["LengthCounts"]["Time"] = t.lap()
    print(f"Time spent: {logs['LengthCounts']['Time']}s. Max RAM: {logs['LengthCounts']['RamUsage_MB']} MB\n")

    # --- Step 5: Marker Plots ---
    print("Starting Marker Plots...")
    with PeakMemoryTracker() as mem:
        runMarkerplots_CLI(paramsdict, primers_dict, samples_dict, float(paramsdict["Filtering"]))
        logs["Markerplots"]["RamUsage_MB"] = round(mem.max_mem_mb, 2)

    logs["Markerplots"]["Time"] = t.lap()
    print(f"Time spent: {logs['Markerplots']['Time']}s. Max RAM: {logs['Markerplots']['RamUsage_MB']} MB\n")

    # --- Finalizing ---
    total_time = t.total()
    print('end-1c', f"\n\nTotal Time spent: {total_time}s \n\n")
    logs["Total"]["Time"] = total_time

    logs_path = Path(paramsdict["Outputfolder"]) / "logs_script1.json"
    with open(logs_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)




def run_GBAS_CLI_memory_part2(paramsdict: dict, executablesdict, parameters_list, list_mandatory, performance, zipping):
        outputfolders_list2 = ['AllelesOut', 'ConsensusOut', 'ConsensusTogether', 'Corrected', 'AlleleCall', 'AdditionalInfo']
        try:
            flag_inputs = check_inputs(paramsdict, executablesdict, parameters_list, list_mandatory)
        except Exception as e:
            flag_inputs = False
            print(f"Error when parsing inputs for the check:\n{e}\n")
        
        samples_dict, number_lines = get_samples(paramsdict["Samplefile"])
        rawsamplenames = get_rawsamples_list(samples_dict)
        primers_dict = get_primers(paramsdict["Primerfile"])
        
        # Initializing Logs
        logs = {
            "Parallel": performance,
            "NumberCores": paramsdict["NumberCores"],
            "QualityTrimmimg": {},
            "Merging": {},
            "Demultiplexing": {},
            "LengthCounts": {},
            "Markerplots": {},
            "LengthExtraction" : {},
            "ConsensusSeqs": {},
            "NCorrection": {},
            "AlleleCall": {},
            "RamUsage": {}, # You can store total script max here if desired
            "Total": {}
        }


        make_output_folders(Path(paramsdict["Outputfolder"]), outputfolders_list2)

        t = Timer()


        with PeakMemoryTracker() as mem:
            run_Length_Extraction_CLI(paramsdict)
            logs["LengthExtraction"]["RamUsage_MB"] = round(mem.max_mem_mb, 2)
            
        logs["LengthExtraction"]["Time"] = t.lap()
        print(f"Time spent: {logs["LengthExtraction"]['Time']:.4g}s. Max RAM: {logs["LengthExtraction"]['RamUsage_MB']} MB\n")


        with PeakMemoryTracker() as mem:
            RunConsensusAll_CLI(paramsdict, performance, int(paramsdict["NumberCores"]))
            logs["ConsensusSeqs"]["RamUsage_MB"] = round(mem.max_mem_mb, 2)
            
        logs["ConsensusSeqs"]["Time"] = t.lap()
        print(f"Time spent: {logs["ConsensusSeqs"]['Time']:.4g}s. Max RAM: {logs["ConsensusSeqs"]['RamUsage_MB']} MB\n")


        with PeakMemoryTracker() as mem:
            RunVariants_Determination_CLI(paramsdict)
            logs["NCorrection"]["RamUsage_MB"] = round(mem.max_mem_mb, 2)
            
        logs["NCorrection"]["Time"] = t.lap()
        print(f"Time spent: {logs["NCorrection"]['Time']:.4g}s. Max RAM: {logs["NCorrection"]['RamUsage_MB']} MB\n")


        with PeakMemoryTracker() as mem:
            run_Allele_Call_CLI(paramsdict)
            logs["AlleleCall"]["RamUsage_MB"] = round(mem.max_mem_mb, 2)
            
        logs["AlleleCall"]["Time"] = t.lap()
        print(f"Time spent: {logs["AlleleCall"]['Time']:.4g}s. Max RAM: {logs["AlleleCall"]['RamUsage_MB']} MB\n")

        # --- Finalizing ---
        total_time = t.total()
        print('end-1c', f"\n\nTotal Time spent: {total_time}s \n\n")
        logs["Total"]["Time"] = total_time

        logs_path = Path(paramsdict["Outputfolder"]) / "logs_script2.json"
        with open(logs_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)









        



    
class PeakMemoryTracker:
    def __init__(self, interval=0.1):
        self.interval = interval
        self.max_mem_bytes = 0
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._monitor)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_event.set()
        self.thread.join()

    def _monitor(self):
        current_process = psutil.Process()
        while not self.stop_event.is_set():
            try:
                # 1. Get memory of the current Python script
                total_mem = current_process.memory_info().rss
                
                # 2. Add memory of all child processes (the CLIs)
                children = current_process.children(recursive=True)
                for child in children:
                    try:
                        total_mem += child.memory_info().rss
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass # Child might finish between listing and checking

                # 3. Update Peak
                if total_mem > self.max_mem_bytes:
                    self.max_mem_bytes = total_mem
                    
            except Exception:
                pass # Fail silently to not crash the main script
            
            time.sleep(self.interval)

    @property
    def max_mem_gb(self):
        """Returns max memory in GB"""
        return self.max_mem_bytes / (1024 ** 3)
        
    @property
    def max_mem_mb(self):
        """Returns max memory in MB"""
        return self.max_mem_bytes / (1024 ** 2)