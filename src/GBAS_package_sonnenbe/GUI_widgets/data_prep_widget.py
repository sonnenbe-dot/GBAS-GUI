from tkinter import ttk, filedialog, font
import tkinter as tk
import customtkinter as ctk
from pathlib import Path
import re, shutil

from GBAS_package_sonnenbe.helper_functions.gui_helpers import browse_dir, browse_file

class data_prep_window(tk.Toplevel):
    def __init__(self, parent, samplefilepath : Path, rawdatafilepath : Path, current_workspace : Path, params : dict, on_done):
        super().__init__(parent)

        self.on_done = on_done

        self.samplefilepath = samplefilepath
        self.rawdatafilepath = rawdatafilepath
        self.current_workspace = current_workspace
        self.params = params

        self.title("General Parameters")
        self.transient(parent)
        self.focus_set()
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.build_window()

        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.bind('<Return>', lambda event: self.closing())
    
    def closing(self):
        try:
            self.on_done(self.rawdatafilepath)
        finally:
            self.destroy()
    
    def build_window(self):
        logo_upper = ctk.CTkLabel(self, text="Import Samples", font=ctk.CTkFont(size=20, weight="bold"))
        logo_upper.grid(row=0, column=0, padx=20, pady=(20, 20))

        frame_upper = ctk.CTkFrame(self, width=100, corner_radius=2)
        frame_upper.grid(row=1, column=0, rowspan=1, sticky="nsew")
        frame_upper.grid_columnconfigure(0, weight=1)
        frame_upper.grid_columnconfigure(1, weight=1)
        frame_upper.grid_columnconfigure(2, weight=1)
        frame_upper.grid_rowconfigure(0, weight=0)

        frame_lower = ctk.CTkFrame(self, width=100, corner_radius=2)
        frame_lower.grid(row=2, column=0, rowspan=1, sticky="nsew")

        ctk.CTkLabel(frame_upper, text="Rawdata:", width=20, font=ctk.CTkFont(size=15, weight="bold")).grid(column=0, row=0, padx=5, pady=5)
        rawdata_entry = ctk.CTkEntry(frame_upper, corner_radius=5)
        ctk.CTkButton(frame_upper, text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = rawdata_entry, dir_param = self.params["Outputfolder"] : browse_dir(entry, dir_param)).grid(column=2, row=0, padx=5, pady=5)
        rawdata_entry.insert(tk.END, str(self.rawdatafilepath))
        rawdata_entry.grid(column=1, row=0, padx=5, pady=5)

        ctk.CTkLabel(frame_upper, text="Samplesheet:", width=20, font=ctk.CTkFont(size=15, weight="bold")).grid(column=0, row=1, padx=5, pady=5)
        sample_entry = ctk.CTkEntry(frame_upper, corner_radius=5)
        ctk.CTkButton(frame_upper, text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = sample_entry, dir_param = self.params["Outputfolder"] : browse_file(entry, dir_param)).grid(column=2, row=1, padx=5, pady=5)
        sample_entry.insert(tk.END, str(self.samplefilepath))
        sample_entry.grid(column=1, row=1, padx=5, pady=5)

        ctk.CTkLabel(frame_upper, text="Output:", width=20, font=ctk.CTkFont(size=15, weight="bold")).grid(column=0, row=2, padx=5, pady=5)
        sample_output = ctk.CTkEntry(frame_upper, corner_radius=5)
        ctk.CTkButton(frame_upper, text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = sample_output, dir_param = self.params["Outputfolder"] : browse_dir(entry, dir_param)).grid(column=2, row=2, padx=5, pady=5)
        sample_output.insert(tk.END, "")
        sample_output.grid(column=1, row=2, padx=5, pady=5)


        ctk.CTkButton(frame_lower, text="Import", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda rawdata_entry = rawdata_entry, sample_entry = sample_entry, sample_output = sample_output : self.import_samples(rawdata_entry, sample_entry, sample_output)).grid(column=1, row=0, padx=5, pady=5)


    def import_samples(self, rawdata_entry, sample_entry, sample_output):
        samples = self.get_samples(Path(sample_entry.get()))
        self.copy_paste_samples(samples, Path(rawdata_entry.get()), Path(sample_output.get()))
        #self.samplefilepath = Path(sample_entry.get())
        self.rawdatafilepath = Path(sample_output.get())
    



    def get_samples(self, samplesheetpath : Path) -> dict:
        samples = {}
        with samplesheetpath.open("r") as samplefile:
            lines = samplefile.readlines()
            for line in lines:
                line = line.rstrip("\r\n")
                samplename_raw = re.split(',|\t|;', line)[0].strip()
                if (samplename_raw not in samples):
                    samples[samplename_raw] = 0
                samples[samplename_raw] += 1
        return samples

    def copy_paste_samples(self, samples : dict, rawfilepath : Path, outputpath : Path) -> dict:
        samples_already_inside = {}
        outputpath.mkdir(parents=True, exist_ok=True)
        for path in rawfilepath.rglob("*"):
            if path.is_file():
                filename = path.stem
                samplename_raw = filename.split("_")[0]
                if (samplename_raw in samples):
                    output_path = outputpath / path.name
                    #if (output_path.exists()):
                    shutil.copy2(path, output_path)
                    print(f"Copied {path} → {output_path}")
                    # if (not output_path.exists()):
                    #     shutil.copy2(path, output_path)
                    #     print(f"Copied {path} → {output_path}")
                    #     samples_already_inside[path.name] = 0
                    # samples_already_inside[path.name] += 1
        return samples_already_inside