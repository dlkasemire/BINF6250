# Introduction

This project implements the Viterbi algorithm for hidden Markov models (HMMs). An HMM has hidden states we cannot see that emit symbols we can see. Given a sequence of observations, Viterbi answers one question: what single sequence of hidden states has the highest joint probability with the observations? This is the decoding problem, one of Rabiner's (1989) three classic HMM questions. We expect the next following projects to cover evaluation and learning.

Our program does this in four stages:

1.  Set up and check the model: read the state names and alphabet from the input dictionaries (nothing hard-coded), check that the dictionaries agree and that every row sums to 1, then convert every probability to a log once. This stage should be applicable toward other HMM models.\

Stage 2 - 4 is for Viterbi Algorithm specifically: \
2. Initialize: fill the first column of the dynamic programming table with initial probability + emission probability of the first symbol (in log space).\
3. Recurse: for every later position and every state, keep only the best way in from the previous column, store its score, and store a back-pointer to where it came from. \
4. Terminate and trace back: pick the best state in the last column, then follow the back-pointers to rebuild the full path.

# Documentation and Results

### Requirements

-   Python 3.14
-   Jupyter Notebook
-   `math` (standard library)

### Usage

Open `project08.ipynb` in Jupyter and run all cells in order, top to bottom (Kernel → Restart & Run All). The notebook is split into:\
Imports: `math`\
Model setup: `HMM` class with `__init__()`, `safe_log()`, `_validate()`, `_convert_to_logs()`\
Decoding: `HMM.viterbi()`\

Example call:

```         
hmm = HMM(init_probs, trans_probs, emit_probs)
path, log_prob = hmm.viterbi("GGCACTGAA")
```
### Project structure

```         
project08/
├── project08.ipynb
├── README.md
```

### Data

There is no data file. We used the four example data structures from the project description:

```         
#I = CpG Island and G = Genome
obs = "GGCACTGAA"
init_probs  = {"I": 0.2, "G": 0.8}
trans_probs = {"I": {"I": 0.7, "G": 0.3}, "G": {"I": 0.1, "G": 0.9}}
emit_probs  = {"I": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1},
               "G": {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3}}
```
Terms used throughout this README:

| Term | Meaning | Input dictionary | Log table in the class |
|------------------|------------------|------------------|------------------|
| **Initial probability** | chance the first position is in each state | `init_probs` | `log_init` |
| **Transition probability** | chance of moving from state i to state j at the next position | `trans_probs` | `log_trans` |
| **Emission probability** | chance a state emits a given symbol | `emit_probs` | `log_emit` |

### Output

### Note about the materials:

# Pseudocode

# We will use the example obs = "GGCACTGAA" for demonstrating

## Stage 1: Set up and check the model

```         
   #example input: the four data structures in the Data section
   #states = ['I', 'G'], symbols = ['A', 'C', 'G', 'T']
```

1.  Create the model

```         
class HMM:
  def __init__(init_probs, trans_probs, emit_probs):
    #1. Save the three tables inside the model
    save init_probs, trans_probs, emit_probs

    #2. Get the state names from the data, not hard-code them
    # states = ['I', 'G']
    states = list of the keys of init_probs
    # stop if there are no states at all
    if states is empty:
        raise error "init_probs has no states"

    #3. Get the alphabet from the emission probabilities of the first state
    # symbols = ['A', 'C', 'G', 'T']
    symbols = list of the keys of emit_probs[first state]

    #4. Check the inputs before doing anything else (function 3)
    _validate()

    #5. Convert every probability to a log, once, upfront (function 4)
    _convert_to_logs()
```

2.  Safe log

```         
  def safe_log(p):
    #1. log(0) is undefined: math.log(0) crashes, numpy.log(0) gives -inf with a warning
    # so we choose -inf ourselves: an impossible event stays impossible,
    # because -inf + anything = -inf, and -inf loses every comparison
    if p == 0:
        return -infinity

    #2. Otherwise, the natural log
    return ln(p)

    # Check: safe_log(1)   -> 0.0
    #        safe_log(0.8) -> -0.2231
    #        safe_log(0)   -> -inf
```

