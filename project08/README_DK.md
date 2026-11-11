FUNCTION set_up_model(starting_chances, moving_chances, letter_chances)

    states  = the keys of starting_chances              # e.g. I, G
    letters = the keys of letter_chances for any state  # e.g. A, C, G, T

    CHECK the inputs
        IF the three tables don't use the same states
            STOP with error "states don't match"
        IF any state is missing a letter
            STOP with error "letters don't match"
        IF any chance is below 0 or above 1
            STOP with error "chance out of range"
        IF starting_chances don't add up to 1
            STOP with error
        FOR each state
            IF its moving_chances don't add up to 1
                STOP with error
            IF its letter_chances don't add up to 1
                STOP with error

    CONVERT every chance to a log
        IF a chance is 0
            its log = minus infinity
        ELSE
            its log = log(chance)


FUNCTION viterbi(sequence)

    IF sequence is empty
        STOP with error
    IF sequence has a letter that is not in letters
        STOP with error "unknown letter"

    MAKE score table  -> one row per state, one column per letter
    MAKE arrow table  -> one row per state, one column per letter

    # Column 1: no roads in, use the starting chances
    FOR each state
        score[state][column 1] = log starting chance of state
                               + log chance state shows letter 1
        arrow[state][column 1] = nothing

    # Columns 2 to the end: compare roads, keep the best 
    FOR each column from 2 to the last
        FOR each state_now
            best_road  = minus infinity
            best_from  = nothing
            FOR each state_before
                road = score[state_before][previous column]
                     + log chance of moving from state_before to state_now
                IF road is bigger than best_road
                    best_road = road
                    best_from = state_before
            score[state_now][column] = best_road
                                     + log chance state_now shows this column's letter
            arrow[state_now][column] = best_from

    # Pick the best ending 
    best_last_state = the state with the biggest score in the last column
    best_score      = that biggest score

    # Trace back by following the arrows
    path = empty list
    standing_on = best_last_state
    FOR each column from the last down to 1
        ADD standing_on to the front of path
        standing_on = arrow[standing_on][column]   # jump to where this box's arrow points

    RETURN path and best_score
