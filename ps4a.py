# Problem Set 4A
# Name: Steven DeNero
# Collaborators:
# Time Spent: x:xx

def remove_duplicate_permutations(sequence):
    """
    This function removes duplicate permutations from your sequence.

    First it determines the total count of each permutation using a dictionary and the "get." method, looping over the full initial sequence

    Then, rather than deleting n-1 permutations, it populates a new list by looping over dictionary keys. These will all be unique, so you dont need to know how many there are. 'n' doesnt matter.

    This function does not touch the original 'sequence' list. It returns a copy.

    Returns : a list of unique permutations

    Example:
    >> remove_duplicate_permutations('abba','abba','bbaa','bbaa')
    ['abba','bbaa]

    """
    frequencies = {} #make new, empty dictionary
    sequence_copy = [] #make new, empty list

    for permutation in sequence:
        frequencies[permutation] = frequencies.get(permutation,0) + 1

    for key in frequencies.keys():
        sequence_copy.append(key)
        #You have to use the append method when you're populating a list index which doesnt exist.
        #This is not like Fortran, which makes an array of (*) length, and you can just index to it immediately.
        #After you use append, you can overwrite that index

    return sequence_copy

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

    permutation_list = []
    if len(sequence) <= 1:
        return [sequence]  #Return a sequence of 1 character or less.
    else:
        for element_of_sequence in get_permutations(sequence[1:]): #cut off the beginning, reducing your total sequence by 1 each time.
            for i in range(len(sequence)):
                permutation_list.append(element_of_sequence[:i]+sequence[0]+element_of_sequence[i:])

        return remove_duplicate_permutations(permutation_list)

'''
Example. Start with abc as your sequence.

sequence = 'abc'
if len(abc) <=1 false
for 'a' in 'bc'
sequence = 'bc'
if len(bc) <= 1 false 
for 'b' in 'c'
sequence = c
if len(c) <= 1 true
return c
for c in 'bc'
       (element_of_sequence = c)
       (sequence = 'bc')
for i in range 0:2. i = 0
element_of_sequence[:i] --> element_of_sequence[:0] = ''
sequence[0] --> sequence[0]                         = 'b'
element_of_sequence[i:] --> element_of_sequence[0:] = 'c' --> 'bc'
for i in range 0:2. i = 1
element_of_sequence[:i] --> element_of_sequence[:1] = 'c'
sequence[0] --> sequence[0]                         = 'b'
element_of_sequence[i:] --> element_of_sequence[1:] = '' --> 'cb'

for 'bc' in 'abc'
       (element_of_sequence = bc)
       (sequence = 'abc')
for i in range 0:3. i = 0
element_of_sequence[:i] --> element_of_sequence[:0] = ''
sequence[0] --> sequence[0]                         = 'a'
element_of_sequence[i:] --> element_of_sequence[0:] = 'bc' --> 'abc'

for i in range 0:3. i = 1
element_of_sequence[:i] --> element_of_sequence[:1] = 'b'
sequence[0] --> sequence[0]                         = 'a'
element_of_sequence[i:] --> element_of_sequence[1:] = 'c' --> 'bac'

for i in range 0:3. i = 2
element_of_sequence[:i] --> element_of_sequence[:1] = 'bc'
sequence[0] --> sequence[0]                         = 'a'
element_of_sequence[i:] --> element_of_sequence[1:] = '' --> 'bca'

for 'cb' in 'abc'
       (element_of_sequence = cb)
       (sequence = 'abc')
for i in range 0:3. i = 0
element_of_sequence[:i] --> element_of_sequence[:0] = ''
sequence[0] --> sequence[0]                         = 'a'
element_of_sequence[i:] --> element_of_sequence[0:] = 'cb' --> 'acb'

for i in range 0:3. i = 1
element_of_sequence[:i] --> element_of_sequence[:1] = 'c'
sequence[0] --> sequence[0]                         = 'a'
element_of_sequence[i:] --> element_of_sequence[1:] = 'b' --> 'cab'

for i in range 0:3. i = 2
element_of_sequence[:i] --> element_of_sequence[:1] = 'cb'
sequence[0] --> sequence[0]                         = 'a'
element_of_sequence[i:] --> element_of_sequence[1:] = '' --> 'cba'
'''


if __name__ == '__main__':
   #EXAMPLE
    print('Example * * * * * * * * * * * * * *')
    example_input = 'ab'
    print('Input:', example_input)
    print('Expected Output:', ['ab','ba'])
    print('Actual Output:', get_permutations(example_input))

    print()
    print('Next Example * * * * * * * * * * * ')
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))

    print()
    print('Next Example * * * * * * * * * * * ')
    example_input = 'bbaa'
    print('Input:', example_input)
    print('Expected Output:', ['bbaa', 'baba', 'baab', 'abba', 'abab', 'aabb'])
    print('Actual Output:', get_permutations(example_input))

