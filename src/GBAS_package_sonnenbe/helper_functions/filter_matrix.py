from pathlib import Path
import pandas as pd
from typing import Tuple, List

def main():

    return 0


def filtering(matrixpath : Path, outputpath : Path, filtering_param : float):
    if (matrixpath.suffix == ".csv"):
        df = pd.read_csv(matrixpath, sep=r"[;,|\t]", engine="python")
    elif (matrixpath.suffix == ".xlsx"):
        df = pd.read_excel(matrixpath) #sheet_name="Barcording_database"
    

    zero_freqs = (df == 0).sum() / len(df)
    cols_to_drop = zero_freqs[zero_freqs > filtering_param].index
    df = df.drop(columns=cols_to_drop)

    row_zero_freqs = (df == 0).sum(axis=1) / df.shape[1]
    rows_to_drop = row_zero_freqs[row_zero_freqs > (1-filtering_param)].index
    df = df.drop(index=rows_to_drop)

    wanted_headers = [header.split(".")[0] for header in df.columns]   # your true duplicate headers
    df.to_csv(outputpath, sep=";", index=False, header=wanted_headers)

    # df.to_csv(outputpath, sep=";", index=False)


def filtering_df(matrixpath : Path, outputpath : Path, filtering_param : float) -> Tuple[pd.DataFrame, List[str]]:
    if (matrixpath.suffix == ".csv"):
        df = pd.read_csv(matrixpath, sep=r"[;,|\t]", engine="python")
    elif (matrixpath.suffix == ".xlsx"):
        df = pd.read_excel(matrixpath) #sheet_name="Barcording_database"
    

    zero_freqs = (df == 0).sum() / len(df)
    cols_to_drop = zero_freqs[zero_freqs > filtering_param].index
    df = df.drop(columns=cols_to_drop)

    row_zero_freqs = (df == 0).sum(axis=1) / df.shape[1]
    rows_to_drop = row_zero_freqs[row_zero_freqs > filtering_param].index
    df = df.drop(index=rows_to_drop)

    wanted_headers = [header.split(".")[0] for header in df.columns]   # your true duplicate headers

    return df, wanted_headers


if __name__ == "__main__":
    main()