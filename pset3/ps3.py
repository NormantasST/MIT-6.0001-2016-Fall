# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Normantas Stankevicius
# Collaborators : none
# Time spent    : 7h

import math
import random
import copy

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*':0,'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

def get_word_score_first_component(word):
    
    """function is needed to calculate score,
    Get's the first component-value
    of score for the inserted word"""
    output = 0
    for letter in word:
        output += SCRABBLE_LETTER_VALUES[letter]
        
    return output

def get_word_score_second_component(word, n):
    
    """function is needed to calculate score,
    Get's the second component-value
    of score for the inserted word"""
    value = 7 * len(word) - 3*(n - len(word))
    
    return value if value > 1 else 1

def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played
            
	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    assert n >= 0, "The hand registered to have {} letters which resulted in an error".Format(n)
    assert type(word) == str, "\"{}\" was imputed as not a string".format(word)
    word = word.lower()
    first_component = get_word_score_first_component(word)
    second_component = get_word_score_second_component(word, n)
    return first_component * second_component

def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    hand["*"] = hand.get("*",0) + 1
    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(original_hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    hand = copy.deepcopy(original_hand) #deepcopies the original dict. hand so it doesn't mutate the original
    word = word.lower()
    
    #Updates hand to unclean hand
    for letter in word:
        if letter in hand:
            hand[letter] -= 1 
            
    #cleans the hand
    for key in list(hand.keys()):
        if hand[key] <= 0:
            hand.pop(key)
            
    return hand
         
def check_if_word_is_possible_with_current_hand(word, original_hand):
    
    hand = copy.deepcopy(original_hand) #keeps the original unaffected
    for letter in word:
        if letter not in hand or hand[letter] == 0:
            return False #Word is impossible with current hand
        else:
            hand[letter] -= 1 #Removes 1 letter use from the current hand copy
        
    return True
      
def check_for_possible_word_with_wildcard(word, word_list):
    """Validates the word when a wildcard was used"""
    for letter in VOWELS:
        temp_string = word.replace('*', letter)
        if temp_string in word_list:
            return True #Found a possible string
        
    return False #No possible string was found
             
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    
    assert type(word) is str, "\"{}\" Wasn't imputed as a string"
    word = word.lower()
    
    #checks if the word is in the word list, includes wildcards
    if '*' in word:
        if check_for_possible_word_with_wildcard(word, word_list) == False:
            return False
    elif word not in word_list:
        return False
    
    #checks if the word was possible to make
    if check_if_word_is_possible_with_current_hand(word, hand) == False:
        return False
    
    return True #Word is possible.

def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    output = 0
    for key in hand:
        output += hand[key]
    
    return output
        
def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    total_score = 0    
    while hand:
        display_hand(hand)
        word = input("Enter word, or \"!!\" to indicate that you are finished: ")            
        
        if  word == "!!":
            break
        else:
            if is_valid_word(word, hand, word_list):
                gained_score = get_word_score(word, calculate_handlen(hand))
                total_score += gained_score
                print("\"{}\" earned {} points. Total: {} points".format(word, gained_score, total_score))
            else:
                 print("That is not a valid word. Please choose another word . ") 
                
            hand = update_hand(hand, word)
            
    if not hand:
        print("Ran out of letters. ", end = '')
    print("Total score: {} points".format(total_score))

    return total_score

def the_hand_doesnt_contain_whole_alphabet(hand):
    """
    LEGACY FUNCTION!!!
    
    Checks if it's possible to substitute the hand
    Accounts there is at least one letter in keys.
    if key counter is n (possible letter count)
    
    if len(keys) < n, that meants there is at least 1 letter possible
    
    if len(keys) == n then checks if one of the letters is '*',
    if TRUE, that means there is one letter still available """
    
    n = len(VOWELS+CONSONANTS)
    keys = list(hand.keys())
    if len(keys) < n or (len(keys) == n and '*' in keys):
        return True
    else:
        return False
    
def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    output = copy.deepcopy(hand)
    usable_alphabet = VOWELS + CONSONANTS
    if letter in hand:
        while len(usable_alphabet) > 0:
            new_letter = random.choice(usable_alphabet)
            if new_letter not in hand: #If the new letter is not a duplicate
                output[new_letter] = hand[letter] #adds new letter
                output.pop(letter) #removes old letter
                break
            else: #removes letters that have appeared, ensures that the loop doesn't last for ever.
                temp_string_list = list(usable_alphabet)
                temp_string_list.remove(new_letter)
                usable_alphabet = "".join(temp_string_list)
            
    return output
    
def print_dashes():
    """Prints dashes"""
    print("----------")
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    number_of_hands = int(input("Enter total number of hands: "))
    total_score = 0
    can_substitute_hand = True
    can_replay_hand = True
    
    #Game Loop
    for i in range(number_of_hands):
        hand = deal_hand(HAND_SIZE) #Current hand
        
        if can_substitute_hand: #If hand can be substituted
            display_hand(hand)
            substitute_hand_input = input("Would you like to substitute a letter? ")
            if substitute_hand_input.lower() == "yes": #Hand has been substituted
                can_substitute_hand = False
                letter = input("Which letter would you like to replace: ")
                hand = substitute_hand(hand, letter)
        
        #Starts the current Round        
        round_score = play_hand(hand, word_list)
        print_dashes()
        
        if can_replay_hand: #Checks if can and if the player wants to replay a round
            replay_hand_input = input("Would you like to replay the hand? ")
            if replay_hand_input.lower() == "yes":
                can_replay_hand = False
                replay_hand_score = play_hand(hand, word_list)
                if replay_hand_score > round_score: #Picks the biggest score out of the 2 rounds with same hand
                    round_score = replay_hand_score
                    
                    
        total_score += round_score #Updates total score and moves to next round
    
    #
    #Game Loop has ended
    #
    print_dashes()
    print("Total score over all hands: {}".format(total_score))

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
