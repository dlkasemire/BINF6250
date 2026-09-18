#!/usr/bin/env python
from pprint import pprint

def parse_line(line):
    """
    Parse line in VCF file and return list of disease names associated
    with the rare variant.

    Returns an empty list if there is no AF_EXAC value, if variant isn't rare,
    or if there is no CLNDN.
    """

    # tab separated, split line by tab
    columns = line.split("\t")

    # info is in the last column of the line
    info = columns[-1]

    # info contains key-value pairs separated by ;
    key_pairs = info.split(";")

    # make a dictionary of all the key-value pairs
    info_dict = {}

    # for each key-value pair,
    for pair in key_pairs:
       split_pair = pair.split("=") # split by the = sign

       # ignore if there is no value
       if len(split_pair) < 2:
           continue

       key = split_pair[0] # index location of key
       value = split_pair[1] # index location of value
       info_dict[key] = value

    # Skip line if "AF_EXAC" not present
    if "AF_EXAC" not in info_dict:
        return []

    # converts value to numbber so it's comparable
    af_value = float(info_dict["AF_EXAC"])

    # keep only rare variants, discard if at or above 0.0001
    if af_value >= 0.0001:
        return []

    # Skip variant if no disease name is found
    if "CLNDN" not in info_dict:
        return []

    # several diseases split by |
    diseases = info_dict["CLNDN"].split("|")
    filtered_diseases = [] # keeps meaningful disase names

    # exclude if not actual condition
    for disease in diseases:
        if disease != "not_specified" and disease != "not_provided":
            filtered_diseases.append(disease)

    return filtered_diseases

def read_file(filename):
    """
    Read a VCF file and count how many rare variants are associated
    with each disease.

    Returns a dictionary of the disease and how many rare variants
    are linked to it.
    """

    counts = {} # store disease name, number of times seen

    with open(filename, "r") as f: # open file
        for line in f:
            if line.startswith("#"): # lines starting with # are headers
                continue # so skip/ignore them

            # remove any trailing newlines before parsing
            line = line.strip()
            diseases = parse_line(line)

            # tally every disease found on this line
            for disease in diseases:
                if disease in counts:
                    counts[disease] += 1 #if it exists, add 1 to its tally

                else:
                    counts[disease] = 1 # if it doesn't exist yet, tally it 1

    return counts

if __name__ == "__main__":
    pprint(read_file("clinvar_20190923_short.vcf"))
