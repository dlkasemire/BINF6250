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
Abby - During this project I encountered a lot of hurdles beginning with using the GitHub platform to interact and collaborate with my teammates. After talking with my team and attending office hours I managed to get a better grip on pull requests and forks. As for the analysis itself it was difficult for me at first to conceptualize the format of the file and the edits that needed to be made in the code. But after going over the commands with Claude and asking how these splits from ";" and "|" affected the file it made a lot more sense. Writing the pseudocode and doing the order of operations neccesary to obtain the correct answer came easier to us as a group. 

# Generative AI Appendix
Claude Anthropic Version 2.110.0 Sonnet 5, I used Claude to assit me in determining the correct way to parse the data file so that the values could be determined. The promt that I used to generate this data was " " and " ". This allowed me to understand how to format my code in order to separate and group my vairubles into key values. 