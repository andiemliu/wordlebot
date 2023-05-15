import tools
class WordleBot:
    def __init__(self):
        # initialize for a new game
        self.alphabet = tools.possible_words
        self.suggest()
    
    def suggest(self):
        # when called, the bot gives you the best word to guess
        suggested_guess = tools.find_best_guess_optimized(self.alphabet)
        print('Next word to guess:', suggested_guess)
    
    def observe(self, word, pattern):
        # after a guess, feed the pattern to the bot to update
        # then, the bot suggests a word to guess
        assert len(word) == len(pattern) == 5
        # update self.alphabet according to the observation,
        # then call self.suggest()
        self.alphabet = tools.divide_alphabet(word, self.alphabet)[pattern]
        self.suggest()
        self.print_alphabet()
    
    def print_alphabet(self):
        print(f"{len(self.alphabet)} words possible: {self.alphabet}")
    
    def restart(self):
        # re-initialize the bot for a new game
        self.alphabet = tools.possible_words
        return