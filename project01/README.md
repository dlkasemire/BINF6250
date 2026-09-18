# Introduction
This project parses a Variant Call Format (VCF) file from ClinVar.
The goal of the project is to identify rare genetic variants with AF_EXAC less than 0.0001, 
and tally the disease (CLNDN) associated with them across the dataset.
The program reads the clinvar_20190923_short.vcf file line per line.
It then extracts the required fields in the INFO column for each variant.
It then checks if it's rare and builds a tally of disease occurrences among the rare variants.
The final tally is then printed to the console.

# Pseudocode
Function parse_line(line)
    split line into columns by tab
    get the last column: info columns
    split info by ; into key-value pairs
    build a dictionary of all key=value pairs
    IF "AF_EXAC" is not in dictionary:
        RETURN empty list
    IF AF_EXAC value >= 0.0001
        RETURN empty list
    split CLNDN value by "|" to get the disease list
    remove "not_specified" and "not_provided" from list
    RETURN remaining disease list


FUNCTION read_file(filename):
    build dictionary of counts
    open file 
        for every line
            if the line starts with #
                skip to next line
            strip white spaces at end of each line
            call parse_line on the line, store result as diseases
            for each disease in diseases:
                IF disease in counts:
                    add 1 to its count
                ELSE:
                    set its count to 1
RETURN counts

# Successes
Learned to collaborate on Github.
Successfully extracted key-value pairs
Understood the importance of reading line per line instead of the entire file, especially for large files.
Writing effective pseudocode for the functions.
We successfully produced the  disease count dictionary 

{'Cardiovascular_phenotype': 14,
 'Cleft_palate': 1,
 'Congenital_myasthenic_syndrome': 3,
 'Developmental_regression': 1,
 'Dystonia': 1,
 'EEG_with_generalized_epileptiform_discharges': 1,
 'Ehlers-Danlos_syndrome,_progeroid_type,_2': 2,
 'Expressive_language_delay': 1,
 'Failure_to_thrive': 1,
 'Global_developmental_delay': 2,
 'Growth_delay': 1,
 'Hypothyroidism': 1,
 'Idiopathic_generalized_epilepsy': 14,
 'Immunodeficiency_16': 2,
 'Immunodeficiency_38_with_basal_ganglia_calcification': 3,
 'Inability_to_walk': 1,
 'Inborn_genetic_diseases': 2,
 'Infantile_axial_hypotonia': 1,
 'Intellectual_disability': 1,
 'Limb_hypertonia': 1,
 'Marfanoid_habitus': 1,
 'Mental_retardation,_autosomal_dominant_42': 1,
 'Multifocal_epileptiform_discharges': 1,
 'Muscular_hypotonia': 2,
 'Myasthenic_syndrome,_congenital,_8': 79,
 'Myelodysplastic_syndrome': 1,
 'Neurodevelopmental_Disability': 2,
 'Nystagmus': 1,
 'Seizures': 2,
 'Severe_Myopia': 1,
 'Shprintzen-Goldberg_syndrome': 37,
 'Spinocerebellar_ataxia_21': 1,
 'Spondyloepimetaphyseal_dysplasia_with_joint_laxity': 1,
 'Strabismus': 1,
 'Upper_limb_hypertonia': 1,
 'hypotonia': 2}.

# Struggles
Faced a number of issues with Github.
Ensuring that the file to be used was in the right folder was challenging at first.
Making multiple commits in the same branch but not wanting all of them.

# Personal reflections
## Group Leader
Since it was my first time working with Github, I faced some challenges creating the required projects.
Following the Github notes provided for the module helped me understand what was required.
I also met up with my team and this helped broaden my understanding of Github.
Figuring out that CLNDN had several diseases separated by | took up alot of time since we had to manually analyse the lines to see this.
The pseudocode helped us figure out what was needed to write the code.

## Other member
Abby - During this project I encountered a lot of hurdles beginning with using the GitHub platform to interact and collaborate with my teammates. 
After talking with my team and attending office hours I managed to get a better grip on pull requests and forks. 
As for the analysis itself it was difficult for me at first to conceptualize the format of the file and the edits that needed to be made in the code. 
But after going over the commands with Claude and asking how these splits from ";" and "|" affected the file it made a lot more sense. 
Writing the pseudocode and doing the order of operations necessary to obtain the correct answer came easier to us as a group.
 
# Generative AI Appendix
Claude Anthropic Version 2.110.0 Sonnet 5, was used to assist in determining the correct way to parse the data file so that the values could be determined. 
The prompt that was used to generate this data was " If i need to split a VCF file by column by "/t" and select the last column for analysis can you give me a starting point" and " Splitting key value pairs by ":" is the next split, I believe it will be the same format can you give me guidance on what to do". 
This allowed us to understand how to format code in order to separate and group variables into key values.