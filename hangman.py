# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

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
    Returns a list of valid words. Words are strings of lower-case letters.
    
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

# print(is_word_guessed(secret_word,letters_guessed))

def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    Uses i to tally the number of correct letters guessed.
    if i = length of the secret word, then the entire word has been guessed. otherwise not.
    '''
    i = 0
    for char in secret_word:
        if char in letters_guessed:
            i += 1
            # print("True", char,i)
        # else:
            # print("false", char,i)
    return i == len(secret_word)


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    This function starts by creating a blank string, and then adds correct guessed letters
        in their correct spots, and blanks in missing spots.
    '''

    progress = ""     # Create a blank string. We're going to add to this string.

    for char in secret_word:
        if char in letters_guessed:
            l_or_b = char
        else:
            l_or_b = "_ "
        progress += l_or_b

    return progress


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    all_letters = "abcdefghijklmnopqrstuvwxyz"
    available_letters = ""
    for char in all_letters:
        if char not in letters_guessed:
            available_letters += char
    return available_letters
    
def check_guess_validity(current_guess,letters_guessed):
    '''
    current_guess: the string value entered by user
    letters_guessed: the list of letters already guessed
    returns: Boolean of True if this the user entered a new letter, False otherwise
    '''
    if current_guess == '*':
        valid = True
    elif not str.isalpha(current_guess):
        print(current_guess, 'is not a letter. Guess letters only')
        valid = False
    elif len(current_guess) > 1:
        print('Your guess must be 1 letter at a time')
        valid = False
    elif current_guess in letters_guessed:
        print('You already guessed that letter. Guess a new letter')
        valid = False
    else:
        valid = True
    return valid


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
    #Initialize Variables
    letters_guessed = []
    n = 6               # This is the number of incorrect guesses user is allowed
    correct_guesses = 0 # This is the number of correct user made
    warnings = 0

    #Begin user prompts
    print('Welcome to the Game Hangman')
    print('I am thinking of a word that is',len(secret_word),'letters long')
    #Begin Loop
    while n > 0:
        available_letters = get_available_letters(letters_guessed)
        print('You have',n,'guesses remaining')
        print('Available letters:',available_letters)
        current_guess = str.lower(input('Please guess a letter '))

        # QA/QC the current guess
        valid_entry = check_guess_validity(current_guess,letters_guessed)
        if not valid_entry:
            warnings += 1
            print('You now have ',3-warnings,'remaining warnings before you lose a guess')
            if warnings % 3 == 0:
                n -= 1
                warnings = 0

        if valid_entry:
            letters_guessed.append(current_guess)
            progress = get_guessed_word(secret_word, letters_guessed)

            if current_guess in secret_word:
                print('Good Guess!')
                # print('Return from get_guessed_word', progress)
                correct_guesses += 1
                print(progress)
            else:
                print('That letter is not in my word.')
                # print('Return from get_guessed_word', progress)
                print(progress)
                if current_guess in "aeiou":
                    n -= 2
                    # print("vowels count as 2 strikes")
                else:
                    n -= 1
                    # print("consonants count as 1 strike")
            print('* * * * * * * * * * * * * *')

            x = is_word_guessed(secret_word, letters_guessed)
            if x:
                print('Congratulations! You discovered my secret word and saved a life!')
                print('Your score is',n*correct_guesses)
                return

    print('Too late. He met a short drop and a quick stop. The word I was thinking of is',secret_word)

    return

# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    PartialWord = my_word.replace('_ ','_')
    FullWord = other_word
    i = 0

    # print('testing with', PartialWord, FullWord)
    if len(PartialWord) == len(FullWord):
        # print('Same Length. Continue.')
        for j in range(len(FullWord)):
            # print(j, len(FullWord) - 1)
            if PartialWord[j] != '_' and PartialWord[j] == FullWord[j]:
                # print('Match of Spot', j)
                i += 1
            elif PartialWord[j] == '_' and FullWord[j] not in PartialWord:
                # print('Missing Spot here. Count for now', j)
                i += 1
            # else:
                 # print('Mismatch of Spot', j)

    return i == len(FullWord)



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    potential_matches = []
    for i in range(len(wordlist)): # This list named wordlist this is from the main program scope.
        if match_with_gaps(my_word, wordlist[i]):
            potential_matches.append(wordlist[i])
    if len(potential_matches) > 0:
        print('Potential Matches',potential_matches)
    else:
        print('No Matches Found')

    # No return. This will return "None"

    return



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)



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
    #Initialize Variables
    letters_guessed = []
    n = 6               # This is the number of incorrect guesses user is allowed
    correct_guesses = 0 # This is the number of correct user made
    warnings = 0

    #Begin user prompts
    print('Welcome to the Game Hangman with Hints')
    print('I am thinking of a word that is',len(secret_word),'letters long')
    #Begin Loop
    while n > 0:
        available_letters = get_available_letters(letters_guessed)
        print('You have',n,'guesses remaining')
        print('Available letters:',available_letters)
        current_guess = str.lower(input('Please guess a letter '))

        # QA/QC the current guess

        valid_entry = check_guess_validity(current_guess,letters_guessed)
        if not valid_entry:
            warnings += 1
            print('You now have ',3-warnings,'remaining warnings before you lose a guess')
            if warnings % 3 == 0:
                n -= 1
                warnings = 0

        if valid_entry and current_guess == '*':
            progress = get_guessed_word(secret_word, letters_guessed)
            show_possible_matches(progress)
        elif valid_entry and current_guess != '*':
            letters_guessed.append(current_guess)
            progress = get_guessed_word(secret_word, letters_guessed)

            if current_guess in secret_word:
                print('Good Guess!')
                # print('Return from get_guessed_word', progress)
                correct_guesses += 1
                print(progress)
            else:
                print('That letter is not in my word.')
                # print('Return from get_guessed_word', progress)
                print(progress)
                if current_guess in "aeiou":
                    n -= 2
                    # print("vowels count as 2 strikes")
                else:
                    n -= 1
                    # print("consonants count as 1 strike")
            print('* * * * * * * * * * * * * *')

            x = is_word_guessed(secret_word, letters_guessed)
            if x:
                print('Congratulations! You discovered my secret word and saved a life!')
                print('Your score is',n*correct_guesses)
                return

    print('Too late. He met a short drop and a quick stop. The word I was thinking of is',secret_word)

    return

# -----------------------------------


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
