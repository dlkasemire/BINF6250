# Introduction

This project implements the Viterbi algorithm for hidden Markov models (HMMs). An HMM has hidden states we cannot see that emit symbols we can see. Given a sequence of observations, Viterbi answers one question: what single sequence of hidden states has the highest joint probability with the observations? This is the decoding problem, one of Rabiner's (1989) three classic HMM questions. We expect the next following projects to cover evaluation and learning.

Our program does this in four stages:

1.  Set up and check the model: read the state names and alphabet from the input dictionaries (nothing hard-coded), check that the dictionaries agree and that every row sums to 1, then convert every probability to a log once. This stage should be applicable toward other HMM models.

Stage 2 - 4 is for Viterbi Algorithm specifically:
2. Initialize: fill the first column of the dynamic programming table with initial probability + emission probability of the first symbol (in log space).
3. Recurse: for every later position and every state, keep only the best way in from the previous column, store its score, and store a back-pointer to where it came from.
4. Terminate and trace back: pick the best state in the last column, then follow the back-pointers to rebuild the full path.

# Documentation and Results

### Requirements

-   Python 3.14
-   Jupyter Notebook
-   `math` (standard library)
-   `itertools` (standard library, used by the brute-force test)

### Usage

Open `project08.ipynb` in Jupyter and run all cells in order, top to bottom (Kernel → Restart & Run All). The notebook is split into:
1. Imports and settings: `math`, `itertools`, `NEG_INF`, `TOLERANCE`
2. The `HMM` class: `__init__()`, `safe_log()`, `_validate()`, `_convert_to_logs()`, `viterbi()`
3. Demonstration on the example data
4. Tests: one cell with every test, each printing PASS or FAIL

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

The demonstration cell prints:

```         
states : ['I', 'G']
symbols: ['A', 'C', 'G', 'T']

observation : GGCACTGAA
best path   : GGGGGGGGG
log prob    : -13.9291
probability : 8.926e-07
```

**Result interpretation**

1.  **What the result says.** The best path for `GGCACTGAA` is `GGGGGGGGG`: every letter is labeled genome background (G), so no CpG island is called.

2.  **Why: the island is expensive to enter and leave.** Entering the island (transition probability 0.1, versus 0.9 for staying in G) is 9 times worse, and leaving it (0.3, versus 0.9) is 3 times worse. The island only earns this back through emissions: it emits C or G with probability 0.4 instead of 0.2 (2 times better), but A or T with only 0.1 instead of 0.3 (3 times worse).

3.  **Why this sequence stays in background state (G).** Its only C/G run (G G C) is short and is followed by A's and T's, so leaving the island costs more than the run earns.

4.  **Tests**: All 21 tests in the notebook pass. Each group of tests checks a different part of the code, so together they give us confidence that the whole program works.
    The hand-checked tests show that the math in each step is right, since the code gives the same numbers we got on paper.
    Brute force shows that Viterbi really finds the best path: on every short sequence we tried, it chose the same path as checking all possible paths one by one, with 2 and 3 states.
    The primer’s model shows the code isn’t tied to our example, since it works with different states and symbols and matches a published answer.
    The error tests show that bad input stops the code with a clear message instead of giving a wrong path, and the long-sequence and underflow tests show that working in logs keeps the scores usable even when plain probabilities would drop to zero.
    Passing these tests does not prove the code is correct in every possible case: they cover the cases we thought to check, and brute force can only confirm short sequences.

# Pseudocode

We will use the example obs = "GGCACTGAA" for demonstrating

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
|-----------------------|------------------------------------------------|
| Initialisation | `delta_1(i) = pi_i * b_i(o_1),  psi_1(i) = 0,  1 <= i <= N` |
| Recursion | `delta_t(j) = max_i( delta_(t-1)(i) * a_ij ) * b_j(o_t),  2 <= t <= T` |
|  | `psi_t(j) = argmax_i( delta_(t-1)(i) * a_ij ),  2 <= t <= T` |
| Termination | `P* = max_i( delta_T(i) ),  q*_T = argmax_i( delta_T(i) )` |
| Trace back | `q*_t = psi_(t+1)( q*_(t+1) ),  t = T-1, T-2, ..., 1` |

### What the symbols mean (and their names in our code)

**Positions and states**

-   `O` = the observation sequence `o_1 … o_T` (`sequence`); `T` = its length (`n`)
-   `t` = the position, which letter we are on, counted from 1 (our code counts columns from 0, so position `t` is column `t - 1`)
-   `o_t` = the letter at position `t`
-   `i` = a state we come **from** (`state_before`); `j` = a state we go **to** (`state_now`); `N` = the number of states

