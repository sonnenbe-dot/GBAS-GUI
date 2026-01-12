from pathlib import Path
import gzip, shutil

def main():


    return 0


def zip_file(filepath : Path):
    if (not(filepath.suffix == ".gz")):
        zipped_filepath = filepath.with_name(filepath.name + ".gz")
        with open(filepath, "rb") as f_in, gzip.open(zipped_filepath, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        filepath.unlink()
    
def unzip_file(zipped_filepath : Path):
    if (zipped_filepath.suffix == ".gz"):
        original_filepath = zipped_filepath.with_suffix("")
        with gzip.open(zipped_filepath, "rb") as f_in, open(original_filepath, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        zipped_filepath.unlink()

if __name__ == "__main__":
    main()