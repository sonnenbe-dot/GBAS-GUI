import customtkinter as ctk
from pathlib import Path
import tkinter as tk
import threading

from GBAS_package_sonnenbe.helper_functions.gui_helpers import browse_dir, browse_file

def main():


    return 0


class allele_comparison_window(tk.Toplevel):
    def __init__(self, parent, current_workspace : Path, paramsdict : dict, on_done):
        super().__init__(parent)

        self.on_done = on_done

        self.allelelist_before = ""
        self.allelelist_after = ""

        self.title("Calculate PIC")
        self.transient(parent)
        self.focus_set()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)  # Make this row expandable for the paths section
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)  # Make this row expandable for the textbox
        self.grid_rowconfigure(4, weight=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)  # Scrollbars or buttons

        self.build_window()
    
    def closing(self):
        # hand the value back before destroying
        try:
            self.on_done("Pipeline has not started:")
        finally:
            self.destroy()

    def build_window(self):
        
        allelelist_paths = []
    
        # Label for Paths
        ctk.CTkLabel(self, text="Paths for Allelist inputs:", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, columnspan=3, sticky="nsew", padx=20, pady=(20, 20))
    
        # Paths Frame
        paths = ctk.CTkFrame(self, width=100, corner_radius=2)
        paths.grid(row=1, column=0, columnspan=3, sticky="nsew")
        paths.grid_columnconfigure(0, weight=1)
        paths.grid_columnconfigure(1, weight=1)
        paths.grid_columnconfigure(2, weight=1)
        paths.grid_rowconfigure(0, weight=1)
    
        # Label for Comparison Output
        ctk.CTkLabel(self, text="Comparison Output:", font=ctk.CTkFont(size=20, weight="bold")).grid(row=2, column=0, columnspan=3, sticky="nsew", padx=20, pady=(20, 20))
    
        # Textbox Frame
        textbox_frame = ctk.CTkFrame(self, width=100, corner_radius=2)
        textbox_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")  # Expanding this row
        textbox_frame.grid_columnconfigure(0, weight=1)
        textbox_frame.grid_rowconfigure(0, weight=1)
    
        # Labels and Entry fields in the paths section
        ctk.CTkLabel(paths, text="Old Allelelist:", width=20).grid(column=0, row=0, padx=5, pady=5)
        entry_old = ctk.CTkEntry(paths, corner_radius=5)
        tk.Button(paths, text="Browse", command=lambda entry=entry_old: browse_file(entry_old, self.workspace)).grid(column=2, row=0, padx=5, pady=5)
        entry_old.insert(tk.END, self.allelelist_before)
        entry_old.grid(column=1, row=0, padx=5, pady=5)
        allelelist_paths.append(entry_old)
    
        ctk.CTkLabel(paths, text="New Allelelist:", width=20).grid(column=0, row=1, padx=5, pady=5)
        entry_new = ctk.CTkEntry(paths, corner_radius=5)
        tk.Button(paths, text="Browse", command=lambda entry=entry_new: browse_file(entry_new, self.workspace)).grid(column=2, row=1, padx=5, pady=5)
        entry_new.insert(tk.END, self.allelelist_after)
        entry_new.grid(column=1, row=1, padx=5, pady=5)
        allelelist_paths.append(entry_new)
    
        # Textbox for Comparison Output
        self.textbox_allelelist_comparison = ctk.CTkTextbox(textbox_frame, width=250)
        self.textbox_allelelist_comparison.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=(5, 5))  # Ensure it's in row 0 inside the frame
        self.textbox_allelelist_comparison.insert("0.0", "Comparison Output:" + "\n\n" * 2)
    
        # Button to get comparison output
        ctk.CTkButton(self, border_width=1, border_color="black", text_color="black", text="Get Comparison Output", command=lambda x=allelelist_paths: self.get_allelelist_comparison_threading(x)).grid(row=4, column=0, columnspan=3, sticky="nsew", padx=(25, 25), pady=(10, 5))


    def get_allelelist_comparison_threading(self, x):
        self.allelelist_before = Path(x[0].get())
        self.allelelist_after = Path(x[1].get())

        thread = threading.Thread(target=self.get_allelelist_comparison)
        thread.start()

    def get_allelelist_comparison(self):
        pass

if __name__ == "__main__":
    main()