**Model probabilities** (built and checked once in Stage 1, by `safe_log()`, `_validate()`, and `_convert_to_logs()`)

-   `pi_i` = initial probability of state i (`log_init[i]`)
-   `a_ij` = transition probability from state i to state j (`log_trans[i][j]`)
-   `b_j(o_t)` = emission probability of letter `o_t` in state j (`log_emit[j][o_t]`)

**What Viterbi computes** (function 5)

-   `delta_t(j)` = score of the best path for the first t letters that ends in state j (`score[t-1][j]`)

-   `psi_t(j)` = the arrow: which state the best path into j at position t came from (`arrow[t-1][j]`); `psi_1(i) = 0` means no arrow (`None`)

-   `max_i` = the biggest value over every i (`best_road`); `argmax_i` = which i gave it (`best_from`)

-   `P*` = the probability of the best path (`best_log_prob` stores its log); `q*_T` = its last state (`best_last_state`); `q*` = the best path (`path`) ### The difference between the formula and our code

**Logs instead of probabilities.** To avoid underflow, our code uses the log of every probability. So `*` becomes `+`, the max stays a max, and probability `0` becomes `-inf`. That is why `score`, `log_init`, `log_trans`, and `log_emit` all hold logs.

### Pseudocode

```         
   #example: sequence = "GGCACTGAA", n = 9, states = I, G
```

5.  Viterbi decoding (in log units)

