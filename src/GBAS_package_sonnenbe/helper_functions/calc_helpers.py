
def main():
    
    return 0


def rev_comp(seq):
    # dictionary with Key for complementing nucleotide
    code = {'A':'T','C':'G','T':'A','G':'C', 'Y':'R', 'R':'Y', 'S':'S', 'W':'W', 'K':'M', 'M':'K', 'B':'V', 'D':'H', 'H':'D', 'V':'B', 'N':'N'}
    result_sequence = '' # resulting string will be saved here
    for i in seq: # iterate through nucleotide in input string
        complement = code.get(i.upper(), i) # get complement. if it does not exist get the input nucleotide
        result_sequence = complement + result_sequence #add complemented nucleotide in the beggining of the output string. This way it is reversed
    return result_sequence
    
def mismatch(seq_a, seq_b):
    # dictionary with Key of nucleotides that can match to each other. For example, an A in one string can matck with 'A','N','R','W','M' in the other string
    IUPAC = {'A':['A', 'N','R','W','M'], 'C':['C', 'N','Y','S','M'], 'G':['G', 'N','R','S','K'], 'T':['T', 'N','Y','W','K'], '-':['-'],
    'R':['A','G', 'N'], 'Y':['C','T', 'N'], 'S':['G','C', 'N'], 'W':['A','T', 'N'], 'K':['G','T', 'N'], 'M':['A','C', 'N'], 'B':['C','G','T', 'N'],
    'D':['A','G','T', 'N'], 'H':['A','C','T', 'N'], 'V':['A','C','G', 'N'], 'N':['A','T','G','C', 'N'], 'I':['A','T','G','C', 'N']}
    len1 = len(seq_a)
    len2 = len(seq_b)
    mismatches = 0 # mismatched is assumed to be 0. Only if a mismatch is found +1 is added
    for pos in range (0,min(len1,len2)): # in case sequences with different lengths are added, iterate only through indexxes of the small one.
        base_b = seq_b[pos] # get nucleotide of seq_b
        if base_b in IUPAC:
            base_b_IUPAC = IUPAC[base_b] # get possible matches of seq_b nucleotide in a list format
            # add mismatch only if corresponding nucleotode in seq_a is not found in the list of possible matches of seq_b
            if not seq_a[pos] in base_b_IUPAC:
                mismatches+=1
        else:
            mismatches+=1
    return mismatches


if __name__ == "__main__":
    main()