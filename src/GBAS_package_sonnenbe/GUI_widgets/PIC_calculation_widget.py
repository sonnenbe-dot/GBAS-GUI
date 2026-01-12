import customtkinter as ctk
from pathlib import Path
import tkinter as tk
import threading

from GBAS_package_sonnenbe.helper_functions.gui_helpers import browse_dir, browse_file

from GBAS_package_sonnenbe.main_functions.PIC_calculation import calculate_PIC


def main():

    return 0



class PIC_calculation_window(tk.Toplevel):
    def __init__(self, parent, current_workspace : Path, paramsdict : dict, filtering_param : float, on_done):
        super().__init__(parent)

        self.on_done = on_done
        self.filtering_param = filtering_param

        self.title("Calculate PIC")
        self.transient(parent)
        self.focus_set()
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.current_workspace = current_workspace
        self.params = paramsdict



        #self.entries = []

        #Testing:
        self.inputpath = Path("E:\\Work_Paper_GUI\\PIC\\test_folder")
        self.outputfolderpath = Path("E:\\Work_Paper_GUI\\PIC\\output")

        self.build_window()

        #self.bind('<Return>', lambda event: self.destroy())

        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.bind('<Return>', lambda event: self.closing())
    
    def closing(self):
        # hand the value back before destroying
        try:
            self.on_done("Pipeline has not started:")
        finally:
            self.destroy()

    
    def build_window(self):
        logo_upper = ctk.CTkLabel(self, text="Calculating PIC", font=ctk.CTkFont(size=20, weight="bold"))
        logo_upper.grid(row=0, column=0, padx=20, pady=(20, 20))

        frame_upper = ctk.CTkFrame(self, width=100, corner_radius=2)
        frame_upper.grid(row=1, column=0, columnspan=3, rowspan=1, sticky="nsew")
        frame_upper.grid_columnconfigure(0, weight=1)
        frame_upper.grid_columnconfigure(1, weight=1)
        frame_upper.grid_columnconfigure(2, weight=1)
        frame_upper.grid_rowconfigure(0, weight=0)

        textbox_frame = ctk.CTkFrame(self, width=100, corner_radius=2)
        textbox_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")  # Expanding this row
        textbox_frame.grid_columnconfigure(0, weight=1)
        textbox_frame.grid_rowconfigure(0, weight=1)

        #frame_lower = ctk.CTkFrame(self, width=100, corner_radius=2)
        #frame_lower.grid(row=3, column=0, rowspan=1, sticky="nsew")

        ctk.CTkLabel(frame_upper, text="Inputfolder:", width=20, font=ctk.CTkFont(size=15, weight="bold")).grid(column=0, row=0, padx=5, pady=5)
        input_entry = ctk.CTkEntry(frame_upper, corner_radius=5)
        ctk.CTkButton(frame_upper, text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = input_entry, dir_param = self.params["Outputfolder"] : browse_dir(entry, dir_param)).grid(column=2, row=0, padx=5, pady=5)
        input_entry.insert(tk.END, str(self.inputpath))
        input_entry.grid(column=1, row=0, padx=5, pady=5)

        ctk.CTkLabel(frame_upper, text="Outputfolder:", width=20, font=ctk.CTkFont(size=15, weight="bold")).grid(column=0, row=1, padx=5, pady=5)
        output_entry = ctk.CTkEntry(frame_upper, corner_radius=5)
        ctk.CTkButton(frame_upper, text="Browse", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda entry = output_entry, dir_param = self.params["Outputfolder"] : browse_dir(entry, dir_param)).grid(column=2, row=1, padx=5, pady=5)
        output_entry.insert(tk.END, str(self.outputfolderpath))
        output_entry.grid(column=1, row=1, padx=5, pady=5)

         # Textbox for Comparison Output
        self.PC_calc_textbox = ctk.CTkTextbox(textbox_frame, width=250)
        self.PC_calc_textbox.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=(5, 5))  # Ensure it's in row 0 inside the frame
        self.PC_calc_textbox.insert("0.0", "Check the official documentation for the structure of the inputfolder for the PIC calculation!" + "\n\n" * 2)

        


        ctk.CTkButton(self, text="Calculate PIC", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda input_entry = input_entry, output_entry = output_entry : self.calculating_PIC_threading(input_entry, output_entry)).grid(column=1, row=3, sticky="se", padx=5, pady=5)
        ctk.CTkButton(self, text="Check Inputs", width=70, height=25, font=ctk.CTkFont(size=14), text_color="black", fg_color = "#add8e6", hover_color="#87ceeb", command=lambda input_entry = input_entry, output_entry = output_entry : self.check_input_threading(input_entry, output_entry)).grid(column=0, row=3, sticky="sw", padx=5, pady=5)

        #ctk.CTkButton(self, border_width=2, corner_radius=4, text="Save Params", fg_color=("blue", "gray75"),  command = lambda x1 = entries, x2 = parameterfile_entry : self.write_params(x1, x2)).grid(column=1, row=6, sticky="se", padx=15, pady=4)
        #ctk.CTkButton(self, border_width=2, corner_radius=4, text="Update Params", fg_color=("blue", "gray75"), command = lambda x1 = entries, x2 = parameterfile_entry : self.set_params(x1, x2)).grid(column=0, row=6, sticky="sw", padx=15, pady=4)

    def check_input_threading(self, input_entry, output_entry):
        self.inputpath = Path(input_entry.get())
        self.outputfolderpath = Path(output_entry.get())
        thread = threading.Thread(target=self.check_input)
        thread.start()
    
    def check_input(self):
        self.PC_calc_textbox.delete(0.0, 'end')
        self.PC_calc_textbox.insert('end-1c', "Checking input folder format.\n\n Projects:\n\n")
        project_names = []
        
        bool_primers = True
        bool_subfolder_length = True
        bool_subfolder_sequence = True

        for folderpath in self.inputpath.iterdir():
            if (folderpath.is_dir()):
                self.PC_calc_textbox.insert('end-1c', f"{folderpath.name}\n")
                project_names.append(folderpath.name)

        for folderpath in self.inputpath.iterdir():
            if (folderpath.is_dir()):
                for path in folderpath.iterdir():
                    primerpath = path / "primers.txt"
                    if (not(primerpath.exists)):
                        bool_primers = False
                    lengthpath = path / "length_matrices"
                    if (not(lengthpath.exists)):
                        bool_subfolder_length = False
                    sequencepath = path / "allele_matrices"
                    if (not(sequencepath.exists)):
                        bool_subfolder_sequence = False
        
                if (not(bool_primers)):
                    self.PC_calc_textbox.insert('end-1c', f"No file 'primers.txt' in project {path.name}.\n")
                    break
                if (not(bool_subfolder_length)):
                    self.PC_calc_textbox.insert('end-1c', f"No subfolder 'length_matrices' in project {path.name}.\n")
                    break
                if (not(bool_subfolder_sequence)):
                    self.PC_calc_textbox.insert('end-1c', f"No subfolder 'allele_matrices' in project {path.name}.\n")
                    break
                
        if (bool_primers and bool_subfolder_length and bool_subfolder_sequence):
            self.PC_calc_textbox.insert('end-1c', f"\n\nInput folder is in correct format, PIC calculation can proceed!\n")


    

    def calculating_PIC_threading(self, input_entry, output_entry):
        self.inputpath = Path(input_entry.get())
        self.outputfolderpath = Path(output_entry.get())
        thread = threading.Thread(target=self.calculating_PIC)
        thread.start()
    
    def calculating_PIC(self):
        self.PC_calc_textbox.delete(0.0, 'end')
        self.PC_calc_textbox.insert('end-1c', f"\nInputfolder:\n{self.inputpath}\nOutputfolder:\n{self.outputfolderpath}\n\n")
        self.PC_calc_textbox.insert('end-1c', "Calculating PIC value.\n")
        self.add_dots_pipelinetextbox = True
        self.append_period()
        calculate_PIC(self.inputpath, self.outputfolderpath, self.filtering_param)

        self.add_dots_pipelinetextbox = False
        self.PC_calc_textbox.insert('end-1c', "\nFinished Calculating PIC value.\n")
    
    def append_period(self):
        self.PC_calc_textbox.insert('end-1c', ".")
        if self.add_dots_pipelinetextbox:
            self.after(1000, self.append_period)


if __name__ == "__main__":
    main()