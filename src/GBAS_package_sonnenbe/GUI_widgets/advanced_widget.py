import customtkinter as ctk
from tkinter import ttk, filedialog, font
import tkinter as tk
import os, platform
from pathlib import Path
import threading, multiprocessing, json

from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import parse_parameterfile, check_paramsdict, new_paramsdict
from GBAS_package_sonnenbe.helper_functions.parse_executables import check_executables #get_bin_executables
from GBAS_package_sonnenbe.helper_functions.input_checks import check_inputs #get_bin_executables
from GBAS_package_sonnenbe.helper_functions.parse_samplefile import get_samples, get_rawsamples_list #get_bin_executables
from GBAS_package_sonnenbe.helper_functions.make_outputs import make_output_folders
from GBAS_package_sonnenbe.helper_functions.parse_primerfile import get_primers
from GBAS_package_sonnenbe.helper_functions.timer_class import Timer

from GBAS_package_sonnenbe.main_functions.trimmomatic import runTrimomatic_GUI
from GBAS_package_sonnenbe.main_functions.merging import runUsearch_GUI
from GBAS_package_sonnenbe.main_functions.demultiplexing import runDemultiplexing_GUI
from GBAS_package_sonnenbe.main_functions.markerstatistics import runLengthstatistics_GUI
from GBAS_package_sonnenbe.main_functions.markerplots import runMarkerplots_GUI

from GBAS_package_sonnenbe.main_functions.extract_lengths import run_Length_Extraction_GUI, run_Length_Extraction
from GBAS_package_sonnenbe.main_functions.consensus_all import RunConsensusAll_GUI, RunConsensusAll
from GBAS_package_sonnenbe.main_functions.allele_determination import RunVariants_Determination_GUI
from GBAS_package_sonnenbe.main_functions.allele_calling import run_Allele_Call_GUI

