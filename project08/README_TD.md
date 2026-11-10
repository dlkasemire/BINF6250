# Introduction

This project implements the Viterbi algorithm for hidden Markov models (HMMs). An HMM has hidden states we cannot see that emit symbols we can see. Given a sequence of observations, Viterbi answers one question: what single sequence of hidden states has the highest joint probability with the observations? This is the decoding problem, one of Rabiner's (1989) three classic HMM questions. We expect the next following projects to cover evaluation and learning.

Our program does this in four stages:

1.  Set up and check the model: read the state names and alphabet from the input dictionaries (nothing hard-coded), check that the dictionaries agree and that every row sums to 1, then convert every probability to a log once. This stage should be applicable toward other HMM models.\

Stage 2 - 4 is for Viterbi Algorithm specifically: 
2. Initialize: fill the first column of the dynamic programming table with start probability + emission of the first symbol (in log space).
3. Recurse: for every later position and every state, keep only the best way in from the previous column, store its score, and store a back-pointer to where it came from. 
4. Terminate and trace back: pick the best state in the last column, then follow the back-pointers to rebuild the full path.

# Documentation and Results

### Requirements

-   Python 3.14
-   Jupyter Notebook
-   `math` (standard library)

### Usage

Open `project08.ipynb` in Jupyter and run all cells in order, top to bottom (Kernel → Restart & Run All). The notebook is split into:\
Imports: `math`\
Model setup: `HMM` class with `__init__()`, `safe_log()`, `validate()`\
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
    #1. Get the state names from the data, not hard-code them
    # states = ['I', 'G']
    states = list of the keys of init_probs

    #2. Get the alphabet from every symbol any state can emit
    # symbols = ['A', 'C', 'G', 'T']
    symbols = sorted set of every key inside every emit_probs[s]

    #3. Check the inputs before doing anything else
    validate(init_probs, trans_probs, emit_probs)

    #4. Convert every probability to a log, once, upfront
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
    # .get(symbol, 0): if a state doesn't list a symbol, use probability 0 (log = -inf)
    # for the example: log_emit['I']['C'] = ln(0.4) = -0.9163
    for each state s and each symbol in symbols:
        log_emit[s][symbol] = safe_log(emit_probs[s].get(symbol, 0))

    # after this, Viterbi only adds these logs and never calls log inside its loops

    # store states, symbols, log_init, log_trans, log_emit on the object
    # We anticipate that next project will reuse them
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
  def validate(init_probs, trans_probs, emit_probs):
    #1. The keys must agree across all three dictionaries
    # catches typos like 'g' in one place and 'G' in another
    check keys of trans_probs == states
    check keys of every trans_probs[i] == states
    check keys of emit_probs == states
    # no real state may be called "BEGIN" (see function 4)
    check "BEGIN" is not in states

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

4.  Log transition probability, with a starting point

```         
  # BEGIN is a pretend starting state that comes before the first symbol
  # it emits nothing; it only gives the first position somewhere to come from
  # its name must not match any real state name (checked in validate)
  BEGIN = "BEGIN"

  def log_transition(from_state, to_state):
    # one lookup for "the log probability of moving from from_state to to_state"
    # it is a class method so other algorithms in later projects can reuse it

    # moving from BEGIN means "starting" in to_state: use the initial probability
    # for the example: log_transition(BEGIN, 'G') = log_init['G'] = ln(0.8) = -0.2231
    if from_state == BEGIN:
        return log_init[to_state]

    # moving between two real states: use the transition probability
    # for the example: log_transition('G', 'G') = log_trans['G']['G'] = ln(0.9) = -0.1054
    return log_trans[from_state][to_state]

    # Check: log_transition(BEGIN, 'I') -> ln(0.2) = -1.6094
    #        log_transition('I', 'G')   -> ln(0.3) = -1.2040
```

## Stage 2–4: Viterbi

### The Viterbi formula (Durbin et al., 1998)

Durbin et al.'s formal description, as given in lecture:

| Step | Formula |
|---|---|
| Initialisation (i = 0) | `v_0(0) = 1,  v_k(0) = 0 for k > 0` |
| Recursion (i = 1 … L) | `v_l(i) = e_l(x_i) * max_k( v_k(i-1) * a_kl )` |
| | `ptr_i(l) = argmax_k( v_k(i-1) * a_kl )` |
| Termination | `P(x,pi*) = max_k( v_k(L) * a_k0 ),  pi*_L = argmax_k( v_k(L) * a_k0 )` |
| Traceback (i = L … 1) | `pi*_(i-1) = ptr_i(pi*_i)` |

### What the symbols mean (and their names in our code)

**Positions and states**
- `x` = the observation sequence `x_1 … x_L` (`x`); `L` = its length (`L`)
- `i` = the position, which letter we are on; `i = 0` means "before any letter"
- `x_i` = the letter at position `i` (`x[i-1]`, because Python counts from 0)
- `k` = a state we come **from**; `l` = a state we go **to**
- `0` = BEGIN, a pretend starting state that emits nothing (`BEGIN`)

