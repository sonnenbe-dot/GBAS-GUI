import customtkinter as ctk
from pathlib import Path
import tkinter as tk
import threading, json
from tkinter import ttk

import csv

from GBAS_package_sonnenbe.main_functions.database_class import local_database_sqlite

def main():

    return 0

class extract_subset_window(tk.Toplevel):
    def __init__(self, parent, current_workspace : Path, paramsdict : dict, checkbox_states_include_dict : dict, checkbox_states_dict2 : dict, textbox_pipeline : ctk.CTkTextbox,  on_done):
        super().__init__(parent)

        self.on_done = on_done
        self.workspace = current_workspace
        self.paramsdict = paramsdict
        self.textbox_pipeline = textbox_pipeline

        self.title("Extract Subset Window")
        self.transient(parent)
        self.focus_set()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=1)

        self.db_instance = None

        # self.checkbox_states = []
        # self.checkbox_states_dict = {}
        # self.checkbox_states_include_dict = {}

        # self.checkbox_states_dict2 = {}
        # self.checkbox_states_dict2["Project"] = {}
        # self.checkbox_states_dict2["Metadata2"] = {}
        # self.checkbox_states_dict2["Loci"] = {}

        self.checkbox_states = []
        self.checkbox_states_dict = {}

        self.checkbox_states_include_dict = checkbox_states_include_dict
        self.checkbox_states_dict2 = checkbox_states_dict2

        self.checkboxes_project_include = []
        self.values_project_include = []

        self.checkboxes_metadata2_include = []
        self.values_metadata2_include = []

        self.checkboxes_loci_include = []
        self.values_loci_include = []

        self.build_window()


        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.bind('<Return>', lambda event: self.closing())

    def build_window(self):
        self.db_instance = local_database_sqlite(self.paramsdict["Database"])
        self.db_instance.create_tables()

        project_frame = ctk.CTkFrame(self, width=50, corner_radius=2)
        project_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        project_frame.grid_columnconfigure(0, weight=1)
        project_frame.grid_rowconfigure(0, weight = 0)
        project_frame.grid_rowconfigure(1, weight = 1)
        
        logo_project_include = ctk.CTkLabel(project_frame, text="Include Project", font=ctk.CTkFont(size=20, weight="bold"))
        logo_project_include.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        project_scrollframe_include = ctk.CTkScrollableFrame(project_frame, width=50, corner_radius=2)
        project_scrollframe_include.grid(row=1, column=0, rowspan=1, sticky="nsew")
        project_scrollframe_include.grid_columnconfigure(0, weight=1)
        
        search_var_project_include = tk.StringVar()
        search_entry_project_include = ctk.CTkEntry(project_scrollframe_include, textvariable=search_var_project_include)
        search_entry_project_include.grid(row=0, column=0, padx=10, pady=(5, 5), sticky="w")
        
        
        checkboxes_project_include = []
        query = "SELECT DISTINCT projectname, ploidy FROM table_project"
        rows_projects = self.db_instance.get_rows(query)

        self.values_project_include = [project[0] for project in rows_projects]
        #self.values_project_include = ["sample1", "sample2", "sample3", "sample4", "sample5", "sample6", "sample7"]
        for i, value in enumerate(self.values_project_include):
            state = self.checkbox_states_include_dict.get(value, 1)
            
            checkbox_var = tk.IntVar(value=state)
            checkbox = ctk.CTkCheckBox(project_scrollframe_include, text=value, variable=checkbox_var)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(5, 5), sticky="w")
            self.checkboxes_project_include.append(checkbox)
            if (checkbox.get() == 1):
                checkboxes_project_include.append(checkbox.cget("text"))
        
        search_var_project_include.trace_add("write", lambda *args: self.updating_checkboxes(self.checkboxes_project_include, self.values_project_include, search_var_project_include, project_scrollframe_include))


        separator1 = tk.Canvas(self, width=2, bg='black')
        separator1.grid(row=0, column=1, sticky='ns')
        separator1.create_line(1, 0, 1, separator1.winfo_height())


        metadata2 = ctk.CTkFrame(self, width=50, corner_radius=2)
        metadata2.grid(row=0, column=2, rowspan=4, sticky="nsew")
        metadata2.grid_columnconfigure(0, weight=1)
        metadata2.grid_rowconfigure(0, weight = 0)
        metadata2.grid_rowconfigure(1, weight = 1)
        

        
        
        
        
        logo_metadata2_include = ctk.CTkLabel(metadata2, text="Include Metadata2", font=ctk.CTkFont(size=20, weight="bold"))
        logo_metadata2_include.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        metadata2_scrollframe_include = ctk.CTkScrollableFrame(metadata2, width=50, corner_radius=2)
        metadata2_scrollframe_include.grid(row=1, column=0, rowspan=1, sticky="nsew")
        metadata2_scrollframe_include.grid_columnconfigure(0, weight=1)

        search_var_metadata2_include = tk.StringVar()
        search_entry_metadata2_include = ctk.CTkEntry(metadata2_scrollframe_include, textvariable=search_var_metadata2_include)
        search_entry_metadata2_include.grid(row=0, column=0, padx=10, pady=(5, 5), sticky="w")
        
        query = "SELECT DISTINCT Metadata2 FROM table_sample"
        rows_metadata2 = self.db_instance.get_rows(query)
        
        checkboxes_metadata2_include = []
        #self.values_organism_include = ["organism1", "organism2", "organism3", "organism4"] #call from database
        self.values_metadata2_include = [meta[0] for meta in rows_metadata2]
        for i, value in enumerate(self.values_metadata2_include):
            state = self.checkbox_states_include_dict.get(value, 1)
    
            checkbox_var = tk.IntVar(value=state)
            checkbox = ctk.CTkCheckBox(metadata2_scrollframe_include, text=value, variable=checkbox_var)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(5, 5), sticky="w")
            self.checkboxes_metadata2_include.append(checkbox)
            if (checkbox.get() == 1):
                checkboxes_metadata2_include.append(checkbox.cget("text"))
        
        search_var_metadata2_include.trace_add("write", lambda *args: self.updating_checkboxes(self.checkboxes_metadata2_include, self.values_metadata2_include, search_var_metadata2_include, metadata2_scrollframe_include))  



        separator2 = tk.Canvas(self, width=2, bg='black')
        separator2.grid(row=0, column=3, sticky='ns')
        separator2.create_line(1, 0, 1, separator1.winfo_height())
        
        
        
        loci = ctk.CTkFrame(self, width=50, corner_radius=2)
        loci.grid(row=0, column=4, rowspan=4, sticky="nsew")
        loci.grid_columnconfigure(0, weight=1)
        loci.grid_rowconfigure(0, weight = 0)
        loci.grid_rowconfigure(1, weight = 1)
        
        logo_loci_include = ctk.CTkLabel(loci, text="Include Loci", font=ctk.CTkFont(size=20, weight="bold"))
        logo_loci_include.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        loci_scrollframe_include = ctk.CTkScrollableFrame(loci, width=50, corner_radius=2)
        loci_scrollframe_include.grid(row=1, column=0, rowspan=1, sticky="nsew")
        loci_scrollframe_include.grid_columnconfigure(0, weight=1)
        
        search_var_loci_include = tk.StringVar()
        search_entry_loci_include = ctk.CTkEntry(loci_scrollframe_include, textvariable=search_var_loci_include)
        search_entry_loci_include.grid(row=0, column=0, padx=10, pady=(5, 5), sticky="w")
        
        
        query = "SELECT DISTINCT Locusname FROM table_loci"
        rows_loci = self.db_instance.get_rows(query)
        
        checkboxes_loci_include = []
        #self.values_loci_include = ["locus1", "locus2", "locus3", "locus4", "locus5", "locus6", "locus7"]
        self.values_loci_include = [loci[0] for loci in rows_loci]
        for i, value in enumerate(self.values_loci_include):
            state = self.checkbox_states_include_dict.get(value, 1)
            
            checkbox_var = tk.IntVar(value=state)
            checkbox = ctk.CTkCheckBox(loci_scrollframe_include, text=value, variable=checkbox_var)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(5, 5), sticky="w")
            self.checkboxes_loci_include.append(checkbox)
            if (checkbox.get() == 1):
                checkboxes_loci_include.append(checkbox.cget("text"))
        
        
        
        search_var_loci_include.trace_add("write", lambda *args: self.updating_checkboxes(self.checkboxes_loci_include, self.values_loci_include, search_var_loci_include, loci_scrollframe_include)) 

        ctk.CTkButton(self, border_width=2, corner_radius=4, text="Download Subset", fg_color=("blue", "gray75"), command = self.get_subset_output).grid(column=0, row=5, sticky="nsew", padx=15, pady=4)
        ctk.CTkButton(self, border_width=2, corner_radius=4, text="Download Genalex", fg_color=("blue", "gray75"), command = self.get_genalex_output).grid(column=4, row=5, sticky="nsew", padx=15, pady=4)

    def set_subset(self):
        self.updating_parameter_checkboxes()
        return self.checkbox_states_dict2["Project"], self.checkbox_states_dict2["Metadata2"], self.checkbox_states_dict2["Loci"]

    def get_subset_output(self):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Generating output from chosen subset.\n")

        project_include, metadata2_include, loci_include = self.set_subset()

        print("HERE\n")
        print(project_include)
        print(metadata2_include)
        print(loci_include)

        rows_projects_include = self.db_instance.get_selected_projects(project_include)
        print(rows_projects_include)

        # query = "SELECT projectname, ploidy FROM table_project"
        # rows_projects = self.db_instance.get_rows(query)

        self.db_instance.get_view_for_extracting()

        # query = "SELECT SampleID, projectname, ploidy, Locusname FROM view_extraction"
        # rows = self.db_instance.get_rows(query)
        #print("\nHERE2\n")
        #print(rows)

        rows_specified = self.db_instance.get_selected_loci_project_metadata(project_include, metadata2_include, loci_include)
        print("Subset rows:\n")
        print(rows_specified)

        # output_dir_path = self.workspace / ("subset_output")
        # if (not output_dir_path.exists()):
        #     output_dir_path.mkdir(parents=True, exist_ok=True)

        # subset_matrix_dict = {}
        # dict_path = output_dir_path / ("subset.json")
        # loci_list = []

        # for project_row in rows_projects_include:
        #     subset_matrix_dict[project_row[0]] = {}
        #     subset_matrix_dict[project_row[0]]["Projectname"] = project_row[0]
        #     subset_matrix_dict[project_row[0]]["Ploidy"] = project_row[1]
        #     subset_matrix_dict[project_row[0]]["Samples"] = {}

        #     for row in rows_specified:
        #         if (not(row[0] in subset_matrix_dict[project_row[0]]["Samples"])):
        #             subset_matrix_dict[project_row[0]]["Samples"][row[0]] = {}
        #             subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Metadata"] = {
        #                 "Project" : row[1],
        #                 "Metadata2" : row[2],
        #                 "Metadata3" : row[3],
        #                 "Metadata4" : row[4],
        #                 "ploidy" : row[5]
        #             }
        #             subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"] = {}
        #         if (not(row[6] in subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"])):
        #             if (row[6] not in loci_list):
        #                 loci_list.append(row[6])
        #             subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]] = {}
        #             subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"] = {}
        #         if (not(row[11] == None or row[11] in subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"])):
        #             subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"][row[13]] = {}
        #             subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"][row[13]]["ID"] = row[11]
        #             subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"][row[13]]["Length"] = row[12]
        #             subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"][row[13]]["Read"] = row[13]

        output_dir_path = self.workspace / ("subset_output")
        if (not output_dir_path.exists()):
            output_dir_path.mkdir(parents=True, exist_ok=True)

        dict_path = output_dir_path / ("subset.json")
        

        subset_matrix_dict, loci_per_project = self.get_subset_matrix(rows_projects_include, rows_specified)

        with open(dict_path, "w", encoding="utf-8") as f:
            json.dump(subset_matrix_dict, f, indent=4, ensure_ascii=False)
        
        for projectname, rest in subset_matrix_dict.items():
            loci_list = loci_per_project[projectname]
            csv_path = output_dir_path / ("matrix_" + projectname + ".csv")
            with open(csv_path , 'w', newline='') as outcsv:
                csvwriter = csv.writer(outcsv, delimiter=';')
                if (subset_matrix_dict[projectname]["Ploidy"] == "diploid"):
                    loci_list = [x for x in loci_list for _ in range(2)]
                csvwriter.writerow(["samples"] + loci_list)
                for sample in rest["Samples"].keys():
                    row_sample = []
                    row_sample.append(sample)
                    for locus, rest2 in rest["Samples"][sample]["Loci"].items():
                        if (not(rest["Samples"][sample]["Loci"][locus]["Alleles"])):
                            row_sample.append(0)
                            if (subset_matrix_dict[projectname]["Ploidy"] == "diploid"):
                                row_sample.append(0)
                        else:
                            for allele, data in rest["Samples"][sample]["Loci"][locus]["Alleles"].items():
                                row_sample.append(int(data["ID"]))
                                if (len(list(rest["Samples"][sample]["Loci"][locus]["Alleles"].keys())) == 1):
                                    row_sample.append(int(data["ID"]))
                
                    csvwriter.writerow(row_sample)

    def get_genalex_output(self):
        self.textbox_pipeline.delete(0.0, 'end')
        self.textbox_pipeline.insert('end-1c', "Generating Genalex output from chosen subset.\n")

        project_include, metadata2_include, loci_include = self.set_subset()

        rows_projects_include = self.db_instance.get_selected_projects(project_include)
        self.db_instance.get_view_for_extracting()
        rows_specified = self.db_instance.get_selected_loci_project_metadata(project_include, metadata2_include, loci_include)

        output_dir_path = self.workspace / ("subset_output")
        if (not output_dir_path.exists()):
            output_dir_path.mkdir(parents=True, exist_ok=True)

        dict_path = output_dir_path / ("subset.json")

        subset_matrix_dict, loci_list = self.get_subset_matrix(rows_projects_include, rows_specified)

        with open(dict_path, "w", encoding="utf-8") as f:
            json.dump(subset_matrix_dict, f, indent=4, ensure_ascii=False)
    
    def get_subset_matrix(self, rows_projects_include : list, rows_specified : list) -> dict:
        subset_matrix_dict = {}
        loci_per_project = {}
        for project_row in rows_projects_include:
            subset_matrix_dict[project_row[0]] = {}
            subset_matrix_dict[project_row[0]]["Projectname"] = project_row[0]
            subset_matrix_dict[project_row[0]]["Ploidy"] = project_row[1]
            subset_matrix_dict[project_row[0]]["Samples"] = {}

            loci_per_project[project_row[0]] = []

            for row in rows_specified:
                if (not(row[1] == project_row[0])):
                    continue
                if (not(row[0] in subset_matrix_dict[project_row[0]]["Samples"])):
                    subset_matrix_dict[project_row[0]]["Samples"][row[0]] = {}
                    subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Metadata"] = {
                        "Project" : row[1],
                        "Metadata2" : row[2],
                        "Metadata3" : row[3],
                        "Metadata4" : row[4],
                        "ploidy" : row[5]
                    }
                    subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"] = {}
                if (not(row[6] in subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"])):
                    if (row[6] not in loci_per_project[project_row[0]]):
                        loci_per_project[project_row[0]].append(row[6])
                    subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]] = {}
                    subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"] = {}
                if (not(row[11] == None or row[11] in subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"])):
                    subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"][row[13]] = {}
                    subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"][row[13]]["ID"] = row[11]
                    subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"][row[13]]["Length"] = row[12]
                    subset_matrix_dict[project_row[0]]["Samples"][row[0]]["Loci"][row[6]]["Alleles"][row[13]]["Read"] = row[13]

        return subset_matrix_dict, loci_per_project


    def updating_checkboxes(self, checkboxes, values, search_var, scrollframe):
        for checkbox in checkboxes:
            # Store the state of the checkbox before removing it
            self.checkbox_states_dict[checkbox.cget("text")] = checkbox.get()
            checkbox.grid_forget()
        
        checkboxes.clear()
    
        query = search_var.get().lower()
        filtered_values = [value for value in values if query in value.lower()]
        
        for i, value in enumerate(filtered_values):
            # Check if there's a stored state for this checkbox
            state = self.checkbox_states_dict.get(value, 0)
                
            checkbox_var = tk.IntVar(value=state)
            checkbox = ctk.CTkCheckBox(scrollframe, text=value, variable=checkbox_var)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(5, 5), sticky="w")
            checkboxes.append(checkbox)


    def updating_parameter_checkboxes(self):
        # self.checkbox_states_dict2["Loci"] = {}
        # self.checkbox_states_dict2["Metadata2"] = {}
        # self.checkbox_states_dict2["Project"] = {}

        list_project_include = []
        for checkbox in self.checkboxes_project_include:
            checkbox_text = checkbox.cget("text")
            if checkbox.get() == 1:
                list_project_include.append(checkbox_text)
            self.checkbox_states_include_dict[checkbox_text] = checkbox.get()
        self.checkbox_states_dict2["Project"] = list(set(list_project_include))
        #self.checkboxes_project_include = []

        list_metadata2_include = []
        for checkbox in self.checkboxes_metadata2_include:
            checkbox_text = checkbox.cget("text")
            if checkbox.get() == 1:
                list_metadata2_include.append(checkbox_text)
            self.checkbox_states_include_dict[checkbox_text] = checkbox.get()
        self.checkbox_states_dict2["Metadata2"] = list(set(list_metadata2_include))
        #self.checkboxes_metadata2_include = []

        list_loci_include = []
        for checkbox in self.checkboxes_loci_include:
            checkbox_text = checkbox.cget("text")
            if checkbox.get() == 1:
                list_loci_include.append(checkbox_text)
            self.checkbox_states_include_dict[checkbox_text] = checkbox.get()
        self.checkbox_states_dict2["Loci"] = list(set(list_loci_include))
        #self.checkboxes_loci_include = []


    def closing(self):
        try:
            self.updating_parameter_checkboxes()
            self.on_done("Pipeline has not started:", self.checkbox_states_include_dict, self.checkbox_states_dict2)
        finally:
            self.destroy()


if __name__ == "__main__":
    main()