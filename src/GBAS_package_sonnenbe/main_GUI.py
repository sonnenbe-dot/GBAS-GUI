import customtkinter as ctk
from tkinter import ttk, filedialog
import tkinter as tk
import os, argparse, json, re, shutil
from pathlib import Path
import platform, threading, multiprocessing, time

from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import parse_parameterfile, check_paramsdict, new_paramsdict
from GBAS_package_sonnenbe.helper_functions.parse_executables import check_executables #get_bin_executables
from GBAS_package_sonnenbe.helper_functions.input_checks import check_inputs #get_bin_executables
from GBAS_package_sonnenbe.helper_functions.parse_samplefile import get_samples, get_rawsamples_list #get_bin_executables
from GBAS_package_sonnenbe.helper_functions.make_outputs import make_output_folders
from GBAS_package_sonnenbe.helper_functions.parse_primerfile import get_primers
from GBAS_package_sonnenbe.helper_functions.timer_class import Timer

from GBAS_package_sonnenbe.GUI_widgets.general_params_widget import general_params_window
from GBAS_package_sonnenbe.GUI_widgets.data_prep_widget import data_prep_window
from GBAS_package_sonnenbe.GUI_widgets.status_widget import status_window
from GBAS_package_sonnenbe.GUI_widgets.PIC_calculation_widget import PIC_calculation_window
from GBAS_package_sonnenbe.GUI_widgets.advanced_widget import advanced_window
from GBAS_package_sonnenbe.GUI_widgets.database_widget import Database_adding_window, Database_status_window
from GBAS_package_sonnenbe.GUI_widgets.extract_subset_widget import extract_subset_window

from GBAS_package_sonnenbe.main_functions.trimmomatic import checkInputDir, runTrimomatic, runTrimomatic_GUI
from GBAS_package_sonnenbe.main_functions.merging import runUsearch, runUsearch_GUI
from GBAS_package_sonnenbe.main_functions.demultiplexing import runDemultiplexing_GUI
from GBAS_package_sonnenbe.main_functions.markerstatistics import runLengthstatistics_GUI
from GBAS_package_sonnenbe.main_functions.markerplots import runMarkerplots_GUI

from GBAS_package_sonnenbe.main_functions.extract_lengths import run_Length_Extraction_GUI, run_Length_Extraction
from GBAS_package_sonnenbe.main_functions.consensus_all import RunConsensusAll_GUI, RunConsensusAll
from GBAS_package_sonnenbe.main_functions.allele_determination import RunVariants_Determination_GUI
from GBAS_package_sonnenbe.main_functions.allele_calling import run_Allele_Call_GUI

from GBAS_package_sonnenbe.main_functions.PIC_calculation import calculate_PIC


def main():

    # parser = argparse.ArgumentParser(description='Starting GBAS-GUI! \n')
    # parser.add_argument("parametersfilepath", type = str, help = "Input parameterfilepath!")
    # args = parser.parse_args()

    parametersfilepath = str(input("Enter parameterfilepath: \n"))
    print("Parameterfilepath set to " + parametersfilepath + "\n")


    try:
        parameterfilepath = Path(parametersfilepath)
    except Exception as e:
        print(f"Not a valid parameterfilepath given!\nException: {e} \n")
        return

    root = root_window(parameterfilepath)
    root.mainloop()

    return 0

class root_window(ctk.CTk):
    def __init__(self, parameterfilepath : Path): #*args, **kwargs
        super().__init__() #*args, **kwargs
        
        self.title("GUI GBAS")
        self.geometry(f"{1000}x{600}")

        self.parameterfilepath = parameterfilepath
        
        #Using grid_...configure only for column 0 and row 0 which means my root has only 1 row and 1 column
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(True)
        
        self.main_frame = main_window(self, parameterfilepath)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Allow the container to expand in both directions
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind('<Return>', lambda event: self.destroy)


