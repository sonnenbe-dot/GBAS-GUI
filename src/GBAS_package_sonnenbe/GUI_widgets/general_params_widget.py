import customtkinter as ctk
from tkinter import ttk, filedialog, font
import tkinter as tk
import os, platform
from pathlib import Path

from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import write_parameterfile
from GBAS_package_sonnenbe.helper_functions.gui_helpers import browse_dir, browse_file


class general_params_window(tk.Toplevel):
    def __init__(self, parent, parameterfilepath : Path, current_workspace : Path, params : dict, frametitle_leftupper : str, frametitle_leftlower : str, frametitle_rightupper : str, frametitle_rightlower : str, elements_leftupper : list, elements_leftlower : list, elements_rightupper : list, elements_rightlower : list, on_done):
        super().__init__(parent)

        self.on_done = on_done

        self.title("General Parameters")
        self.transient(parent)
        self.focus_set()
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.current_workspace = current_workspace
        self.params = params

        self.parameterfilepath = parameterfilepath

        self.frametitle_leftupper = frametitle_leftupper
        self.frametitle_leftlower = frametitle_leftlower
        self.frametitle_rightupper = frametitle_rightupper
        self.frametitle_rightlower = frametitle_rightlower

        self.elements_leftupper = elements_leftupper
        self.elements_leftlower = elements_leftlower
        self.elements_rightupper = elements_rightupper
        self.elements_rightlower = elements_rightlower



        #self.entries = []

        self.build_window()

        #self.bind('<Return>', lambda event: self.destroy())

        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.bind('<Return>', lambda event: self.closing())
    
    def closing(self):
        # hand the value back before destroying
        try:
            self.on_done(self.parameterfilepath)
        finally:
            self.destroy()

    def return_params(self):
        return self.parameterfilename, self.params
    
    def build_window(self):
        logo_leftupper = ctk.CTkLabel(self, text=self.frametitle_leftupper+":", font=ctk.CTkFont(size=20, weight="bold"))
        logo_leftupper.grid(row=0, column=0, padx=20, pady=(20, 20))

        params_leftupper = ctk.CTkFrame(self, width=100, corner_radius=2)
        params_leftupper.grid(row=1, column=0, rowspan=1, sticky="nsew")
        for i in range(0, len(self.elements_leftupper), 1):
            params_leftupper.grid_rowconfigure(i, weight=1)
        params_leftupper.grid_columnconfigure(0, weight=1)
        params_leftupper.grid_columnconfigure(1, weight=1)


        logo_leftlower = ctk.CTkLabel(self, text=self.frametitle_leftlower+":", font=ctk.CTkFont(size=20, weight="bold"))
        logo_leftlower.grid(row=2, column=0, padx=20, pady=(20, 20))

        params_leftlower = ctk.CTkFrame(self, width=100, corner_radius=2)
        params_leftlower.grid(row=3, column=0, rowspan=1, sticky="nsew")
        for i in range(0, len(self.elements_leftlower), 1):
            params_leftlower.grid_rowconfigure(i, weight=1)
        params_leftlower.grid_columnconfigure(0, weight=1)
        params_leftlower.grid_columnconfigure(1, weight=1)

        logo_rightupper = ctk.CTkLabel(self, text=self.frametitle_rightupper+":", font=ctk.CTkFont(size=20, weight="bold"))
        logo_rightupper.grid(row=0, column=1, padx=20, pady=(20, 20))

        params_rightupper = ctk.CTkFrame(self, width=100, corner_radius=2)
        params_rightupper.grid(row=1, column=1, rowspan=1, sticky="nsew")
        for i in range(0, len(self.elements_rightupper), 1):
            params_rightupper.grid_rowconfigure(i, weight=1)
        params_rightupper.grid_columnconfigure(0, weight=1)
        params_rightupper.grid_columnconfigure(1, weight=1)

        logo_rightlower = ctk.CTkLabel(self, text=self.frametitle_rightlower+":", font=ctk.CTkFont(size=20, weight="bold"))
        logo_rightlower.grid(row=2, column=1, padx=20, pady=(20, 20))

        params_rightlower = ctk.CTkFrame(self, width=100, corner_radius=2)
        params_rightlower.grid(row=3, column=1, rowspan=1, sticky="nsew")
        for i in range(0, len(self.elements_rightlower), 1):
            params_rightlower.grid_rowconfigure(i, weight=1)
        params_rightlower.grid_columnconfigure(0, weight=1)
        params_rightlower.grid_columnconfigure(1, weight=1)

        database_frame = ctk.CTkFrame(self, width=100, corner_radius=2)
        database_frame.grid(row=4, columnspan=2, rowspan=1, sticky="nsew")
        database_frame.grid_rowconfigure(0, weight=1)
        database_frame.grid_columnconfigure(0, weight=0)
        database_frame.grid_columnconfigure(1, weight=1)
        database_frame.grid_columnconfigure(2, weight=0)

        parameterfile_frame = ctk.CTkFrame(self, width=100, corner_radius=2)
        parameterfile_frame.grid(row=5, columnspan=2, rowspan=1, sticky="nsew")
        parameterfile_frame.grid_rowconfigure(0, weight=1)
        parameterfile_frame.grid_columnconfigure(0, weight=1)
        parameterfile_frame.grid_columnconfigure(1, weight=1)
        #parameterfile_frame.grid_columnconfigure(2, weight=1)

        entries = []
        custom_font_button =("Times",13,'roman')


        list_frames = [(self.elements_leftupper, params_leftupper), (self.elements_leftlower, params_leftlower), (self.elements_rightupper, params_rightupper), (self.elements_rightlower, params_rightlower)]

        for frame_element in list_frames:
            for i, param in enumerate(frame_element[0]):
                ctk.CTkLabel(frame_element[1], text=param + ":", width=20).grid(column=0, row=i, padx=5, pady=5)
                param_entry = ctk.CTkEntry(frame_element[1], corner_radius=5) #, textvariable=text
                if (frame_element[1] == params_leftupper):
                    ctk.CTkButton(frame_element[1], text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = param_entry, dir_param = self.params["Outputfolder"] : browse_dir(entry, dir_param)).grid(column=2, row=i, padx=5, pady=5)
                elif (frame_element[1] == params_leftlower):
                    ctk.CTkButton(frame_element[1], text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = param_entry, dir_param = self.params["Outputfolder"] : browse_file(entry, dir_param)).grid(column=2, row=i, padx=5, pady=5)
                # if (not(frame_element[1] == params_rightupper) and not(frame_element[1] == params_rightlower)):
                #     if (Path(self.params[param]).is_dir()):
                #         ctk.CTkButton(frame_element[1], text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = param_entry, dir_param = self.params["Outputfolder"] : self.browse_dir(entry, dir_param)).grid(column=2, row=i, padx=5, pady=5)
                #     elif (Path(self.params[param]).is_file()):
                #         ctk.CTkButton(frame_element[1], text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = param_entry, dir_param = self.params["Outputfolder"] : self.browse_file(entry, dir_param)).grid(column=2, row=i, padx=5, pady=5)
                # if (not(isinstance(self.params[param], int))):
                #     tk.Button(frame_element[1], text="Browse", command=lambda entry = param_entry: self.browse_dir(entry)).grid(column=2, row=i, padx=5, pady=5)
                # elif (isinstance(self.params[param], str) and Path(self.params[param]).is_file()):
                #     tk.Button(frame_element[1], text="Browse", command=lambda entry = param_entry: self.browse_file(entry)).grid(column=2, row=i, padx=5, pady=5)
                # if (isinstance(self.params[param], str) and Path(self.params[param]).is_dir()):
                #     tk.Button(frame_element[1], text="Browse", command=lambda entry = param_entry: self.browse_dir(entry)).grid(column=2, row=i, padx=5, pady=5)
                # elif (isinstance(self.params[param], str) and Path(self.params[param]).is_file()):
                #     tk.Button(frame_element[1], text="Browse", command=lambda entry = param_entry: self.browse_file(entry)).grid(column=2, row=i, padx=5, pady=5)
                param_entry.insert(tk.END, self.params[param])
                param_entry.grid(column=1, row=i, padx=5, pady=5)
                entries.append((param, param_entry))
        

        ctk.CTkLabel(database_frame, text="Databasefilepath:", width=20, font=ctk.CTkFont(size=15, weight="bold")).grid(column=0, row=0, sticky="w", padx=5, pady=5)
        database_entry = ctk.CTkEntry(database_frame, corner_radius=5)
        ctk.CTkButton(database_frame, text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = database_entry, dir_param = self.params["Outputfolder"] : browse_file(entry, dir_param)).grid(column=2, row=0, sticky="e", padx=5, pady=5)
        database_entry.insert(tk.END, self.params["Database"])
        database_entry.grid(column=1, row=0, padx=5, pady=5)
        entries.append(("Database", database_entry))


        ctk.CTkLabel(parameterfile_frame, text="Parameterfilepath:", width=20, font=ctk.CTkFont(size=15, weight="bold")).grid(column=0, row=0, padx=5, pady=5)
        #ctk.CTkButton(parameterfile_frame, text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = param_entry, dir_param = self.params["Outputfolder"] : self.browse_file(entry, dir_param)).grid(column=2, row=0, padx=5, pady=5)
        parameterfile_entry = ctk.CTkEntry(parameterfile_frame, corner_radius=5)
        #ctk.CTkButton(parameterfile_frame, text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = parameterfile_entry, dir_param = self.params["Outputfolder"] : self.browse_file(entry, dir_param)).grid(column=2, row=0, padx=5, pady=5)
        parameterfile_entry.insert(tk.END, str(self.parameterfilepath))
        parameterfile_entry.grid(column=1, row=0, padx=5, pady=5)
    
        ctk.CTkButton(self, border_width=2, corner_radius=4, text="Save Params", fg_color=("blue", "gray75"),  command = lambda x1 = entries, x2 = parameterfile_entry : self.write_params(x1, x2)).grid(column=1, row=6, sticky="se", padx=15, pady=4)
        ctk.CTkButton(self, border_width=2, corner_radius=4, text="Update Params", fg_color=("blue", "gray75"), command = lambda x1 = entries, x2 = parameterfile_entry : self.set_params(x1, x2)).grid(column=0, row=6, sticky="sw", padx=15, pady=4)

    def write_params(self, entries, parameterfilename_entry):
        self.set_params(entries, parameterfilename_entry)
        #print(str(self.current_workspace) + "/" + self.parameterfilename + ".txt")
        write_parameterfile(self.paramsdict, str(self.parameterfilepath))
        #write_parameterfile(self.paramsdict, str(self.current_workspace) + "/" + self.parameterfilename + ".txt")

    def set_params(self, entries, parameterfile_entry):
        self.paramsdict = {entry[0] : entry[1].get() for entry in entries}
        self.parameterfilepath = parameterfile_entry.get()
        #print(self.paramsdict)
    

    # def browse_dir(self, entry, dir_param):
    #     directory_path = Path(filedialog.askdirectory(initialdir=dir_param, title="Select folder!"))
    #     entry.delete(0, tk.END)  # Clear the entry
    #     entry.insert(0, str(directory_path))  # Insert the file/folder path into the entry

    # def browse_file(self, entry, dir_param):
    #     file_path = Path(filedialog.askopenfilename(initialdir=dir_param, title="Select file!"))
    #     entry.delete(0, tk.END)  # Clear the entry
    #     entry.insert(0, str(file_path))  # Insert the file/folder path into the entry
