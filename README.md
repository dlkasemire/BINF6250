# BINF6250 - Project 05

# Introduction
This project implements the Smith-Waterman algorithm, a dynamic programming method for local pairwise sequence alignment that finds the highest-scoring shared region between two sequences under a customizable scoring system (defaults: match +1, mismatch -1, gap -1). The program fills a scoring matrix cell by cell, where each cell takes the largest of four options (up-left neighbor plus match or mismatch, up neighbor plus gap, left neighbor plus gap, or 0, which keeps scores from going negative), records the winning direction in a second matrix, and rebuilds the alignment by tracing those directions back from the highest score until it reaches a 0. The work is split across three functions: `cal_score()` scores one cell and returns its direction code (0 = END, 1 = DIAG, 2 = UP, 3 = LEFT), `traceback()` follows the directions to build the two aligned sequences, and `smith_waterman()` builds both NumPy matrices, fills them, finds and prints the best score, calls `traceback()`, and returns the results.  All required functionality described in the assignment instructions was completed. All three functions were implemented, and each was tested with a sanity check on a small example worked out by hand before the full program was run. Test 1 matches the expected output provided in the notebook, and Test 2, which has no expected output, was checked by reasoning through the scores in the printed matrix.

# Pseudocode
This pseudocode reflects the final code that was decided upon and not the original starting version.

### cal_score()
```
Get this row's letter: seq1 at position (i - 1)
Get this column's letter: seq2 at position (j - 1)

Diagonal number:
    IF this row's letter equals this column's letter:
        diag_score = matrix at (i - 1, j - 1) + match
    ELSE:
        diag_score = matrix at (i - 1, j - 1) + mismatch
up_score = matrix at (i - 1, j) + gap
left_score = matrix at (i, j - 1) + gap

score = biggest of: 0, diag_score, up_score, left_score

Pick the move (check in this order, first match wins if tied):
    IF score is 0:          move = 0 (END)
    ELIF score = diag:      move = 1 (DIAG)
    ELIF score = up:        move = 2 (UP)
    ELSE:                   move = 3 (LEFT)

Return score and move
```

### traceback()
```
aligned_seq1 = empty string
aligned_seq2 = empty string
current_row, current_col = maximum_position
current_move = traceback_matrix at (current_row, current_col)

WHILE current_move is not 0 (END):
    IF current_move is 1 (DIAG):
        add seq1 letter at (current_row - 1) to front of aligned_seq1
        add seq2 letter at (current_col - 1) to front of aligned_seq2
        move up one row and left one column
    ELIF current_move is 2 (UP):
        add seq1 letter at (current_row - 1) to front of aligned_seq1
        add "-" to front of aligned_seq2
        move up one row
    ELIF current_move is 3 (LEFT):
        add "-" to front of aligned_seq1
        add seq2 letter at (current_col - 1) to front of aligned_seq2
        move left one column

    current_move = traceback_matrix at (current_row, current_col)

Return aligned_seq1, aligned_seq2
```

### smith_waterman()
```
rows = length of seq1 + 1
cols = length of seq2 + 1
score_matrix = grid of zeros, size rows x cols (whole numbers, dtype=int)
traceback_matrix = grid of zeros, size rows x cols (whole numbers 0, 1, 2, 3, dtype=int)

max_score = 0
max_pos = (0, 0)

FOR i from 1 to rows - 1:
    FOR j from 1 to cols - 1:
        score, move = cal_score(score_matrix, seq1, seq2, i, j, match, mismatch, gap)
        score_matrix at (i, j) = score
        traceback_matrix at (i, j) = move

        IF score > max_score:
            max_score = score
            max_pos = (i, j)
            (using ">" keeps only the first best cell found if there is a tie)

print max_score

aligned_seq1, aligned_seq2 = traceback(seq1, seq2, traceback_matrix, max_pos)

Return aligned_seq1, aligned_seq2, score_matrix
```

# Results Output
### Test 1: TACTTAG vs CACATTAA (Example from slides)
```
Alignment score:  4
AC-TTA
ACATTA
[[0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 1 1 0 0]
 [0 0 1 0 1 0 0 2 1]
 [0 1 0 2 1 0 0 1 1]
 [0 0 0 1 1 2 1 0 0]
 [0 0 0 0 0 2 3 2 1]
 [0 0 1 0 1 1 2 4 3]
 [0 0 0 0 0 0 1 3 3]]
```

