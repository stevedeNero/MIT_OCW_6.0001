# Problem Set 4C
# Name: Steven DeNero
# Collaborators:
# Started 10/28/2020
# Finished 12/4/2020 (had to learn how to use an IDE to link files)

import string
from PS4A import get_permutations

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

# permutated_string = 'eioua'
# for i, letter in enumerate(permutated_string):
#     print(i, letter)


class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object

        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

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
        return self.valid_words.copy()

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
        #self.vowels_permutation = vowels_permutation

        '''
        General Idea
        "a" is always the first letter. so whichever is first in the vowels_permutation should be the new "a"
        "str.upper()" can translate to upper-case the vowels_permutation, so you can map to Upper that way.

        VOWELS_LOWER = 'aeiou'
        VOWELS_UPPER = 'AEIOU'
        CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
        CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'
        '''
        punc = list(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
        dict = {}  # create an empty dictionary. Mapping letters to letters.

        for i, letter in enumerate(
                vowels_permutation.lower()):  # using "lower()" and "upper()" here ensures that the correct case is used, regardless of how it is passed in.
            dict[VOWELS_LOWER[i]] = letter

        for i, letter in enumerate(
                vowels_permutation.upper()):  # using "lower()" and "upper()" here ensures that the correct case is used, regardless of how it is passed in.
            dict[VOWELS_UPPER[i]] = letter

        for letter in CONSONANTS_LOWER:
            dict[letter] = letter

        for letter in CONSONANTS_UPPER:
            dict[letter] = letter

        for mark in punc:
            dict[mark] = mark

        return dict

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary

        Returns: an encrypted version of the message text, based
        on the dictionary

        '''

        encrypted_message = ""

        for letter in self.message_text:

            encrypted_message += transpose_dict[letter]

        return encrypted_message


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

        max_valid_words = 0
        for i, permutation in enumerate(get_permutations(VOWELS_LOWER)): # Get all possible permutations of the list of vowels
            num_valid_words = 0
            dictionary = self.build_transpose_dict(permutation)
            new_message_text = self.apply_transpose(dictionary)
            for word in new_message_text.split():
                if is_word(self.valid_words, word):  # this function actually removes punctuation, so you dont have to worry about that.
                    num_valid_words += 1
            if num_valid_words > max_valid_words:
                max_valid_words = num_valid_words
                best_effort_decrypt = new_message_text

        if max_valid_words > 0:
            return best_effort_decrypt
        else:
            return self.message_text


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

    # TODO: WRITE YOUR TEST CASES HERE
