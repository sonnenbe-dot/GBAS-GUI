import os, json, argparse
import pandas as pd
from pathlib import Path

# Converting a .xlsx or .csv into json format, the excel's first row is the header

def main():
    print("Convert excel to json!\n")

    parser = argparse.ArgumentParser(description='Convert target excel to json! \n')
    parser.add_argument("excelfilepath", type = str, help = "Input excelfilepath!")
    parser.add_argument("jsonfilepath", type = str, help = "Input jsonfilepath!")
    parser.add_argument("excelheader", type = str, help = "Input excelheader for main json key!")
    args = parser.parse_args()

    excelfilepath = os.path.normpath(args.excelfilepath)
    jsonfilepath = os.path.normpath(args.jsonfilepath)

    if (not(valid_path(excelfilepath))):
        print("Not a valid excel filepath! \n")
        return

    if (not(os.path.splitext(excelfilepath)[1] == ".csv" or os.path.splitext(excelfilepath)[1] == ".xlsx")):
        print("This is not .csv or .xlsx! \n")
        return
    
    convert_excel_to_json(excelfilepath, jsonfilepath, args.excelheader)



    return 0

def write_dict_to_json(dict_obj : dict, jsonfilepath : Path):
    with open(jsonfilepath , "w") as file:
        json.dump(dict_obj, file, indent = 4)


def convert_excel_to_json_dict(excelfilepath : Path, excelheader : str):
    #print(excelfilepath.suffix)
    if (excelfilepath.suffix == ".csv"):
        df = pd.read_csv(excelfilepath, sep=r"[;,|\t]", engine="python")
    elif (excelfilepath.suffix == ".xlsx"):
        df = pd.read_excel(excelfilepath) #sheet_name="Barcording_database"
    else:
        print("\nThis is not excel fileformat! Metadata cannot be added!\n")
        return {}
    
    df.rename(columns = lambda x : str(x).strip(), inplace = True)
    outputdict = {}
    headers = [str(header).strip() for header in list(df.columns)]
    #print(headers)
    if (excelheader not in headers):
        print("Excelheader could not be found in excelfile headers! Metadata cannot be added!\n")
        return {}
    
    for _, row in df.iterrows(): #ignoring row indexes with _
        if (excelheader in row and not(pd.isna(row[excelheader]))):
            outputdict[row[excelheader]] = {}
            for header in headers:
                if (header != excelheader):
                    outputdict[row[excelheader]][header] = row[header]
    
    return outputdict

def convert_excel_to_json(excelfilepath : Path, jsonfilepath : str, excelheader : str):
    excelfilepath = os.path.normpath(excelfilepath)
    jsonfilepath = os.path.normpath(jsonfilepath)

    if (os.path.splitext(excelfilepath)[1] == ".csv"):
        df = pd.read_csv(excelfilepath, delimiter=';')
    else:
        df = pd.read_excel(excelfilepath) #sheet_name="Barcording_database"
    df.rename(columns = lambda x : str(x).strip(), inplace = True)
    outputdict = {}

    headers = [str(header).strip() for header in list(df.columns)]
    if (excelheader not in headers):
        print("Excelheader could not be found in excelfile headers!\n")
        return

    #print(headers)
    for _, row in df.iterrows(): #ignoring row indexes with _
        if (excelheader in row and not(pd.isna(row[excelheader]))):
            outputdict[row[excelheader]] = {}
            for header in headers:
                outputdict[row[excelheader]][header] = row[header]

    print(outputdict)
    with open(jsonfilepath , "w") as file:
        json.dump(outputdict, file, indent = 4)


def valid_path(path : str):
    return (os.path.exists(os.path.normpath(path)) and (os.path.basename(os.path.normpath(path)) != "None") and (os.path.normpath(path) != "") and (os.path.normpath(path) != ".") and (os.path.basename(os.path.normpath(path)) != "."))



if __name__ == "__main__":
    main()