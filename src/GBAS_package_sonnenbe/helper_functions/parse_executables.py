import os, platform
from GBAS_package_sonnenbe.helper_functions.parse_write_parameters import is_valid


def main():

    return 0

# def get_bin_executables(binpath : str, adaptersfilename : str, RscriptnameDiploid : str, RscriptnameHaploid : str) -> dict:
#     executable_dict = {}
#     executable_dict["Trimmodir"] = {}
#     executable_dict["Adaptersdir"] = {}
#     executable_dict["Adaptersfilename"] = adaptersfilename
#     executable_dict["Trimmomatic"] = ""
#     executable_dict["Usearch"] = ""
#     executable_dict["RScriptDiploid"] = ""
#     executable_dict["RScriptHaploid"] = ""
#     for subdir, dirs, files in os.walk(binpath):
#         if (os.path.basename(subdir).split('-')[0] == 'Trimmomatic'):
#             trimmdir = os.path.normpath(subdir)
#             executable_dict["Trimmodir"] = os.path.normpath(trimmdir)
#         elif (os.path.basename(subdir) == 'adapters'):
#             adaptersdir = os.path.normpath(subdir)
#             executable_dict["Adaptersdir"] = os.path.normpath(adaptersdir)
#         for file in files:
#             if (file.split("-")[0] == "trimmomatic" and ".jar" in file):
#                 executable_dict["Trimmomatic"] = os.path.normpath(executable_dict["Trimmodir"] + '/' + file)
#             elif file.startswith('usearch'):
#                 if (platform.system().lower() == "windows" and "win" in file):
#                     executable_dict["Usearch"] = os.path.normpath(binpath + '/' + file)
#                 else:
#                     executable_dict["Usearch"] = os.path.normpath(binpath + '/' + file)
#             elif file.startswith(RscriptnameDiploid):
#                 executable_dict["RScriptDiploid"] = os.path.normpath(binpath + '/' + file)
#             elif file.startswith(RscriptnameHaploid):
#                 executable_dict["RScriptHaploid"] = os.path.normpath(binpath + '/' + file)
    
#     return executable_dict
    
def check_executables(executables_dict : dict) -> bool:
    flag = True
    for dir in executables_dict["Folders"]:
        if (not(is_valid(executables_dict["Folders"][dir]))):
            flag = False
            break
    for file in executables_dict["Files"]:
        if (not(is_valid(executables_dict["Files"][file]))):
            flag = False
            break
    for additional in executables_dict["Additional"]:
        if (not(is_valid(executables_dict["Additional"][additional]))):
            flag = False
            break
    return flag


    # try:
    #     executables = ["Trimmodir", "Adaptersdir", "Trimmomatic", "Usearch", "RScriptDiploid", "RScriptHaploid"]
    #     for executable in executables:
    #         if (not(is_valid(str(os.path.normpath(executables_dict[executable]))))):
    #             print("HIERFALSE\n")
    #             flag = False
    #             break
    # except Exception as e:
    #     flag = False
    #     print(f"Error when checking if executables have valid paths! \nException: {e} \n")
    # finally:
    #     return flag


if __name__ == "__main__":
    main()