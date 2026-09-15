# Introduction
Description of the project

# Pseudocode
Put pseudocode in this box:
""" 
Define function parse_line (string argument)
    Split the line into columns by /tab
    Obtain information from final column INFO
    Split info by semicol. into key value pairs (sep by an =) store in dict format

        IF AF_EXAC not in dict skip to next line
        IF varient <0.0001 
            make empty list AF_EXAC_Conditions and circulate through AF_EXAC CLNDN, when it doesnt = not_sepesifed or not_provided add to empty list 
            return list of diseases using CLNDN 

        else
            return empty list
"""
""" 
Define read_file (argument is a str)
    Create empty dictionary to add output 

    Open the file
    For loop iterating through file, if line starts with # skip that line
        feed into parse_line function 
        As key value pairs are returned, if a disease has already been counted the tally should +=1, if not then =1
    return the dic count 
    print results from read_file
    
# Successes
Description of the team's learning points

# Struggles
Description of the stumbling blocks the team experienced

# Personal reflections
## Group Leader
Group leader's reflection on the project

## Other member
Other member's reflection on the project

# Generative AI Appendix
As per the syllabus