3.  Validate

```         
  def _validate():
    #1. The keys must agree across all three dictionaries
    # catches typos like 'g' in one place and 'G' in another
    check keys of trans_probs == states
    check keys of emit_probs == states
    check keys of every trans_probs[i] == states
    # every state must list every symbol
    check keys of every emit_probs[s] == symbols

    #2. Every value must be a real probability
    check every value is between 0 and 1

    #3. Every row must sum to 1, with a small tolerance
    # tolerance because 0.1 + 0.2 = 0.30000000000000004 in floating point
    # for the example: 0.2 + 0.8 = 1; 0.7 + 0.3 = 1; 0.1 + 0.4 + 0.4 + 0.1 = 1
    check sum(init_probs) is within 1e-6 of 1
    check each row of trans_probs sums to 1 (within 1e-6)
    check each row of emit_probs sums to 1 (within 1e-6)

    # if any check fails: raise an error that says which check and which state

    # Check: the example data            -> passes
    #        init_probs = {'I': 0.2, 'G': 0.7} -> raises error (sums to 0.9)
```

4.  Convert to logs

```         
  def _convert_to_logs():
    # Convert every probability to a log, once, upfront
    # (Viterbi reuses the same few numbers many times, so converting once is faster)

    # Initial probabilities: one log per state
    # example: log_init['G'] = ln(0.8) = -0.2231
    for each state s:
        log_init[s] = safe_log(init_probs[s])

    # Transition probabilities: one log per pair of states (from i, to j)
    # for the example: log_trans['G']['G'] = ln(0.9) = -0.1054
    for each pair of states i, j:
        log_trans[i][j] = safe_log(trans_probs[i][j])

    # Emission probabilities: one log per state and symbol
    # for the example: log_emit['I']['C'] = ln(0.4) = -0.9163
    for each state s and each symbol in symbols:
        log_emit[s][symbol] = safe_log(emit_probs[s][symbol])

    # after this, Viterbi only adds these logs and never calls log inside its loops

    # store log_init, log_trans, log_emit on the object
    # We anticipate that next project will reuse them
```

## Stage 2–4: Viterbi

### The Viterbi formula (from the course primer)

The Viterbi formula as given in the course primer, *A primer on HMMs* (Figure 3, notation from Rabiner, 1989):

| Step | Formula |
|---|---|
| Start | `delta_1(i) = pi_i * b_i(o_1),  psi_1(i) = 0,  1 <= i <= N` |
| Move forward one position | `delta_t(j) = max_i( delta_(t-1)(i) * a_ij ) * b_j(o_t),  2 <= t <= T` |
| | `psi_t(j) = argmax_i( delta_(t-1)(i) * a_ij ),  2 <= t <= T` |
| Finish | `P* = max_i( delta_T(i) ),  q*_T = argmax_i( delta_T(i) )` |
| Trace back | `q*_t = psi_(t+1)( q*_(t+1) ),  t = T-1, T-2, ..., 1` |

### What the symbols mean (and their names in our code)

**Positions and states**
- `O` = the observation sequence `o_1 … o_T` (`sequence`); `T` = its length (`n`)
- `t` = the position, which letter we are on, counted from 1 (our code counts columns from 0, so position `t` is column `t - 1`)
- `o_t` = the letter at position `t`
- `i` = a state we come **from** (`state_before`); `j` = a state we go **to** (`state_now`); `N` = the number of states

**Model probabilities** (built and checked once in Stage 1, by `safe_log()`, `_validate()`, and `_convert_to_logs()`)
- `pi_i` = initial probability of state i (`log_init[i]`)
- `a_ij` = transition probability from state i to state j (`log_trans[i][j]`)
- `b_j(o_t)` = emission probability of letter `o_t` in state j (`log_emit[j][o_t]`)