### Test 2: GGGGAAAAAAAAAAAACCCC vs GGGGAAAAAACCCC
```
Alignment score: 10
GGGGAAAAAA
GGGGAAAAAA
[[ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
 [ 0  1  1  1  1  0  0  0  0  0  0  0  0  0  0]
 [ 0  1  2  2  2  1  0  0  0  0  0  0  0  0  0]
 [ 0  1  2  3  3  2  1  0  0  0  0  0  0  0  0]
 [ 0  1  2  3  4  3  2  1  0  0  0  0  0  0  0]
 [ 0  0  1  2  3  5  4  3  2  1  1  0  0  0  0]
 [ 0  0  0  1  2  4  6  5  4  3  2  1  0  0  0]
 [ 0  0  0  0  1  3  5  7  6  5  4  3  2  1  0]
 [ 0  0  0  0  0  2  4  6  8  7  6  5  4  3  2]
 [ 0  0  0  0  0  1  3  5  7  9  8  7  6  5  4]
 [ 0  0  0  0  0  1  2  4  6  8 10  9  8  7  6]
 [ 0  0  0  0  0  1  2  3  5  7  9  9  8  7  6]
 [ 0  0  0  0  0  1  2  3  4  6  8  8  8  7  6]
 [ 0  0  0  0  0  1  2  3  4  5  7  7  7  7  6]
 [ 0  0  0  0  0  1  2  3  4  5  6  6  6  6  6]
 [ 0  0  0  0  0  1  2  3  4  5  6  5  5  5  5]
 [ 0  0  0  0  0  1  2  3  4  5  6  5  4  4  4]
 [ 0  0  0  0  0  0  1  2  3  4  5  7  6  5  5]
 [ 0  0  0  0  0  0  0  1  2  3  4  6  8  7  6]
 [ 0  0  0  0  0  0  0  0  1  2  3  5  7  9  8]
 [ 0  0  0  0  0  0  0  0  0  1  2  4  6  8 10]]
```

The printed matrix contains two cells with the best score of 10: one at row 10 / column 10, which traces back to `GGGGAAAAAA`, and one in the bottom-right corner, which would trace back to `AAAAAACCCC`.

# Successes
* We agreed upon pseudocode written by Ildiko, and each of us wrote code that varied in different functions. The two implementations produced identical alignments and scores on both notebook tests, which served as an informal cross-check on correctness. The final version uses Dianah's approach of tracking the highest score while the matrix fills, which avoided extra NumPy functions and made `smith_waterman()` simpler.
* Two implementations also handled the diagonal score differently. Dianah's `cal_score()` first stores the match or mismatch value in its own variable (`pair_score`) and then adds it to the up-left neighbor in a single line, while Ildiko's version does the addition separately inside each branch of the `if`/`else`. Both give the same result, and comparing them showed how the same pseudocode step can be written more than one way.
* Aamna created a different approach to `traceback()`: building each aligned sequence backward in a list and reversing it once at the end, instead of adding each letter to the front of a string as in Ildiko's and Dianah's versions. Both approaches put the letters in the correct order.
* The final output for Test 1 matches the expected output exactly, including the whole-number formatting of the scoring matrix.
* The scoring values are customizable, and the `cal_score()` test check uses non-default scoring (match +2, mismatch −1, gap −2) to confirm that custom values are applied correctly.

