# Problem Set 4B
# Name: Steven DeNero
# Collaborators:
# Started 10/26/2020
# Finished 10/28/2020

import string


# print(string.ascii_lowercase)
# j = 1
# dict = {}
# for i in string.ascii_letters:
#     dict[i] = j
#     j += 1
#     if j > 26:
#         j -= 26
#
# print(dict)
# print(string.ascii_letters)
# print(string.ascii_letters[2])
# print(dict['a'])
# print(string.ascii_letters[dict['a']-1])

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


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'


class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
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
        copy_valid_words = self.valid_words.copy()
        return copy_valid_words

    def __str__(self):
        return "Message:" + str(self.message_text)

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        

        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        self.number_shift = shift

        dict = {}  # empty dictionary to be filled with letters (as keys) and numbers (as values)

        j = 1 + self.number_shift

        for i in string.ascii_letters:
            dict[i] = j
            j += 1
            if j > 26:  # If the shift key is 25, then a --> 26, and b --> 1, A --> 25, B --> 1
                j -= 26

        return dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        # print('in apply_shift, shift value is',shift)
        assert type(shift) == int, 'warning: shift value must be an integer'
        assert shift >= 0 and shift < 26, 'warning: shift value needs to be 0-25'
        self.number_shift = shift
        shift_dict = self.build_shift_dict(self.number_shift)

        # Framework
        # Highest Level Framework
        #      new message = message + shift
        #
        # Next Level Down
        #      for i in the length of the original message
        #          element = message[i]
        #          if the element is a letter,
        #              find the shifted value of that letter
        #          new message = element
        #
        # How does the dictionary become a part of this?
        # say the random i-th element is "a" and the shift was 5.  The new letter therefore should be "f" (remember to subtract 1 since we have "a" as 1. So a shift of one should be "b", not "c".

        shifted_message = ""

        for element in self.message_text:
            if element not in string.ascii_letters:
                shifted_message += element  # this will be a punctuation & spaces.
            elif element in string.ascii_uppercase:
                shifted_message += string.ascii_uppercase[shift_dict[element] - 1]
            else:
                shifted_message += string.ascii_lowercase[shift_dict[element] - 1]

        return shifted_message


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        copy_encryption_dict = self.encryption_dict.copy()
        return copy_encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        assert shift >= 0 and shift < 26, 'warning: shift value needs to be 0-25'
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value

        General Form

        Loop over 1-26 (0-25)
        use "split" to break the message up into individual words.
        for each entity from the split message, check if it is a valid word
        if valid word, add one to a valid-word-counter
        at the end of the number loop, compare # valid words to Max-Valid-Words
        if this is the new maximum, the the tuple is replaced by this shift value

        After the number loop, decrypt the message using the best-case shift value
        '''
        max_valid_words = 0
        best_shift = 0
        valid_words_list = self.valid_words
        # for i in range(1,27): #loop over all possible shift values
        for i in range(26):  # loop over all possible shift values
            num_valid_words = 0
            unjumbled_string = self.apply_shift(i)  # this decrypts the entire message at once using the shift value i
            unjumble_list = unjumbled_string.split()
            # print('jumble_list', unjumble_list)
            for word in unjumble_list:
                if is_word(valid_words_list,
                           word):  # this function actually removes punctuation, so you dont have to worry about that.
                    num_valid_words += 1
                    # print(num_valid_words, word)
            if num_valid_words > max_valid_words:
                max_valid_words = num_valid_words  # need to overwrite your progress with the latest maximum.
                best_shift = i  # save the best shift value that you've found so far, erasing the previous

        decrytped_message = self.apply_shift(best_shift)

        return (best_shift, decrytped_message)


if __name__ == '__main__':
    # #Example test case (PlaintextMessage)
    # plaintext = PlaintextMessage('hello', 2)
    # print('Expected Output: jgnnq')
    # print('Actual Output:', plaintext.get_message_text_encrypted())
    #
    # Example test case (CiphertextMessage)
    # ciphertext = CiphertextMessage('jgnnq')
    # print('Expected Output:', (24, 'hello'))
    # print('Actual Output:', ciphertext.decrypt_message())

    # Example test case for Building and Shifting a message class statement
    #     message = Message('hello')
    #     print(message)

    #
    # #TODO: WRITE YOUR TEST CASES HERE
    plaintext = PlaintextMessage("I don't know why you say goodbye. I say hello", 5)
    print("Expected Output:N its'y pstb dtz xfd lttigdj. N xfd mjqqt")
    print('Actual Output:', plaintext.get_message_text_encrypted())

    ciphertext = CiphertextMessage('Bee Bt Cvu Cpphfs')
    print('Expected Output:', (25, 'Add As But'))
    print('Actual Output:', ciphertext.decrypt_message())

    # #TODO: best shift value and unencrypted story

    jumble_story = get_story_string()
    ciphertext = CiphertextMessage(jumble_story)
    # ciphertext = CiphertextMessage('Xoqy Tzcfsm wg o amhvwqoz qvofoqhsf qfsohsr cb hvs gdif ct o acasbh hc vszd')
    print('Returned story.txt:', ciphertext.decrypt_message())

