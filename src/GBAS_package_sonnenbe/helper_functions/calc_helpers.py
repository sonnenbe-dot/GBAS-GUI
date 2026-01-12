import numpy as np

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


def mismatch_binary(seq_a : str, seq_b : str, dna_lookup : dict):
    n = min(len(seq_a), len(seq_b))

    a_ints = np.frombuffer(seq_a[:n].encode('ascii'), dtype=np.uint8)
    b_ints = np.frombuffer(seq_b[:n].encode('ascii'), dtype=np.uint8)
    
    # 3. Retrieve Bitmasks from Lookup Table
    a_bits = dna_lookup[a_ints]
    b_bits = dna_lookup[b_ints]
    
    # 4. The Comparison
    # Bitwise AND (&). If result is 0, they share no bits -> Mismatch
    # If result is > 0 (e.g. 1, 2, 4...), they share a bit -> Match
    matches = a_bits & b_bits

    return int(np.sum(matches == 0))


if __name__ == "__main__":
    main()