**What Viterbi computes** (function 5)
- `delta_t(j)` = score of the best path for the first t letters that ends in state j (`score[t-1][j]`)
- `psi_t(j)` = the arrow: which state the best path into j at position t came from (`arrow[t-1][j]`); `psi_1(i) = 0` means no arrow (`None`)
- `max_i` = the biggest value over every i (`best_road`); `argmax_i` = which i gave it (`best_from`)
- `P*` = the probability of the best path (`best_log_prob` stores its log); `q*_T` = its last state (`best_last_state`); `q*` = the best path (`path`)

### The difference between the formula and our code

- **Logs instead of probabilities.** To avoid underflow, our code uses the log of every probability. So `*` becomes `+`, the max stays a max, and probability `0` becomes `-inf`. That is why `score`, `log_init`, `log_trans`, and `log_emit` all hold logs.

### Pseudocode

```         
   #example: sequence = "GGCACTGAA", n = 9, states = I, G
```

5.  Viterbi decoding (in log units)

```         
  def viterbi(sequence):
    #1. Preparation:
    # Check the input sequence and its letters: 
    if sequence is empty:
        raise error "empty sequence"
    for each symbol in sequence:
        if symbol is not in symbols:
            raise error "unknown symbol"

    # Set up the 2 matrices: score for best-scores-in-logs and arrow for traceback direction 
    n = length of sequence
    # one column per letter, columns 0 to n-1 (Python counts from 0, so column t holds sequence[t])
    score = table with one row per state, columns 0 to n-1
    arrow = table with one row per state, columns 0 to n-1

    #2. Initialisation 
    # the first letter has no previous column, so use the initial probability
    first = sequence[0]
    for each state s:
        # cell score = log initial probability + log emission probability of the first letter
        # example: score[0]['G'] = ln(0.8) + ln(0.2) = -1.8326
        score[0][s] = log_init[s] + log_emit[s][first]
        # no arrow: nothing comes before the first letter
        arrow[0][s] = None

    #3. Recursion
    # fill both tables column by column, left to right, starting from the second letter
    for t from 1 to n-1:
        # the letter for this column
        symbol = sequence[t]
        # fill one cell: state_now at column t
        for each state_now:
            # start with the worst possible score
            best_road = -inf
            # no arrow yet
            best_from = None
            # try every way in: each state_before in the previous column
            for each state_before:
                # score of this way in = score of cell state_before + log transition probability from state_before to state_now
                # example: t = 1, state_now = 'I', state_before = 'I': -2.5257 + ln(0.7) = -2.8824
                road = score[t-1][state_before] + log_trans[state_before][state_now]
                # if this way in is the best so far, keep it
                if road > best_road:
                    # keep its score
                    best_road = road
                    # keep its arrow (which state_before it came from)
                    best_from = state_before
            # cell score = best way in + log emission probability of this letter
            # (added once, after the loop, because it is the same for every way in)
            # example: t = 1, state_now = 'I': -2.8824 + ln(0.4) = -3.7987
            score[t][state_now] = best_road + log_emit[state_now][symbol]
            # cell arrow = where the best way in came from
            # example: t = 1, state_now = 'I': 'I'
            arrow[t][state_now] = best_from

    #4. Termination
    # the best path ends in the state with the biggest score in the last column
    # example: I = -17.2249, G = -13.9291 => ends in 'G'
    best_last_state = the state with the largest score[n-1]
    # the score of the best path
    best_log_prob = score[n-1][best_last_state]
    # if even the best score is -inf, every path is impossible: stop
    if best_log_prob == -inf:
        raise error "no possible path for this sequence"

    #5. Traceback
    # start at the last state and follow the arrows back
    path = empty list
    standing_on = best_last_state
    # go back one column at a time, from the last column down to column 0
    for t from n-1 down to 0:
        # add the state we are standing on
        append standing_on to path
        # read its arrow and jump to that state one column left (column 0's arrow is None)
        standing_on = arrow[t][standing_on]
    # we collected the path backwards, so flip it
    reverse path

    #6. Return
    # the best path and its log probability
    return path, best_log_prob
```
Reflection narrative that describes what went right, what went wrong, what you didn't understand, how it could have been better, and how you could have been better.

Appendix (AI usage, citations, etc.)
