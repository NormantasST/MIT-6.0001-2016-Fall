# Problem Set 2, hangman.py
# Name: Normantas Stankeviciuis
# Collaborators: python 3 documentation websites
# Time spent: 5-7h~ including thinking and other things.

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for i in secret_word:
        if i not in letters_guessed:
            return False #letter doesn't exist in guessed words
        
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    output = ""
    for i in secret_word:
        if i in letters_guessed:
            output += i
        else:
            output += "_ "
    return output



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = list(string.ascii_lowercase) #gets a list of all english alphabet letters
    output = sorted(list(set(alphabet) - set(letters_guessed)))
    return "".join(output) #transforms list to a string
   
def print_dashes():
    print("-------------")

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    guesses_left, warnings_left, letters_guessed = initialize_hangman()
    #For testing uncomment:
    #print("!!!!FOR TESTING!!! SECRET WORD IS:",secret_word)
    while(True):
        
        availabe_letters = print_and_get_information_at_start_of_round(guesses_left, letters_guessed)      
        
        #Asks for a letter till it gets a possible letter
        guessed_letter = input("Please guess a letter: ").lower()
        
        if (guessed_letter not in availabe_letters):
            guesses_left, warnings_left = give_out_warning_information(warnings_left, guesses_left, secret_word, letters_guessed, guessed_letter)
            if (guesses_left <= 0):
                #The game has been lost due to warnings
                print_losing_message(secret_word)
                break
            continue
            
        #Updates the guessed word and letters
        letters_guessed.append(guessed_letter)
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        
        #Tells the user how well he did on current round, returns the amount of guesses left
        guesses_left = checks_how_well_the_round_went(guesses_left, guessed_letter, secret_word, guessed_word)

        #Ends Game  
        if (check_if_game_continues(guesses_left, guessed_word, secret_word)):
            break
            
        print_dashes()
        



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------
def initialize_hangman():
    guesses_left = 6
    warnings_left = 3
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {} letters long.".format(len(secret_word)))
    print("You have {} warnings left".format(warnings_left))
    print_dashes()
    return (guesses_left, warnings_left, letters_guessed)

def print_losing_message(secret_word):
    """Prints a message when the game is lost"""
    print_dashes()
    print("Sorry, you ran out of guesses. The word was {}.".format(secret_word))
    
def print_winner_message(guesses_left, secret_word):
    """Prints a message when the user won the game"""
    print_dashes()
    print("Congratulations, you won!")
    print("Your total score for this game is: {}".format(guesses_left * len(set(list(secret_word)))))
    
def give_out_warning_information(warnings_left, guesses_left, secret_word, letters_guessed, guessed_letter):
    """Tells the reason why the guess was wrong
    punishes the user"""
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    reason = ""
    if guessed_letter in letters_guessed:
        reason = "You've already guessed that letter"
    else:
        reason = "That is not a valid letter"
    
    if warnings_left > 0:
        warnings_left -= 1;
        print("Oops! {}. You have {} warnings left: {}".format(reason, warnings_left, guessed_word))
    else:
        guesses_left -= 1
        print(" Oops! {}. You have no warnings left so you lose one guess: {}".format(reason, guessed_word))
    return (guesses_left, warnings_left)

def print_and_get_information_at_start_of_round(guesses_left, letters_guessed):
    """Prints the information at the start of the round,
    returns the avaialble letters"""
    print("You have {} guesses left".format(guesses_left))
    availabe_letters = get_available_letters(letters_guessed)
    print("Available letters: {}".format(availabe_letters))
    return availabe_letters
        
def checks_how_well_the_round_went(guesses_left, guessed_letter, secret_word, guessed_word):
    """Tells the user how well he did on this round
    returns the amount of guesses left"""
    vowels = ['a','e','i','o','u']
    if guessed_letter in list(secret_word):
            print("Good Guess: {}".format(guessed_word))
    else:
        print("Oops! That letter is not in my word: {}".format(guessed_word))
        if guessed_letter in vowels:
            guesses_left -= 2
        else:
            guesses_left -= 1
            
    return guesses_left
                
def check_if_game_continues(guesses_left, guessed_word, secret_word):
    """Checks if the guesses word is correct or there aren't
    any more guesses left"""
    if guesses_left <= 0:
        print_losing_message(secret_word)
        return True
    if guessed_word == secret_word:
        print_winner_message(guesses_left, secret_word)
        return True
    return False

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(" ", "")
    if len(my_word) == len(other_word):
        for i in range(len(my_word)):
            letter = my_word[i]
            if letter == "_":
                continue
            elif letter != other_word[i]:
                return False      
        #All checks were correct, plausible word
        return True
    else:
        return False

def get_possible_matches_list(my_word):
    """my word = currently possible guessable word
    Get's every possible word from wordlist
    implement TRIE for speed if needed"""
    output = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            output.append(word)
            
    return output
    
def print_possible_matches_from_list(possible_matches):
    """Prints possible matches from the list for getting
    all possible matches from a wordlist when playing
    hangman with hints"""
    if(any(possible_matches)):
        print("Possible word matches are: ")
        print(" ".join(possible_matches))
    else:
        print("No matches found")
    
def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    possible_matches_list = get_possible_matches_list(my_word)
    print_possible_matches_from_list(possible_matches_list)
    print_dashes()
    

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_left, warnings_left, letters_guessed = initialize_hangman()
    #For testing uncomment:
    #print("!!!!FOR TESTING!!! SECRET WORD IS:",secret_word)
    while(True):
        
        availabe_letters = print_and_get_information_at_start_of_round(guesses_left, letters_guessed)      
        
        #Asks for a letter till it gets a possible letter
        guessed_letter = input("Please guess a letter: ").lower()
        if guessed_letter == "*":
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue
        elif guessed_letter not in availabe_letters:
            guesses_left, warnings_left = give_out_warning_information(warnings_left, guesses_left, secret_word, letters_guessed, guessed_letter)
            if (guesses_left <= 0):
                #The game has been lost due to warnings
                print_losing_message(secret_word)
                break
            continue
            
        #Updates the guessed word and letters
        letters_guessed.append(guessed_letter)
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        
        #Tells the user how well he did on current round, returns the amount of guesses left
        guesses_left = checks_how_well_the_round_went(guesses_left, guessed_letter, secret_word, guessed_word)

        #Ends Game  
        if (check_if_game_continues(guesses_left, guessed_word, secret_word)):
            break
            
        print_dashes()



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