# Struggles
* The starter materials contained inconsistencies that had to be resolved by decision rather than followed as written. The `traceback()` docstring reverses the gap directions (an UP move puts the gap in seq2, not seq1), and the instructions ask for the alignment score to be printed even though the provided function skeletons have no place for it. Our code follows the correct gap directions, and the score print was added to `smith_waterman()`.
* Test 2 has no expected output and contains two cells tied for the best score. The program reports only the first one it finds, so a second, equally good alignment (`AAAAAACCCC`) goes unreported. Checking this result required reasoning through the printed matrix rather than comparing against a known answer.
* Keeping the shared branch up to date took coordination. Work that is saved or committed locally but never pushed does not appear in a pull request, so the repository did not always reflect everyone's latest work.  We are still improving our GitHub skills.
* All three functions (cal_score, traceback and smith_waterman) work together, and our output matches the expected output for the slide example (AC-TTA / ACATTA).
* Filling in the scoring matrix and tracing back by hand first made the pseudocode much easier to understand and turn into code.
* Meeting as a team to discuss and work through the pseudocode helped us understand each step.
* The scoring values (match, mismatch and gap) can be changed when calling the function, so the algorithm can be tested with different scoring strategies.
* Recording the arrows in a separate traceback matrix made the traceback function simple: it just follows the arrows back to the start.
* Reviewing each others code helped us understand why certain approaches worked and gave us a chance to discuss which implementations were easier to follow.

# Struggles
* At first, it was hard to turn the pseudocode into code. The variable names and indexes made it difficult to see what each line was doing until we worked an example by hand.
* Indexing was confusing at first: Python counts from 0, and the matrix has an extra border row and column, so matrix row i matches seq1[i-1].
* It took practice to remember that the match score only applies to the diagonal move, while up and left always use the gap penalty.
* Traceback was also a little confusing at first, especially understanding which sequence gets a gap when moving up or left and how the aligned sequences are built in the correct order.


# Reflection and Adaptive Learning
* Choosing the matrix type involved a trade-off. A whole-number matrix matches the expected output's formatting, but it silently truncates decimal gap penalties: with a gap of −0.5, it returns a score of 10 instead of the correct 11, with no error. We chose whole numbers to match the test cases, so the program assumes whole-number scoring values without handling the edge case we considered. A next step would be to keep the decimal matrix for scoring and convert it to whole numbers only for display when every value is whole, or to have the function warn the user if a decimal scoring value is passed in.
* Because the starter materials contained inconsistencies, we learned not to treat the provided docstrings and examples as automatically correct. Checking a function's description against a small example worked by hand, and against the expected output, is what showed which version was right. We plan to do this check at the start of future projects, before writing code.
* The tie in Test 2 showed that a single reported alignment is not always the whole answer. A next step would be to have `smith_waterman()` find every cell that holds the best score and trace back from each one, so all equally good alignments are reported.
* For keeping the shared branch current, we plan to confirm that a pull request shows the changed files before letting the group know it's ready, and to pull from the upstream branch at the start of each work session.

# Personal Reflections
## Group leader : Dianah Kasemire
This was an interesting activity. At first, the pseudocode was hard to follow, and I struggled to turn it into code. What helped most was filling in the scoring matrix by hand for two short sequences, one cell at a time. Once I had done that manually, the pseudocode made sense, and each line of code matched a step I had already done myself. Tracing back through the table by hand also made the traceback function much easier to write. Meeting up with my team to discuss and work through the pseudocode together also helped a lot. Talking through each step made the algorithm clearer, and I’d use both approaches again for future problems.

## Other member: Aamna Sheikh
I think the most interesting part of this project was understanding how the scoring matrix and traceback work together to find the best local alignment. The scoring calculations were fairly straightforward once I understood what each direction represented, but traceback took a little more thought, especially figuring out which sequence gets a gap and how to build the aligned sequences in the correct order. I found it helpful to look through my group members code alongside our pseudocode and work through how the different functions connected, rather than just focusing on each function individually.

## Other member: Aamna Sheikh
I think the most interesting part of this project was understanding how the scoring matrix and traceback work together to find the best local alignment. The scoring calculations were fairly straightforward once I understood what each direction represented, but traceback took a little more thought, especially figuring out which sequence gets a gap and how to build the aligned sequences in the correct order. I found it helpful to look through my group members code alongside our pseudocode and work through how the different functions connected, rather than just focusing on each function individually.

I also found our discussions comparing implementations really helpful. Even though we approached certain parts differently, we all were getting the same results, so it was really cool to look at why each approach worked and consider things like readability and how different scoring values would be handled. I think reviewing each other's code helped me understand the reasoning behind the final implementation rather than just focusing on whether the output was correct. Overall, I feel like I have a better understanding of how dynamic programming works in an alignment context, rather than just knowing what Smith-Waterman is supposed to do.

