# Introduction
This project implements a Markov chain to process sentences.
The project starts with a simple first-order model, where the next word depends only on the current word. 
It then extends this idea to an Nth-order model, where the next word depends on the previous N words. 
This is similar to how Markov chain models can be used in bioinformatics, 
such as identifying coding regions in a genome by using higher-order models to capture patterns between codon triplets.

# Pseudocode
FUNCTION build_markov_model(markov_model, new_text):
    SPLIT new_text into a list of words
    ADD '*S*' to the front of the list (marks start)
    ADD '*E*' to the end of the list (marks end)
    FOR each position i from 1 to end of the padded list:
        state = the word just before position i
        next_word = the word at position i
            IF state has not been seen before:
            CREATE an empty tally sheet for state
        INCREMENT the count of next_word on state's tally sheet
        (starting from 0 if it's the first time seeing this next_word)
    RETURN the completed markov_model

Test  code
CREATE an empty markov_model
SET text = "one fish two fish red fish blue fish"
CALL build_markov_model(markov_model, text) and store the result back in markov_model
PRINT markov_model

Nth order Markov chain:
FUNCTION build_markov_model(markov_model, text, order):
    IF markov_model is empty/not given:
        CREATE an empty markov_model
    SPLIT text into a list of words
    ADD 'order' copies of '*S*' to the front of the list (marks start)
    ADD '*E*' to the end of the list (marks end)
    FOR each position i from 'order' to end of the padded list:
        IF order equals 1:
            state = the single word just before position i
        ELSE:
            state = the tuple of the last 'order' words before position i
        next_word = the word at position i
        IF state has not been seen before:
            CREATE an empty tally sheet for state
        INCREMENT the count of next_word on state's tally sheet
        (starting from 0 if it's the first time seeing this next_word)
    RETURN the completed markov_model

Test code
CREATE an empty markov_model
SET text = "one fish two fish red fish blue red fish blue"
CALL build_markov_model(markov_model, text, order=2) and store the result back in markov_model
DISPLAY markov_model

FUNCTION get_next_word(current_word, markov_model, seed)
	Set random seed based on seed provided
Values dictionary of potential next words (keys) and their counts (values) associated with the current word
Get list of next words by extracting the keys as a list
Get list of their counts by extracting the values
Add up the total counts of possible next words
Calculate a list of probabilities of each next word as (their counts) /(total counts)
Use np.random.choice to choose a next word based on its associated probability
Return the word 

FUNCTION generate_random_text(markov_model, seed)
	Check what order the markov model is
		If it is not first order, set the current (start) state to *S* x order
		If first order set to *S*
	Create a list of words to add to
	While the the end character (*E*) hasn’t been set to the next word
		Call the next word function with the current state, model, and seed
		If the next word is the end character end the loop
		If else, add the next word to the list 
		Increment the current state to the next word or tuple of words
Return a joined list of words


# Successes
Successfully implemented a first order Markov model that matched the expected output.
Successfully Got the Nth-order version working by using word-pairs as dictionary keys instead of single words. 
Traced a test sentence by hand and compared it to my code's output. They matched exactly, including repeated pairs and 
pairs that led to different next-words at different points.
Got the full generation pipeline working end-to-end on the toy Dr. Seuss example, producing valid generated sentences.
We worked together well and got some of the code working. 
We overcame many challenges with GitHub and getting set up after one of us joined late to get a product turned in that is ready for improvement by peer review.


# Struggles

Dianah: One of my group members dropped the class just as we were about to start the project, so I had to begin working on the project alone. 
Thankfully, Matthew later joined the group, although he was still learning how the class and project worked.
Since I had never used Jupyter notebooks before, so the initial setup was challenging. It became easier once I learned how to use Jupyter directly in PyCharm.
After merging Matthew’s pull request on GitHub, the notebook became jumbled when I pulled the changes to my computer. I fixed this by downloading a fresh copy from GitHub.

Matthew: I struggled with GitHub/VS code interface and ended up having to download the relevant files locally from canvas and GitHub, modify them, and then upload them back through the GitHub website. 
I could not successfully pull Dianah’s branch into my own vs code environment. I could see the files, but they weren’t editable. 
I had to copy the raw Jupyter Notebook text from my local file to push to GitHub. 
I also struggled to catch up after starting the class late, and had to learn about the model, GitHub, Jupyter Notebooks, and refresh my python all at the same time. 
The code doesn’t seem to work as intended after "Generate Text for Markov Model" as it loops endlessly. This seems to have something to do with the seeds used. 
When seeds are removed the code seems to work.

# Personal reflections
## Group Leader
Dianah: Working on the project alone at the beginning was challenging, but it helped me understand the project better. 
Once Matthew joined, we were able to work through some of the problems together, including the indentation errors and the infinite loop. 
This experience taught me to be flexible and patient when working through unexpected changes in a group.

## Other member
Matthew: After joining the class late, I thought this project went smoothly. Dianah had most of the code done, and it was great review to look at her work. 
I also was able to make address some bugs which I think improved functionality. 
Additionally, we worked well as a team and Dianah also helped me get up to speed on other elements of the class.

# Generative AI Appendix
Claude (Anthropic), Version 2.110.0, Sonnet 5, was used to assist in debugging the "Generate Text from Markov Model" chunk of code. 
We realized the code didn't seem to work as intended after "Generate Text for Markov Model", and it looped endlessly. 
This seemed to have something to do with the seeds being used, since get_next_word resets the random seed to the same fixed value on every call, meaning revisiting the same word or 
state later in a sentence always produced the exact same "random" output as before on repetitive text.
This created a cycle that never reached the end marker, causing the loop to run forever.
When seeds were removed from being reset on every call, the code worked as intended.