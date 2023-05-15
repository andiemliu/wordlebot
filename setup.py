import pickle

with open('raw_data/possible_words.txt') as file:
    possible_words = [line.rstrip() for line in file]
with open('raw_data/allowed_guesses.txt') as file:
    allowed_guesses = [line.rstrip() for line in file]

with open('processed_data/possible_words_lst.pkl', 'wb') as f:
    pickle.dump(possible_words, f)
with open('processed_data/allowed_guesses_lst.pkl', 'wb') as f:
    pickle.dump(allowed_guesses, f)
"""
Define a pattern to be information about each letter's presence in the secret word: 
green = 2, yellow = 1, grey = 0.
"""
def compute_pattern(guess, answer):
    # Returns a length 5 tuple
    
    pattern = [0, 0, 0, 0, 0]
    taken = [False, False, False, False, False]
    
    # Green pass
    for i in range(5):
        if guess[i] == answer[i]:
            # If it's an exact match, color it green, and mark it as taken
            # so that the yellow pass doesn't match to it again
            pattern[i] = 2
            taken[i] = True
    
    # Yellow pass
    for i in range(5):
        if pattern[i] == 2:
            # If a spot is already colored green, we skip it
            continue
        query = guess[i]
        for j in range(5):
            if query == answer[j] and taken[j] is False:
                # If there is a misplaced match that is not taken by the
                # green pass or a previous yellow pass, we color it yellow
                # and mark it as taken
                pattern[i] = 1
                taken[j] = True
                break
    
    return tuple(pattern)

pattern_table = {}

for guess in allowed_guesses:
    word_table = {}
    for answer in possible_words:
        word_table[answer] = compute_pattern(guess, answer)
    pattern_table[guess] = word_table

with open('processed_data/pattern_table.pkl', 'wb') as f:
    pickle.dump(pattern_table, f)