## Other member: Ildiko Polyak
Compared to graph algorithms, Smith-Waterman felt much easier to understand and code, since each cell of the matrix is just three additions and a max. My strategy has been to put most of my effort into understanding the algorithm first and then writing robust pseudocode, so that writing the real code (my biggest weakness) is easier translation. Where I struggled this week was not the algorithm itself but how the project split it across three functions, because the steps were not divided in the same order I had learned them. What helped was writing out a generic pseudocode for Smith-Waterman pairwise alignment first, in its natural order (set up, fill, find the best cell, trace back, output), and then assigning each step to the function it belonged in, which kept clear which steps needed to be written where and in what order. For the same reason, I added a simple print test after each function, running it on a small example I had already worked out by hand, so I could confirm each function worked on its own instead of waiting to troubleshoot the entire program at the end. Reflecting on that, I can still only process an algorithm in its proper order, and trying to separate it into pieces for a more "advanced" program leads to confusion for me. In the beginning of the semester, this stressed me out because I felt like I had to "master" each algorithm, but the pace of the class is fast and switches to a new world the next week.  Halfway throughout the semester, I'm now OK with understanding the algorithm at my level and continued use and consideration will fortify it.  I also need to spend more time learning how to work with numpy.

Even though the group's schedule had very little overlap for much collaborative work, we were able to meet for two short sessions and it was nice to reflect on our experience in the class together and not feel so alone in the fast pace and struggle to keep up with new difficult information every week.  It helped build confidence in the learning process without the need to master an outcome.

# Generative AI Appendix
Anthropic Claude Opus 5.5 and OpenAI ChatGPT were used for this project.
Anthropic Claude Opus 5.5 and ChatGPT was used for this project.

Ildiko - I am inexperienced with NumPy and used Claude to write the NumPy-specific code, since don't know those functions: creating the scoring and traceback matrices (`np.zeros()`, including `dtype=int` for the traceback matrix), finding the best score and its position (`np.max()`, `np.argmax()`, and `np.unravel_index()`), and building the small test matrix for the `traceback()` sanity check (`np.array()`). Claude also explained how each of these functions works before it was added to the code.  However, we did not end up using this part of code in the final project version because Dianah wrote a much simpler and cleaner version without those codes and it was nice to see two different ways of writing that portion.

Dianah- I used Claude to understand the algorithm. It explained how Smith-Waterman works and walked me through filling in the scoring matrix and doing the traceback by hand on a small example. I filled in the cells myself, and Claude checked my answers and explained my mistakes. I then started writing the pseudocode and used it to check my steps. I wrote most of the lines myself, and for a few parts I was stuck on, Claude showed me the line and explained what it did. I also used it to understand the git errors when pushing and merging our team’s work.

Aamna- I used ChatGPT throughout this project to help me understand both the biological purpose of sequence alignment and the Smith-Waterman algorithm itself. I understood what we needed to do for the assignment, but I didn't fully understand why we were doing it or what the results meant biologically. I always find it easier to approach coding problems when I understand the reasoning behind them, so a big part of my AI use was asking questions about the biology. I also used ChatGPT to help explain parts of my implementation too, particularly the traceback function, and to compare sections of our group members different approaches to the same ideas. I also created a pull request that somehow did not update my work on the PR branch and used it to understand what I did wrong. (I think I just did not save my file before pushing it. AI was not very helpful for this particular task).
Aamna- I used ChatGPT throughout this project to help me understand both the biological purpose of sequence alignment and the Smith-Waterman algorithm itself. I understood what we needed to do for the assignment, but I didn't fully understand why we were doing it or what the results meant biologically. I always find it easier to approach coding problems when I understand the reasoning behind them, so a big part of my AI use was asking questions about the biology. I also used ChatGPT to help explain parts of my implementation too, particularly the traceback function, and to compare sections of our group members different approaches to the same ideas. I also created a pull request that somehow did not update my work on the PR branch and used it to understand what I did wrong. (I think I just did not save my file before pushing it. AI was not very helpful for this particular task).
