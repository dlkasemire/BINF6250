# Introduction

This project extends our Project 08 `HMM` class with three new algorithms: Forward, Backward, and Forward-Backward. Viterbi (Project 08) answered "what is the single best path of hidden states?" Project 09 answers two new questions about **every** path at once:

1.  **Evaluation:** how likely is the whole observation sequence under the model, counting every possible path? (Forward and Backward, Rabiner's (1989) evaluation problem)
2.  **Posterior decoding:** how sure can we be about the state at each position, given the whole sequence? (Forward-Backward)

Our program does this in five stages:

1.  Set up and check the model: unchanged from Project 08.

2.  Shared helpers:

    one input check for every algorithm, 

    one left-to-right sweep that both Viterbi and Forward use, so the `max`-based and `sum`-based recursions are not two copies of the same loop,

    a safe log-sum-exp.

3.  Forward: sweep left to right, adding every way into each cell, then add up the last column to get the probability of the whole sequence.

4.  Backward: sweep right to left, adding every way out of each cell to the end, then fold in the initial probability and the first emission probability to get the same probability.

5.  Forward-Backward: combine the two tables to get the posterior probability of each state at each position.

# Documentation and Results

### Requirements

-   Python 3.14
-   Jupyter Notebook
-   `math` (standard library)

### Usage

Open `project09.ipynb` in Jupyter and run all cells in order, top to bottom (Kernel → Restart & Run All). The notebook is split into:

1.  Imports and settings: `math`, `itertools`, `NEG_INF`, `TOLERANCE`, `LOG_TOLERANCE`
2.  The `HMM` class:
    -   From Project 08: `__init__()`, `safe_log()`, `_validate()`, `_convert_to_logs()`, `viterbi()`
    -   New helpers: `_check_sequence()`, `log_sum_exp()`, `_sweep_left_to_right()`
    -   New algorithms: `forward()`, `backward()`, `forward_backward()`
3.  Demonstration on the example data
4.  Tests: one cell with every test, each printing PASS or FAIL

Example call:

```         
hmm = HMM(init_probs, trans_probs, emit_probs)
forward_table, log_px = hmm.forward("ATGCAA")
backward_table, log_px_back = hmm.backward("ATGCAA")
result = hmm.forward_backward("ATGCAA")
result["posterior"][0]["E"]     # chance position 1 is in state E
```

### Project structure

```         
project09/
├── project09.ipynb
├── README.md
```

### Data

There is no data file. We used the four example data structures from the project description:

```         
# E = Exon and I = Intron (note: in Project 08, "I" meant CpG Island)
obs = "ATGCAA"
init_probs  = {"E": 0.6, "I": 0.4}
trans_probs = {"E": {"E": 0.8, "I": 0.2}, "I": {"E": 0.3, "I": 0.7}}
emit_probs  = {"E": {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3},
               "I": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1}}
```

Terms used throughout this README:

| Term | Meaning | Input dictionary | Log table in the class |
|------------------|------------------|------------------|------------------|
| **Initial probability** | chance the first position is in each state | `init_probs` | `log_init` |
| **Transition probability** | chance of moving from state i to state j at the next position | `trans_probs` | `log_trans` |
| **Emission probability** | chance a state emits a given symbol | `emit_probs` | `log_emit` |
| **Forward value** | chance of seeing the first t symbols and being in state i at position t | (computed) | `forward_table[t-1][i]` (log) |
| **Backward value** | chance of seeing the rest of the symbols (t+1 to T), given state i at position t | (computed) | `backward_table[t-1][i]` (log) |
| **Posterior probability** | chance position t is in state i, given the whole sequence | (computed) | `posterior[t-1][i]` (plain probability) |

### Output

**Result interpretation**

### Design: what we reused and what we refactored from project08

Reused unchanged from Project 08:

-   init(), safe_log(), \_validate(), and \_convert_to_logs() stay exactly as they were. Forward and Backward need the same log tables and the same checks on the model. \# Pseudocode

Moved out of `viterbi()` so other algorithm can use it:

-   The input checks at the top of `viterbi()` (empty sequence, unknown symbol) moved into `_check_sequence()`. All four algorithms need the same checks.

-   Viterbi's left-to-right loop moved into `_sweep_left_to_right()`. Viterbi and Forward are the same loop, except that Viterbi keeps the best way into each cell and Forward adds every way in.

Stayed in `viterbi()`

-   Viterbi's termination and traceback stay in `viterbi()`. Forward has no arrows to follow.

### Pseudocode

## Stage 1: Set up and check the model (unchanged from Project 08)

```         
   #example input: the four data structures in the Data section
```

1.  Create the model

```         
class HMM:
  def __init__(init_probs, trans_probs, emit_probs):
    #1. Save the three tables inside the model
    save init_probs, trans_probs, emit_probs

    #2. Get the state names from the data, not hard-code them
    # states = ['E', 'I']
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
    #1. log(0) is undefined, so we choose -inf ourselves: an impossible event stays impossible
    if p == 0:
        return -infinity

    #2. Otherwise, the natural log
    return ln(p)
```

3.  Validate

```         
  def _validate():
    #1. The keys must agree across all three dictionaries
    check keys of trans_probs == states
    check keys of emit_probs == states
    check keys of every trans_probs[i] == states
    check keys of every emit_probs[s] == symbols

    #2. Every value must be a real probability
    check every value is between 0 and 1

    #3. Every row must sum to 1, within 1e-6
    check sum(init_probs), each row of trans_probs, and each row of emit_probs

    # if any check fails: raise an error that says which check and which state
```

4.  Convert to logs

```         
  def _convert_to_logs():
    # Initial probabilities: one log per state
    for each state s:
        log_init[s] = safe_log(init_probs[s])

    # Transition probabilities: one log per pair of states (from i, to j)
    for each pair of states i, j:
        log_trans[i][j] = safe_log(trans_probs[i][j])

    # Emission probabilities: one log per state and symbol
    # example: log_emit['I']['C'] = ln(0.4) = -0.9163
    for each state s and each symbol in symbols:
        log_emit[s][symbol] = safe_log(emit_probs[s][symbol])
```

## Stage 2: Shared helpers (new) 

5.  Check the sequence input

```         
  def _check_sequence(sequence):
    #1. No symbols means no columns and no path
    if sequence is empty:
        raise error "empty sequence"

    #2. Every symbol must be one the model knows
    for each symbol in sequence:
        if symbol is not in symbols:
            raise error "unknown symbol"
```
6.  One left-to-right sweep for Viterbi and Forward (reused from project 08, def viterbi() without termination and traceback)

```         
  def _sweep_left_to_right(sequence, mode):
    # mode = "best" for Viterbi (keep the best way in, remember where it came from)
    # mode = "all"  for Forward (add every way in, no arrows)

    #1. Set up the 2 tables, one column per symbol
    n = length of sequence
    table = list of n empty dictionaries
    arrow = list of n empty dictionaries

    #2. Initialisation: the first symbol has no previous column, so use the initial probability
    first = sequence[0]
    for each state s:
        # cell score = log initial probability + log emission probability of the first symbol
        # example: table[0]['E'] = ln(0.6) + ln(0.3) = -1.7148 = ln(0.18)
        table[0][s] = log_init[s] + log_emit[s][first]
        # no arrow: nothing comes before the first symbol
        arrow[0][s] = None

    #3. Recursion: fill the table column by column, left to right
    for t from 1 to n-1:
        # the symbol for this column
        symbol = sequence[t]
        # fill one cell: state_now at column t
        for each state_now:
            # every way in: score of state_before + log transition probability into state_now
            # example: t = 1, state_now = 'E': [ln 0.18 + ln 0.8, ln 0.04 + ln 0.3] = [-1.9379, -4.4228]
            roads = [table[t-1][state_before] + log_trans[state_before][state_now] for each state_before]

            if mode == "best":
                # Viterbi: keep the best road (strict ">" keeps the first state on a tie, as in Project 08)
                best_road, best_from = the largest road and the state_before it came from
            else:
                # Forward: add every road
                # example: log_sum_exp([-1.9379, -4.4228]) = -1.8579 = ln(0.156)
                best_road = log_sum_exp(roads)
                # no arrow: every road counts, so there is no single place it came from
                best_from = None

            # cell score = combined roads + log emission probability of this symbol
            # (added once, after combining, because it is the same for every road)
            # example (Forward): t = 1, 'E': -1.8579 + ln(0.3) = -3.0619 = ln(0.0468)
            table[t][state_now] = best_road + log_emit[state_now][symbol]
            # remember the arrow (None for Forward)
            arrow[t][state_now] = best_from

    #4. Return both tables
    return table, arrow
```
7.  Log-sum-exp (new, to be used in def Forward())

```         
  def log_sum_exp(values):
    # adds probabilities that are stored as logs

    #1. Find the largest value
    # example: values = [-1.9379, -4.4228] (ln 0.144 and ln 0.012) -> m = -1.9379
    m = max(values)

    #2. If even the largest is -inf, every way is impossible
    # (without this, -inf - (-inf) gives nan, and nan spreads through the whole table)
    if m == -inf:
        return -inf

    #3. Factor out the largest, so the biggest term is e^0 = 1 and nothing rounds to 0
    # example: -1.9379 + ln(e^0 + e^(-2.4849)) = -1.9379 + ln(1.0833) = -1.8579 = ln(0.156)
    return m + ln( sum of e^(v - m) for each v in values )

    # Check: log_sum_exp([ln 0.144, ln 0.012]) -> ln(0.156) = -1.8579
    #        log_sum_exp([-1000, -1001])       -> -999.6867 (not an error)
    #        log_sum_exp([-inf, -inf])         -> -inf (not nan)
```

8.  Viterbi decoding (Project 08's function, now using the shared sweep)

```         
  def viterbi(sequence):
    #1. Check the input (function 5)
    _check_sequence(sequence)

    #2. Fill the score and arrow tables, keeping the best way in (function 6)
    score, arrow = _sweep_left_to_right(sequence, "best")

    #3. Termination and #4. Traceback: unchanged from Project 08
    # (best state in the last column, stop if -inf, follow the arrows back, reverse)

    #5. Return the best path and its log probability
    return path, best_log_prob
```

## Stage 3: Forward

### The Forward formula (from the course primer)

TODO: check each line against the primer's Figure 4 and Rabiner (1989). Same notation as our Project 08 README.

| Step | Formula |
|------------------------------------|------------------------------------|
| Initialisation | `alpha_1(i) = pi_i * b_i(o_1),  1 <= i <= N` |
| Recursion | `alpha_t(j) = [ sum_i( alpha_(t-1)(i) * a_ij ) ] * b_j(o_t),  2 <= t <= T` |
| Termination | `P(O) = sum_i( alpha_T(i) )` |

Compared with Viterbi, the only change is `sum` where Viterbi has `max`, and there is no `psi` (arrow).

**Symbols** (same as Project 08, plus): `alpha_t(i)` = forward value of state i at position t (`forward_table[t-1][i]`); `P(O)` = probability of the whole sequence (`log_px` stores its log). In logs, `*` becomes `+` and `sum` becomes `log_sum_exp`.

9.  Forward

```         
  def forward(sequence):
    #1. Check the input: call on function 5
    _check_sequence(sequence)

    #2. Fill the forward table,call on function 6
    forward_table, unused_arrows = _sweep_left_to_right(sequence, "all")

    #3. Termination: add up the last column, call on function 7
    log_px = log_sum_exp(forward_table[n-1][s] for each state s)

    #4. Return the table and the log probability of the whole sequence
    # (log_px = -inf means the sequence is impossible under the model; we return it rather than raise,
    #  because "probability 0" is a real answer to the evaluation question)
    return forward_table, log_px
```
