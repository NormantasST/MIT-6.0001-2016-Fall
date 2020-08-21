# Problem Set 4C
# Name: Normantas Stankevicius
# Collaborators: MIT6_0001F16_Pset4.pdf
# Time Spent: 0:55

import string
from ps4a import get_permutations
import copy

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.message_text = text
        
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return copy.deepcopy(self.valid_words)
    
    @staticmethod
    def build_unciphered_dict():
        """Builds an unciphered dictionary
        so a->a, b->b, z->z, A->A, B->B, Z->Z..."""
        alphabet = string.ascii_lowercase
        unciphered_dict = {}
        for letter in alphabet:
            unciphered_dict[letter] = letter
            unciphered_dict[letter.upper()] = letter.upper()
        return unciphered_dict
            
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        #VOWELS: 'aeiou'
        assert len(vowels_permutation) == len(VOWELS_LOWER), "The amount of vowels is invalid"
        vowels_permutation = vowels_permutation.lower()
        transpose_dict = SubMessage.build_unciphered_dict() #Builds an enpty dict so I don't need to add constanants
        for vowel_index in range(len(vowels_permutation)):
            letter = vowels_permutation[vowel_index]
            transpose_dict[VOWELS_LOWER[vowel_index]] = letter
            transpose_dict[VOWELS_UPPER[vowel_index]] = letter.upper()
        
        return transpose_dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        transpose_text = ""
        for letter in self.message_text:
            if letter.isalpha():
                transpose_text += transpose_dict[letter]
            else:
                transpose_text += letter
                
        return transpose_text
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)
        
    def get_score_of_valid_words(self, text):
        """Returns a score of valid words.
        1 valid word => +1 to score"""
        all_words_in_text = text.split(' ')
        score = 0
        for word in all_words_in_text:
            if is_word(self.get_valid_words(), word):
                score += 1
   
        return score
    
    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        permutations = get_permutations(VOWELS_LOWER)
        best_decrypted_message = "Message hasn't been decrypted"
        best_decrypted_message_score = 0
        message = SubMessage(self.get_message_text())
        for permutation in permutations:
            enc_dict = message.build_transpose_dict(permutation)
            decrypted_text = message.apply_transpose(enc_dict)
            current_score = self.get_score_of_valid_words(decrypted_text)

            if current_score > best_decrypted_message_score:
                best_decrypted_message_score = current_score
                best_decrypted_message = decrypted_text
    
        return best_decrypted_message

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    
    #
    #--------------------------------------------------------
    #
    
    message = SubMessage("The quick brown fox jumps over the lazy dog")
    permutation = "aeiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "The qoick bruwn fux jomps uver the lazy dug")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    
    #
    #-------------------------------------------------------------------
    #
    
    message = SubMessage("Hello World!")
    permutation = "aeiou"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hello World!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    
    #Deduction, code could be way quicker if the word list wasn't being copied
    #memory could be saved if word list was a global or class variable