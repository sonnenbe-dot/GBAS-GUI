from pathlib import Path

def main():


    return 0


def make_output_folders(folderpath_newfolderpath_new : Path, outputlist : list):
    for folder in outputlist:
        folderpath_new =  folderpath_newfolderpath_new / folder
        folderpath_new.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()