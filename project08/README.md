## A description of the project


## Pertinent documentation and usage write-up


## Pseudocode


## Reflection narrative that describes what went right, what went wrong, what you didn't understand, how it could have been better, and how you could have been better.


## Appendix (AI usage, citations, etc.)


Set up the model
    Take in the three dictionaries: starting chances, switching chances, emission chances
    Get the list of states from the keys of the starting chances
    Get the list of symbols from the keys of any state's emission chances
    Check the inputs:
        every dictionary uses the same states
        every state can emit the same symbols
        every number is between 0 and 1
        the starting chances add up to 1
        each state's switching chances add up to 1
        each state's emission chances add up to 1
        if any check fails, stop with a clear error message
    Turn every chance into a log (a chance of 0 becomes minus infinity)

Run Viterbi on a sequence
    If the sequence is empty, stop with an error
    If the sequence has a symbol no state can emit, stop with an error
    Make two empty tables, one row per state and one column per symbol in the sequence:
        a score table: the best score for reaching each circle
        a pointer table: which state that best score came from

     Fill the first column:
        for each state:
            score = log starting chance + log chance this state emits the first symbol
            no pointer yet

    Fill the rest of the columns, left to right:
        for each column after the first:
            for each state you could be in now:
                for each state you could have come from:
                    try = previous score + log chance of switching to this state
                keep the biggest try, and remember which state gave it
                score = biggest try + log chance this state emits this symbol
                pointer = the state that gave the biggest try

    Find the end of the best path:
        look at the last column
        pick the state with the highest score
        that score is the log-probability of the best path

    Trace back to get the path:
        start at that best last state
        move left one column at a time, following the pointers
        write down each state you land on
        flip the list so it reads left to right

    Return the path and its log-probability

Test it
    One symbol "G" with the example tables:
        expected path G, probability 0.16
    Two symbols "GG" with the example tables:
        expected path G G, probability 0.0288
    The primer's 7 windows (none, few, many, many, none, many, none):
        expected path U U T T T T U, probability about 0.0000097
    A sequence with a symbol like "N":
        expected an error message
    A long sequence of 1,000 symbols:
        expected a real number, not minus infinity