class advanced_window(tk.Toplevel):
    def __init__(self, parent, current_workspace : Path, paramsdict : dict, performance : bool, num_cores : int, checkbox_states_pipeline_advanced : dict, executablesdict : dict, parameters_list : list, list_mandatory : list, textbox_pipeline : ctk.CTkTextbox, outputfolders_list1 : list, outputfolders_list2 : list, on_done):
        super().__init__(parent)

        self.on_done = on_done
        self.add_dots_pipelinetextbox = False
        self.textbox_pipeline = textbox_pipeline

        self.outputfolders_list1 = outputfolders_list1
        self.outputfolders_list2 = outputfolders_list2

        self.title("Advanced Pipeline Options")
        self.transient(parent)
        self.focus_set()
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        

        self.current_workspace = current_workspace
        self.paramsdict = paramsdict
        self.executablesdict = executablesdict
        self.parameters_list = parameters_list
        self.list_mandatory = list_mandatory

        self.number_cores = num_cores
        self.performance = performance
        self.checkbox_performance = 1
        if (not(self.performance)):
            self.checkbox_performance = 0
        self.checkbox_states_pipeline_advanced = checkbox_states_pipeline_advanced
        self.checkboxes_pipeline1 = []
        self.checkboxes_pipeline2 = []
        self.checkbox_advanced = []

        self.build_window()

        #self.bind('<Return>', lambda event: self.destroy())

        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.bind('<Return>', lambda event: self.closing())
    
    def closing(self):
        # hand the value back before destroying
        try:
            for checkbox in self.checkboxes_pipeline1:
                checkbox_text = checkbox.cget("text")
                self.checkbox_states_pipeline_advanced[checkbox_text] = checkbox.get()
            
            for checkbox in self.checkboxes_pipeline2:
                checkbox_text = checkbox.cget("text")
                self.checkbox_states_pipeline_advanced[checkbox_text] = checkbox.get()
            
            for checkbox in self.checkbox_advanced:
                self.checkbox_performance = checkbox.get()

            #update self.number_cores here as well in the future!
            
            if (self.checkbox_performance):
                self.performance = True
            else:
                self.performance = False
            self.on_done("Pipeline has not started:", self.performance, self.checkbox_states_pipeline_advanced)
        finally:
            self.destroy()

    
    def build_window(self):
        ctk.CTkLabel(self, text="Advanced Input Settings:", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 20))
        
        advanced_input_settings = ctk.CTkFrame(self, width=100, corner_radius=2)
        advanced_input_settings.grid(row=1, column=0, rowspan=1, sticky="nsew")
        advanced_input_settings.grid_columnconfigure(0, weight=1)
        advanced_input_settings.grid_columnconfigure(1, weight=1)
        advanced_input_settings.grid_columnconfigure(2, weight=1)
        advanced_input_settings.grid_rowconfigure(0, weight=1)
        advanced_input_settings.grid_rowconfigure(1, weight=1)
        
        
        checkbox_performance_var = tk.IntVar(value = self.checkbox_performance)
        checkbox_performance = ctk.CTkCheckBox(advanced_input_settings, text="HighPerformance", variable=checkbox_performance_var)
        checkbox_performance.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="w")
        self.checkbox_advanced.append(checkbox_performance)

        checkbox_performance_var = tk.IntVar(value = self.checkbox_performance)
        checkbox_performance = ctk.CTkCheckBox(advanced_input_settings, text="Zipping files", variable=checkbox_performance_var)
        checkbox_performance.grid(row=2, column=0, padx=10, pady=(5, 5), sticky="w")
        self.checkbox_advanced.append(checkbox_performance)
        
        advanced_pipeline1_settings_logo = ctk.CTkLabel(self, text="Advanced Pipeline Settings (1):", font=ctk.CTkFont(size=20, weight="bold"))
        advanced_pipeline1_settings_logo.grid(row=3, column=0, padx=20, pady=(20, 20))
        
        advanced_pipeline1_settings = ctk.CTkFrame(self, width=100, corner_radius=2)
        advanced_pipeline1_settings.grid(row=4, column=0, rowspan=1, sticky="nsew")
        advanced_pipeline1_settings.grid_columnconfigure(0, weight=1)
        advanced_pipeline1_settings.grid_rowconfigure(0, weight=1)
        advanced_pipeline1_settings.grid_rowconfigure(1, weight=1)
        
        advanced_pipeline2_settings_logo = ctk.CTkLabel(self, text="Advanced Pipeline Settings (2):", font=ctk.CTkFont(size=20, weight="bold"))
        advanced_pipeline2_settings_logo.grid(row=5, column=0, padx=20, pady=(20, 20))
        
        advanced_pipeline2_settings = ctk.CTkFrame(self, width=100, corner_radius=2)
        advanced_pipeline2_settings.grid(row=6, column=0, rowspan=1, sticky="nsew")
        advanced_pipeline2_settings.grid_columnconfigure(0, weight=1)
        advanced_pipeline2_settings.grid_rowconfigure(0, weight=1)
        advanced_pipeline2_settings.grid_rowconfigure(1, weight=1)
        
        
        scrollframe_pipeline1 = ctk.CTkFrame(advanced_pipeline1_settings, width=50, corner_radius=2)
        scrollframe_pipeline1.grid(row=0, column=0, rowspan=1, sticky="nsew")
        scrollframe_pipeline1.grid_columnconfigure(0, weight=1)
        
        options = ["Trimmomatic", "Usearch", "Demultiplexing", "Markerstatistics", "Markerplots+Markermatrix"]
        for i, option in enumerate(options):
            checkbox_var = tk.IntVar(value = self.checkbox_states_pipeline_advanced[option])
            checkbox = ctk.CTkCheckBox(scrollframe_pipeline1, text=option, variable=checkbox_var)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(5, 5), sticky="w")
            self.checkboxes_pipeline1.append(checkbox)
        
        scrollframe_pipeline2 = ctk.CTkFrame(advanced_pipeline2_settings, width=50, corner_radius=2)
        scrollframe_pipeline2.grid(row=0, column=0, rowspan=1, sticky="nsew")
        scrollframe_pipeline2.grid_columnconfigure(0, weight=1)
        
        options = ["LengthExtraction", "ConsensusSequence", "AlleleDetection", "AlleleCall"]
        for i, option in enumerate(options):
            checkbox_var = tk.IntVar(value = self.checkbox_states_pipeline_advanced[option])
            checkbox = ctk.CTkCheckBox(scrollframe_pipeline2, text=option, variable=checkbox_var)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(5, 5), sticky="w")
            self.checkboxes_pipeline2.append(checkbox)
        
        ctk.CTkButton(self, border_width=1, border_color="black", text_color="black", text = "Run Pipeline1 Advanced", command = self.run_lengths_advanced_thread).grid(row=7, column=0, sticky="sw", padx=(5, 25), pady=(10, 5))
        ctk.CTkButton(self, border_width=1, border_color="black", text_color="black", text = "Run Pipeline2 Advanced", command = self.run_snips_advanced_thread).grid(row=7, column=0, sticky="se", padx=(25, 5), pady=(10, 5))

    def run_lengths_advanced_thread(self):
        thread = threading.Thread(target=self.run_lengths_advanced, daemon=True)
        thread.start()

    def run_snips_advanced_thread(self):
        thread = threading.Thread(target=self.run_snips_advanced, daemon=True)
        thread.start()

    
    def run_lengths_advanced(self):
        for checkbox in self.checkboxes_pipeline1:
            checkbox_text = checkbox.cget("text")
            self.checkbox_states_pipeline_advanced[checkbox_text] = checkbox.get()
        
        for checkbox in self.checkboxes_pipeline2:
            checkbox_text = checkbox.cget("text")
            self.checkbox_states_pipeline_advanced[checkbox_text] = checkbox.get()
        

        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Running Length Detection in advanced mode \n")

        
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
                "NumberCores" : number_cores,
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

        make_output_folders(Path(self.paramsdict["Outputfolder"]), self.outputfolders_list1)

        self.add_dots_pipelinetextbox = True
        t = Timer()
        self.append_period()

        if (self.checkbox_states_pipeline_advanced["Trimmomatic"] == 1):
            runTrimomatic_GUI(self.textbox_pipeline, self.paramsdict, self.executablesdict, rawsamplenames, self.performance, self.number_cores)
            logs["QualityTrimmimg"]["Time"] = t.lap()
            self.textbox_pipeline.insert("end", f"\nTime spent: {logs["QualityTrimmimg"]["Time"]:.4g}.\n")
        if (self.checkbox_states_pipeline_advanced["Usearch"] == 1):
            runUsearch_GUI(self.textbox_pipeline, self.paramsdict, self.executablesdict, self.performance, self.number_cores)
            logs["Merging"]["Time"] = t.lap()
            self.textbox_pipeline.insert("end", "\nTime spent: " + str(logs["Merging"]["Time"]) + ".\n")
        if (self.checkbox_states_pipeline_advanced["Demultiplexing"] == 1):
            runDemultiplexing_GUI(self.textbox_pipeline, self.paramsdict, primers_dict, samples_dict, self.performance, self.number_cores)
            logs["Demultiplexing"]["Time"] = t.lap()
            self.textbox_pipeline.insert("end", "\nTime spent: " + str(logs["Demultiplexing"]["Time"]) + ".\n")
        if (self.checkbox_states_pipeline_advanced["Markerstatistics"] == 1):
            runLengthstatistics_GUI(self.textbox_pipeline, self.paramsdict, primers_dict, self.performance, self.number_cores)
            logs["LengthCounts"]["Time"] = t.lap()
            self.textbox_pipeline.insert("end", "\nTime spent: " + str(logs["LengthCounts"]["Time"]) + ".\n")
        if (self.checkbox_states_pipeline_advanced["Markerplots+Markermatrix"] == 1):
            runMarkerplots_GUI(self.textbox_pipeline, self.paramsdict, primers_dict, samples_dict)
            logs["Markerplots"]["Time"] = t.lap()
            self.textbox_pipeline.insert("end", "\nTime spent: " + str(logs["Markerplots"]["Time"]) + ".\n")

        self.add_dots_pipelinetextbox = False
        self.textbox_pipeline.insert('end-1c', "\n\nTotal Time spent: " + str(t.total()) + "s \n\n")

        logs["Total"]["Time"] = t.total()
        # logs["Total"]["Time"] = end - start

        logs_path = Path(self.paramsdict["Outputfolder"]) / "logs_script1.json"
        with open(logs_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)


    def run_snips_advanced_thread(self):
        for checkbox in self.checkboxes_pipeline1:
            checkbox_text = checkbox.cget("text")
            self.checkbox_states_pipeline_advanced[checkbox_text] = checkbox.get()
        
        for checkbox in self.checkboxes_pipeline2:
            checkbox_text = checkbox.cget("text")
            self.checkbox_states_pipeline_advanced[checkbox_text] = checkbox.get()
        
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Running Snips Detection in advanced mode \n")

        samples_dict, number_lines = get_samples(self.paramsdict["Samplefile"])
        #print(samples_dict)
        rawsamplenames = get_rawsamples_list(samples_dict)
        primers_dict = get_primers(self.paramsdict["Primerfile"])
        number_cores = multiprocessing.cpu_count()-1
        logs = {"Parallel" : self.performance,
                "NumberCores" : number_cores,
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


        if (self.checkbox_states_pipeline_advanced["LengthExtraction"] == 1):
            run_Length_Extraction_GUI(self.textbox_pipeline, self.paramsdict)
            logs["LengthExtraction"]["Time"] = t.lap()
            self.textbox_pipeline.insert("end", f"\nTime spent: {logs["LengthExtraction"]["Time"]:.4g}.\n")
        if (self.checkbox_states_pipeline_advanced["ConsensusSequence"] == 1):
            RunConsensusAll_GUI(self.textbox_pipeline, self.paramsdict, self.performance, self.number_cores)
            logs["ConsensusSeqs"]["Time"] = t.lap()
            self.textbox_pipeline.insert("end", f"\nTime spent: {logs["ConsensusSeqs"]["Time"]:.4g}.\n")
        if (self.checkbox_states_pipeline_advanced["AlleleDetection"] == 1):
            RunVariants_Determination_GUI(self.textbox_pipeline, self.paramsdict)
            logs["NCorrection"]["Time"] = t.lap()
            self.textbox_pipeline.insert("end", f"\nTime spent: {logs["NCorrection"]["Time"]:.4g}.\n")
        if (self.checkbox_states_pipeline_advanced["AlleleCall"] == 1):
            run_Allele_Call_GUI(self.textbox_pipeline, self.paramsdict)
            logs["AlleleCall"]["Time"] = t.lap()
            self.textbox_pipeline.insert("end", f"\nTime spent: {logs["AlleleCall"]["Time"]:.4g}.\n")




        self.add_dots_pipelinetextbox = False
        self.textbox_pipeline.insert('end-1c', "\n\nTotal Time spent: " + str(t.total()) + "s \n\n")

        logs["Total"]["Time"] = t.total()
        # logs["Total"]["Time"] = end - start

        logs_path = Path(self.paramsdict["Outputfolder"]) / "logs_script2.json"
        with open(logs_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)
    

    def append_period(self):
        self.textbox_pipeline.insert('end-1c', ".")
        if self.add_dots_pipelinetextbox:
            self.after(1000, self.append_period)