#!/usr/bin/env python
from pprint import pprint


# Modify this function signature and fill in the details
#Begin by spliting the data by tabs, then split the 8th column by semicolons, 
# and finally split each of those by equals signs to create a dictionary of key-value pairs.
def parse_line(line):
    columns = str.split("\t")
    info = columns[-1]
    info_pairs = info.split(";")
    
    af_exac_check = None
    clndn = None

    for pair in info_pairs:
        key_value = pair.split("=")
        key = key_value[0]

        if len(key_value) < 2:
            continue

        value = key_value[1]

        if key == "AF_EXAC":
                af_exac_check = float(value)
        elif key == "CLNDN":
                clndn = value
        return af_exac_check, clndn

    if af_exac_check is None:
        return []
    
    if af_exac_check >= 0.0001:
        return []

    diseasescase = clndn.split("|") 
    filtered_diseases = []
    for disease in diseasescase:
        if disease != "not_provided" and disease != "not_specified":
            filtered_diseases.append(disease)
    return filtered_diseases


            
        


# Modify this function signature and fill in the details
def read_file(filename):



if __name__ == "__main__":
    pprint(read_file("clinvar_20190923_short.vcf"))