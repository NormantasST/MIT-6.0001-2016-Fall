# Problem Set 4A
# Name: Normatas
# Collaborators: Research how permutations work
# Time Spent: 0:45 

def add_letter_to_start_of_item_in_list(letter, sequence):
    """adds a letter to a  start of a item in a list
    example:
    letter:a, sequence: ['bc', 'cb'] => a + bc, a + cb
    returns ['abc','acb']
    """
    output = []
    for item in sequence:
        output.append(letter + item)
    
    return output

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''    
    if len(sequence) <= 1:
        return sequence
    
    possible_permutations = []
    for letter in sequence:
        letter_list = list(sequence) #Creates a mutable list
        letter_list.remove(letter) #removes this letter as it can be reused
        smaller_possible_permutatios = get_permutations(letter_list) #Gets other possible permutations excluding current letter
        possible_permutations.extend(add_letter_to_start_of_item_in_list(letter, smaller_possible_permutatios)) #adds to a possible list of permutations
    
    return possible_permutations
    
if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
    example_input = 'bc'
    print('Input:', example_input)
    print('Expected Output:', ['bc', 'cb'])
    print('Actual Output:', get_permutations(example_input))
    
    example_input = '1234'
    print('Input:', example_input)
    print('Expected Output:', ['1234', '1243', '1324', '1342', '1423', '1432', '2134', '2143', '2314', '2341', '2413', '2431', '3124', '3142', '3214', '3241', '3412', '3421', '4123', '4132', '4213', '4231', '4312', '4321'])
    print('Actual Output:', get_permutations(example_input)) 