from pathlib import Path

def main():

    return 0

def writeFasta(SeqDict : dict, out : Path):
    with open(out,'w') as outFasta:
        for header, sequence in SeqDict.items():
            outFasta.write('>' + header[1:] + '\n' + sequence + '\n')

if __name__ == "__main__":
    main()