import pickle
import random
import math
import os

with open('processed_data/possible_words_lst.pkl', 'rb') as f:
    possible_words = pickle.load(f)
with open('processed_data/allowed_guesses_lst.pkl', 'rb') as f:
    allowed_guesses = pickle.load(f)
with open('processed_data/pattern_table.pkl', 'rb') as f:
    pattern_table = pickle.load(f)

"""
divide_alphabet: splits current alphabet into smaller subgroups. 
    input: a guess, the current alphabet. 
    output: a dictionary that maps from the set of possible color patterns to the set of secret words 
    such that pattern_table[guess][secret_word] is that color pattern. 
    ex: guess = "shake", alphabet = {shape, shake, shame}
        divide_alphabet() = (2,2,2,2,2) → {shake}, (2,2,2,0,2) → {shape, shame}.
"""
def divide_alphabet(guess, alphabet):
    pattern_to_subgroup = {pattern_table[guess][word]: [] for word in alphabet}
    for word in alphabet:
        pattern_to_subgroup[pattern_table[guess][word]].append(word)
    return pattern_to_subgroup

"""
computes uniform probability distribution over patterns
pattern_groups = (2,2,2,2,2) → {shake}, (2,2,2,0,2) → {shape, shame}
prob_dist() = [0.333, 0.666]
"""
def prob_dist(pattern_groups):
    # returns a probability distribution in the form of a list
    # for example, if the probability distribution is
    # P(pattern_1) = 0.2, P(pattern_2) = 0.3, P(pattern_3) = 0.5,
    # this function should return [0.2, 0.3, 0.5]. Order doesn't matter
    dist = []
    total_words = 0
    for v in pattern_groups.values():
        total_words += len(v)
    dist = [len(x)/total_words for x in pattern_groups.values()] 
    return dist

#Takes in probability distribution in list format and outputs its entropy
def entropy(dist):
    h = 0
    for p in dist:
        h += p * math.log2(p)
    return -1 * h

#Finds best guess that maximizes entropy of Ytk
def find_best_guess(alphabet, allowed_guesses):
    word, highest = None, 0
    for guess in allowed_guesses:
        dist = prob_dist(divide_alphabet(guess, alphabet))
        curr_entropy = entropy(dist) #Ytk = pattern for guess 
        if curr_entropy > highest:
            word = guess
            highest = curr_entropy
    return word

"""
Strategies:
    Always open with 'soare'.
    Limit guesses to alphabet if small.
"""
def find_best_guess_optimized(alphabet):
    if len(alphabet) == 2315:
        # if it's the opening guess, we directly output 'soare'
        return 'soare'
    elif len(alphabet) == 1:
        # if we are certain what the secret word is, directly guess it
        return alphabet[0]
    elif len(alphabet) <= 3:
        # if the alphabet is small, limit our guess to within the alphabet
        return find_best_guess(alphabet, alphabet)
    else:
        # otherwise, we apply no optimization
        return find_best_guess(alphabet, allowed_guesses)
    
#For statistical testing
def create_wordle_game(true_answer):
    def wordle_game(guess):
        # takes in a guess and outputs the pattern
        return pattern_table[guess][true_answer]
    return wordle_game
def play_wordle(wordle_game, print_guesses=False):
    alphabet = possible_words
    num_guesses = 0
    while True:
        num_guesses += 1
        guess = find_best_guess_optimized(alphabet)
        color_pattern = wordle_game(guess)
        if print_guesses:
            print(f'Guess {num_guesses}: {guess}  |  Pattern: {color_pattern}')
        if color_pattern == (2, 2, 2, 2, 2):
            # correct answer!
            break
        # find the true pattern observed, and then update alphabet
        alphabet = divide_alphabet(guess, alphabet)[color_pattern]

    return num_guesses