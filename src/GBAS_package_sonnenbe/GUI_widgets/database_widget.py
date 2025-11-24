import customtkinter as ctk
from pathlib import Path
import tkinter as tk
import threading, json

from GBAS_package_sonnenbe.helper_functions.gui_helpers import browse_dir, browse_file
from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import is_valid
from GBAS_package_sonnenbe.helper_functions.parse_primerfile import get_primers
from GBAS_package_sonnenbe.helper_functions.convert_excel_to_json import convert_excel_to_json_dict, write_dict_to_json

from GBAS_package_sonnenbe.main_functions.database_class import local_database_sqlite

def main():

    return 0


class Database_window(tk.Toplevel):
    def __init__(self, parent, current_workspace : Path, paramsdict : dict, matrix_outputpath : str, on_done):
        super().__init__(parent)

        self.on_done = on_done
        self.workspace = current_workspace
        self.paramsdict = paramsdict
        self.matrix_outputpath = matrix_outputpath

        self.primerfilepath = self.paramsdict["Primerfile"]
        self.metadatapath = Path(self.paramsdict["Metadata"])
        self.databasepath = Path(self.paramsdict["Database"])

        self.add_dots_textbox = False

        self.title("Database Window")
        self.transient(parent)
        self.focus_set()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)  # Make this row expandable for the paths section
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)  # Make this row expandable for the textbox
        self.grid_rowconfigure(4, weight=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.build_window()

        self.db_instance = None
    

        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.bind('<Return>', lambda event: self.closing())
    
    def closing(self):
        # hand the value back before destroying
        try:
            self.on_done("Pipeline has not started:")
        finally:
            self.destroy()
    
    def build_window(self):
        input_paths = []
    
        # Label for Paths
        ctk.CTkLabel(self, text="Paths for inputs:", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, columnspan=3, sticky="nsew", padx=20, pady=(20, 20))
    
        # Paths Frame
        paths = ctk.CTkFrame(self, width=100, corner_radius=2)
        paths.grid(row=1, column=0, columnspan=3, sticky="nsew")
        paths.grid_columnconfigure(0, weight=1)
        paths.grid_columnconfigure(1, weight=1)
        paths.grid_columnconfigure(2, weight=1)
        paths.grid_rowconfigure(0, weight=1)
              
        
        # Label for Comparison Output
        ctk.CTkLabel(self, text="Status:", font=ctk.CTkFont(size=20, weight="bold")).grid(row=2, column=0, columnspan=3, sticky="nsew", padx=20, pady=(20, 20))
        
        # Textbox Frame
        textbox_frame = ctk.CTkFrame(self, width=100, corner_radius=2)
        textbox_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")  # Expanding this row
        textbox_frame.grid_columnconfigure(0, weight=1)
        textbox_frame.grid_rowconfigure(0, weight=1)
    
        # Labels and Entry fields in the paths section
        ctk.CTkLabel(paths, text="Matrix Output (.json):", width=20).grid(column=0, row=0, padx=5, pady=5)
        entry_output = ctk.CTkEntry(paths, corner_radius=5)
        tk.Button(paths, text="Browse", command=lambda entry=entry_output: browse_file(entry, self.workspace)).grid(column=2, row=0, padx=5, pady=5)
        entry_output.insert(tk.END, self.matrix_outputpath)
        entry_output.grid(column=1, row=0, padx=5, pady=5)
        input_paths.append(entry_output)

        ctk.CTkLabel(paths, text="Primerfile:", width=20).grid(column=0, row=1, padx=5, pady=5)
        entry_primerfile = ctk.CTkEntry(paths, corner_radius=5)
        tk.Button(paths, text="Browse", command=lambda entry=entry_primerfile: browse_file(entry, self.workspace)).grid(column=2, row=1, padx=5, pady=5)
        entry_primerfile.insert(tk.END, self.primerfilepath)
        entry_primerfile.grid(column=1, row=1, padx=5, pady=5)
        input_paths.append(entry_primerfile)
        
        ctk.CTkLabel(paths, text="Metadata:", width=20).grid(column=0, row=2, padx=5, pady=5)
        entry_metadata = ctk.CTkEntry(paths, corner_radius=5)
        tk.Button(paths, text="Browse", command=lambda entry=entry_metadata: browse_file(entry, self.workspace)).grid(column=2, row=2, padx=5, pady=5)
        entry_metadata.insert(tk.END, self.metadatapath)
        entry_metadata.grid(column=1, row=2, padx=5, pady=5)
        input_paths.append(entry_metadata)


        # Textbox for Comparison Output
        self.textbox_dataset_import = ctk.CTkTextbox(textbox_frame, width=140)
        self.textbox_dataset_import.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=(5, 5))  # Ensure it's in row 0 inside the frame
        self.textbox_dataset_import.insert("0.0", "Database Status:" + "\n\n" * 2)
        if (not(is_valid(str(self.databasepath))) and not(self.databasepath.suffix == ".db")):
            self.textbox_dataset_import.insert('end-1c', f"There is no database at location {self.databasepath} or wrong file.\n")
            if (not(self.databasepath.name == "." or not(self.databasepath.name == "None"))):
                self.databasepath = Path(self.databasepath.stem + ".db")
                self.textbox_dataset_import.insert('end-1c', f"Database will be saved at location {str(self.databasepath)}.\n\n")
            else:
                self.databasepath = Path("database.db")
                self.textbox_dataset_import.insert('end-1c', f"Database will be saved in current folder with default name 'database.db'.\n\n")
        
        self.textbox_dataset_import.insert('end-1c', f"Database stored at location {str(self.databasepath)}.\n\n")
        self.textbox_dataset_import.insert('end-1c', f"\nDatabase contains the following data:\n\n")
        self.show_database_status()
        
        # Left-aligned button
        ctk.CTkButton(self, border_width=1, border_color="black", text_color="black", text="Update Database Status", command= self.updating_Database_status).grid(row=5, column=0, sticky="w", padx=(25, 5), pady=(10, 5))

        # Right-aligned button
        ctk.CTkButton(self, border_width=1, border_color="black", text_color="black", text="Add to local Database", command = self.adding_data_to_database_threading).grid(row=5, column=2, sticky="e", padx=(5, 25), pady=(10, 5))
    

    def updating_Database_status(self):
        self.textbox_dataset_import.delete(0.0, 'end')
        self.textbox_dataset_import.insert('end-1c', "Current Database Status:\n\n")
        self.show_database_status()

    def show_database_status(self):
        self.db_instance = local_database_sqlite(self.databasepath)
        self.db_instance.create_tables()

        query = "SELECT Locusname, Alleleindex, Sequencelength, Sequenceread FROM table_allele"
        rows = self.db_instance.get_distinct(query)

        #print(rows)

        total_number = self.db_instance.get_number_nonempty_sequences()
        number_loci = self.db_instance.get_number_distinct_loci_with_alleles()
        number_loci_without_alleles = self.db_instance.get_number_distinct_loci_without_alleles()
        number_lengths = self.db_instance.get_number_distinct_lengths()
        
        self.textbox_dataset_import.insert('end-1c', "Number of appearing Marker with Alleles:" + str(number_loci) + "\n\n")
        self.textbox_dataset_import.insert('end-1c', "Number of appearing Marker with no Alleles:" + str(len(number_loci_without_alleles)) + "\n\n")
        self.textbox_dataset_import.insert('end-1c', "\nNumber of stored Alleles:" + str(total_number) + "\n\n")
        self.textbox_dataset_import.insert('end-1c', "Number of unique Sequence Lengths:" + str(number_lengths) + "\n\n")
        #self.display_data(rows)

        self.db_instance.closing()

    
    def adding_data_to_database_threading(self):
        thread = threading.Thread(target=self.adding_data_to_database, daemon=True)
        thread.start()

    def adding_data_to_database(self):
        self.textbox_dataset_import.delete(0.0, 'end')
        self.textbox_dataset_import.insert('end-1c', "Checking format of inputs...\n\n")
        self.db_instance = local_database_sqlite(self.databasepath)
        self.db_instance.create_tables()

        self.textbox_dataset_import.insert('end-1c', "\nAdding dataset into database.\n")

        self.add_dots_pipelinetextbox = True
        self.append_period()

        primers_dict = get_primers(self.primerfilepath)
        meta_dict = convert_excel_to_json_dict(self.metadatapath, "sample")
        markermatrix_dict = {}
        with open(self.matrix_outputpath) as json_file:
            markermatrix_dict = json.load(json_file)
        
        metadata_headers = [metadata_header for metadata_header in meta_dict[list(meta_dict.keys())[0]]]


        ok, err, added_sequences_count = self.db_instance.insert_dataset(primers_dict, markermatrix_dict, meta_dict, metadata_headers)

        #print(metadata_headers)


        self.add_dots_pipelinetextbox = False
        if (ok):    
            self.textbox_dataset_import.insert('end-1c', "\nDataset was added with no errors.\n")
            self.textbox_dataset_import.insert('end-1c', f"\n{added_sequences_count} new alleles were added.\n")
        else:
            self.textbox_dataset_import.insert('end-1c', "\nThere were problems when adding the dataset.\n")
            self.textbox_dataset_import.insert('end-1c', f"\nError message: {err}.\n")
        
        self.db_instance.closing()


    def append_period(self):
        self.textbox_dataset_import.insert('end-1c', ".")
        if self.add_dots_pipelinetextbox:
            self.after(1000, self.append_period)




if __name__ == "__main__":
    main()