```         
  def viterbi(sequence):
    #0. Preparation:
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

    #1. Initialisation 
    # the first letter has no previous column, so use the initial probability
    first = sequence[0]
    for each state s:
        # cell score = log initial probability + log emission probability of the first letter
        # example: score[0]['G'] = ln(0.8) + ln(0.2) = -1.8326
        score[0][s] = log_init[s] + log_emit[s][first]
        # no arrow: nothing comes before the first letter
        arrow[0][s] = None

    #2. Recursion
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

    #3. Termination
    # the best path ends in the state with the biggest score in the last column
    # example: I = -17.2249, G = -13.9291 => ends in 'G'
    best_last_state = the state with the largest score[n-1]
    # the score of the best path
    best_log_prob = score[n-1][best_last_state]
    # if even the best score is -inf, every path is impossible: stop
    if best_log_prob == -inf:
        raise error "no possible path for this sequence"

    #4. Traceback
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

# Reflection narrative

### What went right:

**Program worked**
All 21 tests pass: the code reproduces the answers we worked out by hand, and on every sequence we tried, with both 2 and 3 states, it finds the same best path as brute force, which checks every possible path one by one. Our way of working also paid off. Because we each wrote our own pseudocode first and then compared them, we could see that both versions gave exactly the same results, and that let us confidently choose the simpler one.

**How our code answers some the project's design questions and notes**
Our code uses only the four data structures the project gives us and makes no assumptions about what they model. **init**() takes the states from init_probs and the symbols from the emission probabilities, so nothing is hard-coded, and _validate() then checks that the keys match across all three dictionaries, that every value is between 0 and 1, and that every row adds up to 1. Because of this, the same class runs the CpG example, the course primer’s model (with different states and symbols), and a three-state model without any changes. Before decoding, _convert_to_logs() turns every probability into a log once, which keeps long sequences from underflowing; the max still picks the right winner, because log keeps the same order (if a > b, then log a > log b). 

A probability of 0 becomes -inf through safe_log(), so an impossible event stays impossible, which we test with an initial probability of 0 and with a model where every path is impossible. viterbi() returns both the best path and its log probability rather than the plain probability, since the plain probability drops to 0.0 on long sequences. If the observation contains a symbol no state can emit, it stops with an “unknown symbol” error instead of returning a path that looks real but means nothing. Its three nested loops take O(N × K²) time, and its score and arrow tables use O(N × K) memory. Finally, our first tests are the hand-checkable answers the project asks for: G gives a probability of 0.16 and GG gives 0.0288, the same numbers we worked out on paper.

### Our Limitations and how it could be improved:

A few parts of the project page are not fully covered by our design. We store the model’s parts on the class so that later algorithms can reuse them, but Forward, Backward, and Baum-Welch are not built yet, so we have not tested how well the class extends (design question 2). For zero probabilities, we chose -inf through safe_log() and did not try pseudocounts to compare the two approaches. Our viterbi() returns a single best path and gives no measure of how confident we can be in each label, so we did not explore whether the most probable path can differ from the most probable state at each position; the page says Project 09 will answer this. If two paths tie for the best score, the code keeps the first state in dictionary order without reporting the tie. Finally, because the symbols come from the first state’s emission probabilities, every state must list every symbol, and if the first state is the one missing a symbol, the error message names a different state. 

### What we still didn't understand : 

**Ties
When two ways into a cell have exactly the same score, our code keeps the first one (`road > best_road`), and `max(...)` does the same at the end. The path it returns is still a most likely path, but if other paths are equally likely, the code doesn't tell the user. We're not sure whether that matters in practice, or how tools usually report it.

**Checking correctness on long sequences.**
Our brute-force test proves Viterbi matches the best of every possible path, but only for short sequences, since the number of paths doubles with each symbol. For long sequences we can only check that the score isn't -inf, not that the path is right.

**Choosing tolerances**
We used 1e-6 to check that rows add up to 1, 1e-4 to compare our scores with hand-calculated values, and 1e-9 to compare with brute force. Each worked, but we picked them by judgment rather than by a rule. Each tolerance was chosen to be larger than the error we expected in that comparison, but much smaller than a real mistake. We're not sure whether there's a more standard way to choose them.

**Every state must list every symbol**
`_validate` requires each emission row to include every symbol, even if its probability is 0. We aren't sure whether a real model might reasonably leave symbols out, and whether we should allow that (treating a missing symbol as probability 0).

### Personal Reflection: 

-   Trang Do: Dianah and I enjoyed working together, and being in the same time zone made planning easy. In our first meeting, we worked through the example by hand. Doing it this way made the algorithm click for us in a way the formula alone didn’t, and it gave us expected values (0.16 for G and 0.0288 for GG) that later became our first tests. After that, we each wrote our own pseudocode. Mine followed Durbin et al.’s formula from the lecture slide, including a silent BEGIN state and an extra column 0 before the first letter. Dianah’s skipped BEGIN and filled the first column directly with the initial probability times the emission probability. When we compared them, both gave exactly the same results, but hers was simpler. Honestly, although I thought I understood the BEGIN part of my own version, I could barely explain it back, and if it confused me, it would probably confuse a reviewer too. So we went with Dianah’s version. I built on her notebook by adding four checks (brute force, a three-state model, an initial probability of 0, and an impossible path) plus two underflow checks, and I changed her tests to print PASS or FAIL for each one.

-   Dianah Kasemire: This project was a little confusing at the start, but working together with Trang made things simpler. We met up and worked through the task by hand which gave a clearer picture of what the movement was like. It still gets a bit confusing as you continue moving along the table because of the many numbers and how the maths is done, but knowing the concept helped. Starting the pseudocode was another challenge altogether. Breaking it into small parts helped: setting up the model, filling the first column, filling the rest of the columns, and then tracing back. The trace back confused me the longest. I first thought you read all the arrows along one row, but each arrow belongs only to its own box, so you follow the arrow of the box you are standing on. Going through the code one line at a time helped a lot, and testing it against the values we worked out by hand showed it was doing the same thing we did on paper.

# Appendix (AI usage, citations, etc.)

### AI usage

We used Claude (Anthropic, Claude Opus 5.5) during November 2026 to provide guidance while we worked through the example by hand. We also used Claude to structure our notebook Markdown (the formula section, the symbol list, and the test list). We had also used Claude to review our code and whether it had addressed all of the design requirement given in the assignment. Outside of project 08, we also had used it to help summarized and provide detailed explanation of what we might not understand fully in the provided reading "A primer on HMMs: From one picture to five algorithms."

### Citations 

-   Durbin, R., Eddy, S. R., Krogh, A., & Mitchison, G. (1998). *Biological sequence analysis: Probabilistic models of proteins and nucleic acids.* Cambridge University Press. <https://doi.org/10.1017/CBO9780511790492> 
-   Rabiner, L. R. (1989). A tutorial on hidden Markov models and selected applications in speech recognition. *Proceedings of the IEEE, 77*(2), 257–286. <https://doi.org/10.1109/5.18626>
-   *A primer on HMMs: From one picture to five algorithms.* BINF6250 Algorithmic Foundations in Bioinformatics course material, Fall 2026. 
-   *Project 08: The Viterbi algorithm for hidden Markov models.* BINF6250 project description, Fall 2026.
