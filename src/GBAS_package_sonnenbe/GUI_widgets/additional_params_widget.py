from tkinter import ttk, filedialog, font
import tkinter as tk
import customtkinter as ctk
from pathlib import Path

class additional_params_window(tk.Toplevel):
    def __init__(self, parent, high_performance : bool, zipping_files : bool, likelihood_approach : bool, on_done):
        super().__init__(parent)

        self.on_done = on_done

        self.high_performance = high_performance
        self.zipping_files = zipping_files
        self.likelihood_approach = likelihood_approach
        self.checkbox_high_performance = 1
        self.checkbox_zipping_files = 1
        self.checkbox_likelihood_approach = 1
        if (not(self.high_performance)):
            self.checkbox_high_performance = 0
        if (not(self.zipping_files)):
            self.checkbox_zipping_files = 0
        if (not(self.likelihood_approach)):
            self.checkbox_likelihood_approach = 0

        self.checkboxes_additional = []

        self.title("Additional Parameters")
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
            self.on_done(self.checkboxes_additional[0].get(), self.checkboxes_additional[1].get(), self.checkboxes_additional[2].get())
        finally:
            self.destroy()
    
    def build_window(self):
        ctk.CTkLabel(self, text="Additional Parameters", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 20))
        
        additional_input_settings = ctk.CTkFrame(self, width=100, corner_radius=2)
        additional_input_settings.grid(row=1, column=0, rowspan=1, sticky="nsew")
        additional_input_settings.grid_columnconfigure(0, weight=1)
        additional_input_settings.grid_columnconfigure(1, weight=1)
        additional_input_settings.grid_columnconfigure(2, weight=1)
        additional_input_settings.grid_rowconfigure(0, weight=1)
        additional_input_settings.grid_rowconfigure(1, weight=1)
        
        
        checkbox_performance_var = tk.IntVar(value = self.checkbox_high_performance)
        checkbox_performance = ctk.CTkCheckBox(additional_input_settings, text="High Performance", variable=checkbox_performance_var)
        checkbox_performance.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="w")
        self.checkboxes_additional.append(checkbox_performance)

        checkbox_zipping_var = tk.IntVar(value = self.checkbox_zipping_files)
        checkbox_zipping = ctk.CTkCheckBox(additional_input_settings, text="Zipping Files", variable=checkbox_zipping_var)
        checkbox_zipping.grid(row=2, column=0, padx=10, pady=(5, 5), sticky="w")
        self.checkboxes_additional.append(checkbox_zipping)

        likelihood_approach_var = tk.IntVar(value = self.likelihood_approach)
        checkbox_likelihood_approach = ctk.CTkCheckBox(additional_input_settings, text="Likelihood Approach", variable=likelihood_approach_var)
        checkbox_likelihood_approach.grid(row=3, column=0, padx=10, pady=(5, 5), sticky="w")
        self.checkboxes_additional.append(checkbox_likelihood_approach)