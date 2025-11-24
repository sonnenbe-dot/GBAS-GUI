import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path

def main():


    return 0



def browse_dir(entry, dir_param):
    directory_path = Path(filedialog.askdirectory(initialdir=dir_param, title="Select folder!"))
    entry.delete(0, tk.END)  # Clear the entry
    entry.insert(0, directory_path)  # Insert the file/folder path into the entry

def browse_file(entry, dir_param):
    file_path = Path(filedialog.askopenfilename(initialdir=dir_param, title="Select file!"))
    entry.delete(0, tk.END)  # Clear the entry
    entry.insert(0, file_path)  # Insert the file/folder path into the entry