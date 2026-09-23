# Introduction
This project implements a Markov chain to process sentences.
The project starts with a simple first-order model, where the next word depends only on the current word. 
It then extends this idea to an Nth-order model, where the next word depends on the previous N words. 
This is similar to how Markov chain models can be used in bioinformatics, 
such as identifying coding regions in a genome by using higher-order models to capture patterns between codon triplets.

# Pseudocode
Building the model
(build_markov_model):
Add artificial states for start (*S*) and end (*E*).
For each word or N-word window in the text:
    increment markov_model[state][next_word]
Return markov_model

Selecting the next word
(get_next_word):

# Successes
Successfully implemented a first order Markov model that matched the expected output.
Successfully Got the Nth-order version working by using word-pairs as dictionary keys instead of single words. 
Traced a test sentence by hand and compared it to my code's output. They matched exactly, including repeated pairs and 
pairs that led to different next-words at different points.
Got the full generation pipeline working end-to-end on the toy Dr. Seuss example, producing valid generated sentences.


# Struggles

# Personal reflections
## Group Leader


## Other member

# Generative AI Appendix
