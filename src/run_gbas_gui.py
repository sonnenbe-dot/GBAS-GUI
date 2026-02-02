import multiprocessing as mp
from GBAS_package_sonnenbe import main_GUI


def main() -> None:
    # Needed for Windows + PyInstaller + multiprocessing.Pool etc.
    mp.freeze_support()
    # Call the main entry of your GUI module
    main_GUI.main()


if __name__ == "__main__":
    main()



# import runpy
# import sys
# from pathlib import Path
# import multiprocessing as mp

# # Path to the package's src folder
# ROOT = Path(__file__).resolve().parent
# SRC_PATH = ROOT / "package" / "src"

# # Make the GBAS package importable
# sys.path.insert(0, str(SRC_PATH))

# def main():
#     try:
#         mp.freeze_support()   # Needed for Windows + PyInstaller + multiprocessing
#     except Exception:
#         pass

#     # Run the real GUI main module (inside package/src)
#     runpy.run_module("GBAS_package_sonnenbe.main_GUI", run_name="__main__")

# if __name__ == "__main__":
#     main()




















# import runpy, sys
# from pathlib import Path

# ROOT = Path(__file__).resolve().parent
# # Make the src layout importable (both when running normally and during PyInstaller analysis)
# sys.path.insert(0, str(ROOT / "package" / "src"))

# if __name__ == "__main__":
#     try:
#         import multiprocessing as mp
#         mp.freeze_support()
#     except Exception:
#         pass
#     runpy.run_module("GBAS_package_sonnenbe.main_GUI", run_name="__main__")




# import runpy, sys
# from pathlib import Path

# # Make 'src' visible in both normal runs and when PyInstaller analyzes imports
# repo_root = Path(__file__).resolve().parent
# sys.path.insert(0, str(repo_root / "src"))

# if __name__ == "__main__":
#     # If you use multiprocessing anywhere:
#     try:
#         import multiprocessing as mp
#         mp.freeze_support()
#     except Exception:
#         pass

#     runpy.run_module("GBAS_package_sonnenbe.main_GUI", run_name="__main__")



# import runpy

# if __name__ == "__main__":
#     runpy.run_module("GBAS_package_sonnenbe.main_GUI", run_name="__main__")