**Model probabilities** (built and checked once in Stage 1, by `safe_log()` and `validate()`)
- `a_kl` = transition probability from state k to state l (`log_trans[k][l]`, through `log_transition(k, l)`)
- `a_0l` = moving from BEGIN to l, which is our **initial probability** of l (`log_init[l]`, through `log_transition(BEGIN, l)`)
- `a_k0` = moving into an END state; our input has none, so this is dropped (see below)
- `e_l(x_i)` = emission probability of letter `x_i` in state l (`log_emit[l][x_i]`)

**What Viterbi computes** (function 5)
- `v_k(i)` = score of the best path for the first i letters that ends in state k (`V[k][i]`)
- `ptr_i(l)` = the arrow: which state the best path into l at position i came from (`ptr[l][i]`)
- `max_k` = the biggest value over every k (`best_score`); `argmax_k` = which k gave it (`best_prev`)
- `pi*` = the best path, one state per letter (`path`); `pi*_L` = its last state (`pi_star_L`)
- `P(x,pi*)` = the probability of the best path (`best_log_prob` stores its log)

### Two differences between the formula and our code

- **Logs instead of probabilities.** To avoid underflow, our code uses the log of every probability. So `*` becomes `+`, the max stays a max, `1` becomes `0`, and `0` becomes `-inf`. That is why `V`, `log_init`, `log_trans`, and `log_emit` all hold logs.
- **No END state.** Durbin's termination multiplies by `a_k0`, a move into an END state. Our input has no END state, and when the end is not modelled this term disappears. So our termination just picks the biggest score in the last column.

### Pseudocode

```         
   #example: x = "GGCACTGAA", L = 9, states = I, G
```

5.  Viterbi decoding (Durbin et al., in log units)

```         
  def viterbi(x):
    #1. Preparation:
    # Check the input x and its letters: 
    if x is empty:
        raise error "empty observation"
    for each symbol in x:
        if symbol is not in symbols:
            raise error "unknown symbol"

    # Set up the 2 matrices: V for best-scores-in-logs and ptr for traceback direction 
    rows = [BEGIN] + states
    L = length of x
    V = table with one row per item in rows, columns 0 to L
    ptr = table with one row per item in rows, columns 0 to L

    #2. Initialisation 
    # before any symbol we are in BEGIN: log(1) = 0
    V[BEGIN][0] = 0
    # and not in any real state: log(0) = -inf
    for each state k:
        V[k][0] = -inf
    # nothing moves back into BEGIN, so its later columns stay -inf
    for i from 1 to L:
        V[BEGIN][i] = -inf

    #3. Recursion
    # fill both tables column by column, left to right (one letter at a time)
    for i from 1 to L:
        # the letter for this column (Python starts counting at 0)
        symbol = x[i-1]
        # fill one cell: state l at column i
        for each state l:
            # start with the worst possible score
            best_score = -inf
            # no arrow yet
            best_prev = None
            # try every way in: each state k in the previous column (BEGIN too)
            for each k in rows:
                # score of this way in = score of cell k + log transition probability from k to l
                # example: i = 1, l = 'G', k = BEGIN: 0 + ln(0.8) = -0.2231
                candidate = V[k][i-1] + log_transition(k, l)
                # if this way in is the best so far, keep it
                if candidate > best_score:
                    # keep its score
                    best_score = candidate
                    # keep its arrow (which k it came from)
                    best_prev = k
            # cell score = best way in + log emission probability of this letter
            # (added once, after the loop, because it is the same for every way in)
            # example: i = 1, l = 'G': -0.2231 + ln(0.2) = -1.8326
            V[l][i] = log_emit[l][symbol] + best_score
            # cell arrow = where the best way in came from
            # example: i = 1, l = 'G': BEGIN
            ptr[l][i] = best_prev

    #4. Termination
    # the best path ends in the state with the biggest score in the last column
    # (no END state in our input, so Durbin's a_k0 is dropped)
    # example: I = -17.2249, G = -13.9291 => ends in 'G'
    pi_star_L = the state k with the largest V[k][L]
    # the score of the best path
    best_log_prob = V[pi_star_L][L]
    # if even the best score is -inf, every path is impossible: stop
    if best_log_prob == -inf:
        raise error "no possible path for this observation"

    #5. Traceback
    # start at the last state and follow the arrows back
    path = [pi_star_L]
    # go back one column at a time; stop at column 2, because column 1's arrow points to BEGIN
    for i from L down to 2:
        # add the state the arrow points to
        append ptr[last item of path][i] to path
    # we collected the path backwards, so flip it
    reverse path

    #6. Return
    # the best path and its log probability
    return path, best_log_prob
    
    # Check: will do this whenever im done with the code writing 
```