class main_window(ctk.CTkFrame):
    def __init__(self, parent, parameterfilepath : Path):
        super().__init__(parent)



        # self.parameterfilename = "parameters_GBAS"
        self.parameterfilepath = parameterfilepath
        self.parameterfilename = str(parameterfilepath.name).split(".txt")[0]
        #self.adaptersfilename = "TrueSeqAdaptersInUsage.fa"
        #self.RscriptDiploid = "Rscript_Markerlength_STUTTER_Color_BaryzentricMinsize20_notVerbose.R"
        #self.RscriptHaploid = "Rscript_Markerlength_Haploid.R"

        #self.current_workspace = Path.cwd() / "GBAS_package_sonnenbe"
        self.current_workspace = Path.cwd()
        self.parameterfilename_full = self.parameterfilename + ".txt"

        #self.parameterfilepath_default = self.current_workspace / self.parameterfilename_full

        self.parameterfilepath_default = self.current_workspace / "parameters.txt"

        self.parameters_list = ["Outputfolder", "Bin", "Rawdata", "Primerfile", "Samplefile", "Metadata", "Allelelist", "Database", "Maxmismatch", "Mincount", "Minlength", "Consensusthreshold", "Lengthwindow", "Ploidy", "Operatingsystem", "Uniqueidentifier", "Indexcomboposition", "NumberCores"]
        self.parameters_default = [("Outputfolder", str(self.current_workspace / "output")), ("Bin", str(self.current_workspace / "bin")), ("Rawdata", "None"), ("Primerfile", "None"), ("Samplefile", "None"), ("Metadata", "None"), ("Allelelist", "None"), ("Database", "None"), ("Maxmismatch", 2), ("Mincount", 20), ("Minlength", 290), ("Consensusthreshold", 0.7), ("Lengthwindow", "310, 600"), ("Ploidy", "diploid"), ("Operatingsystem", platform.system()), ("Uniqueidentifier", "default"), ("Indexcomboposition", 1), ("NumberCores", multiprocessing.cpu_count()-1)]

        self.paramsdict = {}
        #self.executablesdict = {}

        self.parse_parameterfile()

        self.list_not_mandatory = ["Metadata", "Allelelist", "Database"]
        self.list_mandatory = ["Outputfolder", "Bin", "Rawdata", "Primerfile", "Samplefile"]

        self.executablesdict = {
            "Folders" : {
                "Trimmodir" : Path(Path(self.paramsdict["Bin"]) / "Trimmomatic-0.39"),
                "Adaptersdir" : Path(Path(self.paramsdict["Bin"]) / "Trimmomatic-0.39" / "adapters")
            },
            "Files" : {
                "Trimmomatic" : Path(Path(self.paramsdict["Bin"]) / "Trimmomatic-0.39" / "trimmomatic-0.39.jar"),
                "UsearchLinux" : Path(Path(self.paramsdict["Bin"]) / "usearch11.0.667_i86linux32"),
                "UsearchWindows" : Path(Path(self.paramsdict["Bin"]) / "usearch11.0.667_win32.exe"),
                "RScriptDiploid" : Path(Path(self.paramsdict["Bin"]) / "Rscript_Markerlength_STUTTER_Color_BaryzentricMinsize20_notVerbose.R"),
                "RScriptHaploid" : Path(Path(self.paramsdict["Bin"]) / "Rscript_Markerlength_Haploid.R"),
            },
            "Additional" : {
                "Adapterfile" : Path(Path(self.paramsdict["Bin"]) / "Trimmomatic-0.39" / "adapters" / "TrueSeqAdaptersInUsage.fa")
            }
        }

        
        self.outputfolders_list1 = ['QC', 'SeparatOut', 'MergedOut', 'MarkerStatistics', 'MarkerStatisticsDuplicates',  'AlleleLenghtCounts', 'MarkerPlots', 'Markerplots_dupl']
        self.outputfolders_list2 = ['AllelesOut', 'ConsensusOut', 'ConsensusTogether', 'Corrected', 'AlleleCall', 'AdditionalInfo']

        self.add_dots_pipelinetextbox = False

        self.performance = True
        self.number_cores = multiprocessing.cpu_count()-1

        self.advanced_pipeline_options = ["Trimmomatic", "Usearch", "Demultiplexing", "Markerstatistics", "Markerplots+Markermatrix",  "LengthExtraction", "ConsensusSequence", "AlleleDetection", "AlleleCall"]
        self.checkbox_states_pipeline_advanced = {key : 0 for key in self.advanced_pipeline_options}
        self.checkboxes_pipeline1 = []
        self.checkboxes_pipeline2 = []
        self.checkbox_advanced = []


        
        self.checkbox_include_dict = {}
        self.checkbox_states_dict2 = {}
        self.checkbox_states_dict2["Project"] = {}
        self.checkbox_states_dict2["Metadata2"] = {}
        self.checkbox_states_dict2["Loci"] = {}

        self.build_mainframe()

        #print(self.paramsdict["Bin"])

    def parse_parameterfile(self):
        paramscheck = True
        try:
            self.paramsdict = parse_parameterfile(self.parameterfilepath)
        except Exception as e:
            paramscheck = False
            print(f"Either no parameterfile {self.parameterfilename} in the current directory or a problem with parsing the parameterfile!\nException: {e} \n")

        check_params = check_paramsdict(self.paramsdict, self.parameters_list)
        if (paramscheck and not(check_params)):
            print("Either parameterfile empty or parameterfile does not include certain parameter values necessary for the GBAS pipeline!\n")
        
        if (not(self.paramsdict) or not(check_params)):
            print("Setting Parameters to defaults. \n")
            self.paramsdict = new_paramsdict(self.parameters_default)
            self.parameterfilepath = self.parameterfilepath_default
            print("Setting parameterfile to default name.\n")

        




    def build_mainframe(self):
        for i in range(0, 6, 1):
            if (i in (0, 2, 4)):
                self.columnconfigure(i, weight=1) 
            else:
                self.columnconfigure(i, weight=0) 
            
        self.parameters = ctk.CTkFrame(self, width=100, corner_radius=2)
        self.parameters.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.parameters.grid_columnconfigure(0, weight=1)
        self.parameters.grid_rowconfigure(5, weight=1)
        ctk.CTkLabel(self.parameters, text="Preparation", font=ctk.CTkFont(size=28, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 20))
        ctk.CTkButton(self.parameters, border_width=1, border_color="black", text_color="black", text = "Pipeline Parameters", command = self.get_general_params).grid(row=1, column=0, padx=20, pady=(10, 10)) #, command = self.get_general_params
        ctk.CTkButton(self.parameters, border_width=1, border_color="black", text_color="black", text = "Workspace Status", command = self.get_status_window).grid(row=2, column=0, padx=20, pady=(10, 20)) #, command = self.check_status
        ctk.CTkButton(self.parameters, border_width=1, border_color="black", text_color="black", text = "Data Preparation", command = self.get_data_prep).grid(row=3, column=0, padx=20, pady=(10, 20)) #, command = self.check_status



        self.separator1 = tk.Canvas(self, width=2, bg='black')
        self.separator1.grid(row=0, column=1, sticky='ns')
        self.separator1.create_line(1, 0, 1, self.separator1.winfo_height())
        
        self.pipeline = ctk.CTkFrame(self, width=100, corner_radius=2)
        self.pipeline.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.pipeline.grid_columnconfigure(0, weight=1)
        self.pipeline.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(self.pipeline, text="Pipeline", font=ctk.CTkFont(size=28, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 20)) #command=self.advanced_setting
        ctk.CTkButton(self.pipeline, border_width=1, border_color="black", text_color="black", text = "Advanced Mode" , command = self.run_individual_pipeline_parts).grid(row=1, column=0, padx=20, pady=(10, 10)) #command = self.advanced_setting
        ctk.CTkButton(self.pipeline, border_width=1, border_color="black", text_color="black", text = "Individual Mode").grid(row=2, column=0, padx=20, pady=(10, 40)) #command = self.individual_run individual_running command = self.individual_running
        ctk.CTkButton(self.pipeline, border_width=1, border_color="black", text_color="black", text = "Run Length Detection", command = self.first_script_threading).grid(row=3, column=0, padx=20, pady=(10, 10)) #command = self.run_first_script
        ctk.CTkButton(self.pipeline, border_width=1, border_color="black", text_color="black", text = "Run SNP Detection", command = self.second_script_threading).grid(row=4, column=0, padx=20, pady=(10, 20)) #command = self.run_second_script 
        self.textbox_pipeline = ctk.CTkTextbox(self.pipeline, width=250)
        self.textbox_pipeline.grid(row=5, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.textbox_pipeline.insert("0.0", "Pipeline has not started:" + "\n\n" * 2)
        


        self.separator2 = tk.Canvas(self, width=2, bg='black')
        self.separator2.grid(row=0, column=3, sticky='ns')
        self.separator2.create_line(1, 0, 1, self.separator1.winfo_height())

        self.database = ctk.CTkFrame(self, width=100, corner_radius=2)
        self.database.grid(row=0, column=4, rowspan=4, sticky="nsew")
        self.database.grid_columnconfigure(0, weight=1)
        self.database.grid_rowconfigure(4, weight=1)
        self.database.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(self.database, text="Database", font=ctk.CTkFont(size=28, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 20), sticky="nsew")
        ctk.CTkButton(self.database, border_width=1, border_color="black", text_color="black", text = "PIC Calculation", command = self.PIC_calculation).grid(row=1, column=0, padx=20, pady=(10, 10)) 

        ctk.CTkButton(self.database, border_width=1, border_color="black", text_color="black", text = "Add to Database", command = self.adding_dataset).grid(row=3, column=0, padx=20, pady=(10, 10))    
        ctk.CTkButton(self.database, border_width=1, border_color="black", text_color="black", text = "Database Status", command = self.show_database_status).grid(row=4, column=0, padx=20, pady=(10, 10))  
        ctk.CTkButton(self.database, border_width=1, border_color="black", text_color="black", text = "Extract subset", command = self.extract_subset_from_database).grid(row=5, column=0, padx=20, pady=(10, 10))#extract_subset_from_database_threading

    def get_general_params(self):
        #window = tk.Toplevel(self)
        # window.transient(self)
        # window.focus_set()

        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Show Parameters Window \n")

        self.parse_parameterfile()

        param_list_dirs = ["Outputfolder", "Bin", "Rawdata"]
        param_list_files = ["Primerfile", "Samplefile", "Metadata", "Allelelist"]
        param_list_calc = ["Maxmismatch", "Mincount", "Minlength", "Consensusthreshold", "Lengthwindow"]
        param_list_special = ["Ploidy", "Operatingsystem", "Uniqueidentifier", "Indexcomboposition", "NumberCores"]
        obj = general_params_window(self, self.parameterfilepath, self.current_workspace, self.paramsdict, "Folders", "Files", "Calculation Params", "Additional Params", param_list_dirs, param_list_files, param_list_calc, param_list_special, on_done=self.update_parameterfilepath)
        
        
        # self.parameterfilename, self.paramsdict = obj.return_params()
        # print(self.paramsdict)
        # print(self.parameterfilename)

    def update_parameterfilepath(self, parameterfilepath : Path):
        self.parameterfilepath = parameterfilepath
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert("0.0", "Pipeline has not started:" + "\n\n" * 2)
        #self.label.configure(text=f"Current value: {self.param}")
    
    def update_rawdatafolder(self, rawdatafolderpath : Path):
        self.paramsdict["Rawdata"] = str(rawdatafolderpath)
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert("0.0", "Pipeline has not started:" + "\n\n" * 2)
    
    def update_textbox(self, text : str):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert("0.0", text + "\n\n" * 2)

    def update_advanced(self, text : str, performance : bool, checkbox_states_pipeline_advanced : dict):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert("0.0", text + "\n\n" * 2)
        self.checkbox_states_pipeline_advanced = checkbox_states_pipeline_advanced
        self.performance = performance

    def update_extract(self, text : str, include_dict1 : dict, include_dict2 : dict):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert("0.0", text + "\n\n" * 2)
        self.checkbox_include_dict = include_dict1
        self.checkbox_states_dict2 = include_dict2

    
    def get_data_prep(self):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Show Preparation Window \n")
        self.parse_parameterfile()
        obj = data_prep_window(self, self.paramsdict["Samplefile"], self.paramsdict["Rawdata"], self.current_workspace, self.paramsdict, on_done=self.update_rawdatafolder)

    def get_status_window(self):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Show Workspace Window \n")
        #self.add_dots_pipelinetextbox = True

        self.parse_parameterfile()
        #self.executablesdict = get_bin_executables(self.paramsdict["Bin"], self.adaptersfilename, self.RscriptDiploid, self.RscriptHaploid)

        #list_not_mandatory = ["Metadata", "Allelelist", "Database"]
        #list_mandatory = ["Outputfolder", "Bin", "Rawdata", "Primerfile", "Samplefile"]
        Path(self.paramsdict["Outputfolder"]).mkdir(parents=True, exist_ok=True)
        status_window(self, self.paramsdict, self.executablesdict, self.parameters_list, self.list_not_mandatory, self.list_mandatory, on_done=self.update_textbox)
    

    def append_period(self):
        self.textbox_pipeline.insert('end-1c', ".")
        if self.add_dots_pipelinetextbox:
            self.after(1000, self.append_period)

    def first_script_threading(self):
        thread = threading.Thread(target=self.first_script_running)
        thread.start()
    
    def first_script_running(self):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Running Length Detection!\n\n")

        self.parse_parameterfile()
        
        self.textbox_pipeline.insert("end", "Check Inputs: ")
        flag_inputs = check_inputs(self.paramsdict, self.executablesdict, self.parameters_list, self.list_mandatory)
        if (flag_inputs):
            self.textbox_pipeline.insert("end", "Correct.\n")
            self.textbox_pipeline.insert("end", "Pipeline is ready to start.\n\n")
        else:
            self.textbox_pipeline.insert("end", "Not Correct.\n")
            self.textbox_pipeline.insert("end", "Pipeline is not ready to start.\n")
            self.textbox_pipeline.insert("end", "Check Workspace Status!\n\n")
            return
        
        samples_dict, number_lines = get_samples(self.paramsdict["Samplefile"])
        #print(samples_dict)
        rawsamplenames = get_rawsamples_list(samples_dict)
        primers_dict = get_primers(self.paramsdict["Primerfile"])
        number_cores = multiprocessing.cpu_count()-1
        logs = {"Parallel" : self.performance,
                "NumberCores" : self.paramsdict["NumberCores"],
                "QualityTrimmimg" : {},
                "Merging" : {},
                "Demultiplexing" : {},
                "LengthCounts" : {},
                "Markerplots" : {},
                "ConsensusSeqs" : {},
                "NCorrection" : {},
                "AlleleCall" : {},
                "Total" : {}
        }

        make_output_folders(Path(self.paramsdict["Outputfolder"]), self.outputfolders_list1)

        self.add_dots_pipelinetextbox = True
        #start = time.time()
        t = Timer()
        
        self.append_period()



        runTrimomatic_GUI(self.textbox_pipeline, self.paramsdict, self.executablesdict, rawsamplenames, self.performance, int(self.paramsdict["NumberCores"]))
        logs["QualityTrimmimg"]["Time"] = t.lap()
        self.textbox_pipeline.insert("end", f"\nTime spent: {logs['QualityTrimmimg']['Time']:.4g}.\n")

        runUsearch_GUI(self.textbox_pipeline, self.paramsdict, self.executablesdict, self.performance, int(self.paramsdict["NumberCores"]))
        logs["Merging"]["Time"] = t.lap()
        self.textbox_pipeline.insert("end", "\nTime spent: " + str(logs['Merging']['Time']) + ".\n")

        runDemultiplexing_GUI(self.textbox_pipeline, self.paramsdict, primers_dict, samples_dict, self.performance, int(self.paramsdict["NumberCores"]))
        logs["Demultiplexing"]["Time"] = t.lap()
        self.textbox_pipeline.insert("end", "\nTime spent: " + str(logs['Demultiplexing']['Time']) + ".\n")

        runLengthstatistics_GUI(self.textbox_pipeline, self.paramsdict, primers_dict, self.performance, int(self.paramsdict["NumberCores"]))
        logs["LengthCounts"]["Time"] = t.lap()
        self.textbox_pipeline.insert("end", "\nTime spent: " + str(logs['LengthCounts']['Time']) + ".\n")

        runMarkerplots_GUI(self.textbox_pipeline, self.paramsdict, primers_dict, samples_dict)
        logs["Markerplots"]["Time"] = t.lap()
        self.textbox_pipeline.insert("end", "\nTime spent: " + str(logs['Markerplots']['Time']) + ".\n")




        self.add_dots_pipelinetextbox = False
        self.textbox_pipeline.insert('end-1c', "\n\nTotal Time spent: " + str(t.total()) + "s \n\n")

        logs["Total"]["Time"] = t.total()
        # logs["Total"]["Time"] = end - start

        logs_path = Path(self.paramsdict["Outputfolder"]) / "logs_script1.json"
        with open(logs_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)

    def second_script_threading(self):
        thread = threading.Thread(target=self.second_script_running)
        thread.start()
    
    def second_script_running(self):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Running Allele Detection!\n\n")

        self.parse_parameterfile()

        samples_dict, number_lines = get_samples(self.paramsdict["Samplefile"])
        rawsamplenames = get_rawsamples_list(samples_dict)
        primers_dict = get_primers(self.paramsdict["Primerfile"])
        number_cores = multiprocessing.cpu_count()-1
        logs = {"Parallel" : self.performance,
                "NumberCores" : int(self.paramsdict["NumberCores"]),
                "QualityTrimmimg" : {},
                "Merging" : {},
                "Demultiplexing" : {},
                "LengthCounts" : {},
                "Markerplots" : {},
                "LengthExtraction" : {},
                "ConsensusSeqs" : {},
                "NCorrection" : {},
                "AlleleCall" : {},
                "Total" : {}
        }

        make_output_folders(Path(self.paramsdict["Outputfolder"]), self.outputfolders_list2)
        self.add_dots_pipelinetextbox = True
        t = Timer()
        
        self.append_period()


        run_Length_Extraction_GUI(self.textbox_pipeline, self.paramsdict)
        logs["LengthExtraction"]["Time"] = t.lap()
        self.textbox_pipeline.insert("end", f"\nTime spent: {logs['LengthExtraction']['Time']:.4g}.\n")

        RunConsensusAll_GUI(self.textbox_pipeline, self.paramsdict, self.performance, int(self.paramsdict["NumberCores"]))
        logs["ConsensusSeqs"]["Time"] = t.lap()
        self.textbox_pipeline.insert("end", f"\nTime spent: {logs['ConsensusSeqs']['Time']:.4g}.\n")

        RunVariants_Determination_GUI(self.textbox_pipeline, self.paramsdict)
        logs["NCorrection"]["Time"] = t.lap()
        self.textbox_pipeline.insert("end", f"\nTime spent: {logs['NCorrection']['Time']:.4g}.\n")

        run_Allele_Call_GUI(self.textbox_pipeline, self.paramsdict)
        logs["AlleleCall"]["Time"] = t.lap()
        self.textbox_pipeline.insert("end", f"\nTime spent: {logs['AlleleCall']['Time']:.4g}.\n")

        # inputfolderpath = Path("E:\\Work_Paper_GUI\\PIC\\test_folder")
        # outputfolderpath = Path("E:\\Work_Paper_GUI\\PIC\\output")
        # calculate_PIC(inputfolderpath, outputfolderpath)

        self.add_dots_pipelinetextbox = False
        self.textbox_pipeline.insert('end-1c', "\n\nTotal Time spent: " + str(t.total()) + "s \n\n")

        logs["Total"]["Time"] = t.total()

        logs_path = Path(self.paramsdict["Outputfolder"]) / "logs_script2.json"
        with open(logs_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)
    
    def PIC_calculation(self):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Show PIC Calculation Window \n")
        PIC_calculation_window(self, self.current_workspace, self.paramsdict, on_done=self.update_textbox)

    def run_individual_pipeline_parts(self):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Show Advanced Pipeline Options Window \n")
        self.parse_parameterfile()
        advanced_window(self, self.current_workspace, self.paramsdict, self.performance, int(self.paramsdict["NumberCores"]), self.checkbox_states_pipeline_advanced, self.executablesdict, self.parameters_list, self.list_mandatory, self.textbox_pipeline, self.outputfolders_list1, self.outputfolders_list2, on_done=self.update_advanced)

    def adding_dataset(self):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Show Database Adding Window \n")
        self.parse_parameterfile()

        matrix_outputpath = Path(self.paramsdict["Outputfolder"]) / ("AlleleCall/matrix.json")
        if (matrix_outputpath.exists()):
            Database_adding_window(self, self.current_workspace, self.paramsdict, str(matrix_outputpath), on_done=self.update_textbox)
        else:
            Database_adding_window(self, self.current_workspace, self.paramsdict, "", on_done=self.update_textbox)
    
    def show_database_status(self):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Show Database Status Window \n")
        self.parse_parameterfile()

        Database_status_window(self, self.current_workspace, self.paramsdict, on_done=self.update_textbox)
    

    # def extract_subset_from_database_threading(self):
    #     thread = threading.Thread(target=self.extract_subset_from_database)
    #     thread.start()

    def extract_subset_from_database(self):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Show Extract Subset Window \n")
        self.parse_parameterfile()

        extract_subset_window(self, self.current_workspace, self.paramsdict, self.checkbox_include_dict, self.checkbox_states_dict2, self.textbox_pipeline, on_done=self.update_extract)


if __name__ == "__main__":
    main()