PROJECT 08: VITERBI- PSEUDOCODE

```
Example data used in the comments:
    init_probs  = {I: 0.2, G: 0.8}
    trans_probs = {I: {I: 0.7, G: 0.3},
                   G: {I: 0.1, G: 0.9}}
    emit_probs  = {I: {A: 0.1, C: 0.4, G: 0.4, T: 0.1},
                   G: {A: 0.3, C: 0.2, G: 0.2, T: 0.3}}
    sequence    = "GGCACTGAA"

All logs are natural logs (ln).
```

1. CREATE THE MODEL
CLASS HMM
```
    FUNCTION create(init_probs, trans_probs, emit_probs)

        # Save the three tables inside the model
        SAVE init_probs, trans_probs, emit_probs

        # Get the states and symbols FROM the data (never hard-code them)
        states  = the keys of init_probs                   # example: [I, G]
        symbols = the keys of emit_probs for the first state  # example: [A, C, G, T]

        # Check the tables before doing anything else
        CALL validate()

        # Convert every probability to a log, once, up front
        CALL convert_to_logs()
```

2. SAFE LOG
```
    FUNCTION safe_log(prob)
        # log(0) does not exist, so we define it as minus infinity:
        # "impossible" loses every comparison and never ends up in the path
        IF prob is 0
            RETURN minus infinity
        ELSE
            RETURN ln(prob)

        # Check: safe_log(1)   -> 0
        #        safe_log(0.8) -> -0.2231
        #        safe_log(0)   -> minus infinity

```
3. VALIDATE
```
    FUNCTION validate()

        # 1. Keys must match across the three tables
        IF trans_probs or emit_probs don't use the same states as init_probs
            STOP with error "states don't match"
        FOR each state
            IF its trans_probs don't list every state
                STOP with error "transition table is missing a state"
            IF its emit_probs don't list every symbol
                STOP with error "emission table is missing a symbol"

        # 2. Every value must be a real probability
        IF any probability is below 0 or above 1
            STOP with error "probability out of range"

        # 3. Every row must add up to 1 (allow tiny rounding, within 0.000001)
        IF init_probs don't add up to 1
            STOP with error "initial probabilities don't add up to 1"
        FOR each state
            IF its trans_probs don't add up to 1
                STOP with error "transition probabilities don't add up to 1"
            IF its emit_probs don't add up to 1
                STOP with error "emission probabilities don't add up to 1"

        # Check: the example data                  -> passes
        #        init_probs = {I: 0.2, G: 0.7}      -> error (adds up to 0.9)

```
4. CONVERT TO LOGS
```
    FUNCTION convert_to_logs()
        FOR each state
            log_init[state] = safe_log(init_probs[state])
            FOR each other_state
                log_trans[state][other_state] = safe_log(trans_probs[state][other_state])
            FOR each symbol
                log_emit[state][symbol] = safe_log(emit_probs[state][symbol])

        # Check: log_init[G]     = ln(0.8) = -0.2231
        #        log_trans[G][G] = ln(0.9) = -0.1054
        #        log_emit[I][C]  = ln(0.4) = -0.9163

```
5. VITERBI
```
    FUNCTION viterbi(sequence)

        # Step 0: check the input
        IF sequence is empty
            STOP with error "empty sequence"
        FOR each symbol in sequence
            IF symbol is not in symbols
                STOP with error "unknown symbol"

        # Step 0: make the two tables
        MAKE score table -> one row per state, one column per symbol in sequence
        MAKE arrow table -> one row per state, one column per symbol in sequence

        # Step 1: column 1 (no ways in yet, use initial probabilities)
        FOR each state
            score[state][1] = log_init[state] + log_emit[state][symbol 1]
            arrow[state][1] = nothing

        # Check: score[I][1] = ln(0.2) + ln(0.4) = ln(0.08) = -2.5257
        #        score[G][1] = ln(0.8) + ln(0.2) = ln(0.16) = -1.8326

        # Step 2: columns 2 to the end (try every way in, keep the best)
        FOR each column from 2 to the last
            FOR each state_now
                best_road = minus infinity
                best_from = nothing
                FOR each state_before
                    road = score[state_before][column - 1]
                         + log_trans[state_before][state_now]
                    IF road is bigger than best_road
                        best_road = road
                        best_from = state_before
                score[state_now][column] = best_road
                                         + log_emit[state_now][this column's symbol]
                arrow[state_now][column] = best_from

        # Check (column 2, state I):
        #   from I: ln(0.08) + ln(0.7) = ln(0.056)  <- bigger, arrow = I
        #   from G: ln(0.16) + ln(0.1) = ln(0.016)
        #   score[I][2] = ln(0.056) + ln(0.4) = ln(0.0224) = -3.7987

        # Step 3: best ending
        best_last_state = the state with the biggest score in the last column
        best_log_prob   = that score
        IF best_log_prob is minus infinity
            STOP with error "no possible path for this sequence"

        # Check: last column I = -17.2249, G = -13.9291  -> ends in G

        # Step 4: trace back
        # stand on a box, read ITS arrow, jump to that state one column left
        path = empty list
        standing_on = best_last_state
        FOR each column from the last down to 1
            ADD standing_on to path
            standing_on = arrow[standing_on][column]
        REVERSE path   # we collected it backwards

        # Step 5: return
        RETURN path, best_log_prob
 ```  
6. TESTS
```
TEST one symbol          viterbi("G")         -> path G,         prob 0.16
TEST two symbols         viterbi("GG")        -> path G G,       prob 0.0288
TEST three symbols       viterbi("GGC")       -> path I I I,     prob 0.006272
TEST class example       viterbi("GGCACTGAA") -> path all G,     log prob -13.9291
TEST different model     primer model (T/U states, none/few/many symbols)
                         on [none, few, many, many, none, many, none]
                                              -> path U U T T T T U, prob about 0.0000097
TEST unknown symbol      viterbi("GGNA")      -> error
TEST empty sequence      viterbi("")          -> error
TEST broken table        emissions add up to 0.9 -> error when creating the model
TEST long sequence       1,800 symbols        -> log prob is a real number, not minus infinity
```
