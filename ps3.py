# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
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

#
# Problem #1: Scoring a word
#
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

    first_part = 0 #sum of points for letters in the word
    for letter in word:
        letter = str.lower(letter)
        first_part += SCRABBLE_LETTER_VALUES[letter]

    second_part = max(1, 7*len(word) - 3*(n-len(word)))

    score = first_part * second_part

    return score
# -----------------------------------

#
# Make sure you understand how this function works and what it does!
#
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

    print("Inside function display_hand")
    for letter in hand.keys():           # letter cycles through all of the keys in the dictionary, including repeats
        for j in range(hand[letter]):    # hand[letter] returns a value. For loops stop at n-1.
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
    num_vowels = int(math.ceil(n / 3))      #Same as ROUNDUP in excel. int(CEIL(1/3)) = 1. 3 -> 1, 4 -> 2,...

    for i in range(num_vowels):             #Adds num_vowels amount of vowels to dictionary hand.
        if i == 0:                          #ALWAYS adds another Wildcard. So if they dont use the wildcard, you're going to stockpile.
            x = '*'
        else:
            x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):          #Adds n-num_vowels amount of consonants to dictionary hand.
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
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

    print('In Update Hand. Testing word:',word)
    print('You are currently holding',hand)
    new_hand = hand.copy()
    # for letter in hand:
    #     letter = str.lower(letter)
    #     # new_hand[letter] = hand[letter]                  #Dont know how to clone Dictionary. This works.
    #     new_hand[letter] = hand.get(letter)               #This also works. They APPEAR to be the same.
    # print(new_hand)

    #Need to remove wildcards when they are used.
    # WILDCARD STEP 1: This will determine if the wildcard is in the hand.
    wildcard_exist = new_hand.get("*", 0)


    for letter in word:                #loop to remove letters one-by-one. this creates negatives if you try to use too many
        letter = str.lower(letter)
        if letter in hand:
            new_hand[letter] = new_hand.get(letter, 0) - 1
        # Need to remove wildcards when they are used.
        # WILDCARD STEP 2: Letter will cycle through actual letters. Wont look at wildcard.
        # So this will remove the wildcard in the event that you tried to use a vowel without owning it, but you still have the wildcard.
        elif letter in VOWELS and wildcard_exist > 0:
            print()
            print("Removing the wildcard")
            print()
            new_hand["*"] = new_hand.get("*", 0) - 1
        else:
            print('You dont have', letter, 'in your hand')

    for letter in hand:                #Delete out any 0 or negative values from the dictionary
        letter = str.lower(letter)
        if new_hand[letter] <= 0:
            del (new_hand[letter])

    # print('Letters in your hand after playing that word')
    # print(new_hand)
    # print(hand)

    return new_hand

## Test calls to function 'update_hand'
# hand_dict = {'a':1,'q':1, 'l':2, 'm':1, 'u':1, 'i':1}
# word_str = 'ALiS$ONQ'
# update_hand(hand_dict,word_str)

##Testing out cloning dictionaries
#
# dict_1 = {'a':1,'b':1, 'c':1, 'd':1, 'e':1, 'f':1}
# dict_2 = dict_1.copy()
# # for letter in dict_1.keys():
# #     dict_2[letter] = dict_1.get(letter)
# print(dict_1)
# print(dict_2)
# dict_2['a'] = 0
# print(dict_1)
# print(dict_2)

#
# Problem #3: Test word validity
#
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

    # print('Testing validity of',word,'with hand',hand)
    lowercase_word = ''
    for letter in word:
        lowercase_word += str.lower(letter)

    print('Lowercase_word is created:',lowercase_word)
    j = 0
    k = 0
    letters_used = {}
    wildcard_spot = lowercase_word.find('*')  #the find() method returns -1 if the substring is not found.
    print('wildcard position',wildcard_spot)
    wildcard_subs = []

# Did they use a Wildcard: Yes
    if wildcard_spot != -1:
        for letter in VOWELS:
            replace_word = lowercase_word[0:wildcard_spot] + letter + lowercase_word[wildcard_spot + 1:len(lowercase_word)]
            if replace_word in word_list:
                wildcard_subs.append(replace_word)
        print('Possible Wild Card Substitutes:',wildcard_subs)   #Lets see all of the possible words available.

        # Now, using the first option of all possible words, see if it is in the word list.
        print('length of wildcard_subs',len(wildcard_subs))
        if len(wildcard_subs) > 0:
            for letter in wildcard_subs[0]:
                print('letter at position 1',letter)
                letters_used[letter] = letters_used.get(letter,0)+1

            print('letters_used dictionary',letters_used)
            for letter in lowercase_word:
                i = letters_used.get(letter,0)
                j = hand.get(letter,-1)
                print('letter at position 2:',letter,', i:',i,', j:',j)
                if not i <= j:
                    k += 1
            return k == 0
        else:
            print('In func is_valid_word. That is not a valid word')
            return False


# Did they use a Wildcard: No
    elif wildcard_spot == -1 and lowercase_word in word_list:
        for letter in lowercase_word:
            letters_used[letter] = letters_used.get(letter,0)+1

        # for letter in letters_used.keys():
        for letter in lowercase_word:
            i = letters_used.get(letter,0)
            j = hand.get(letter,-1)
            # print(letter,i,j)
            if not i <= j:
                k += 1
        return k == 0

    else:
        print('In func is_valid_word. That is not a valid word')
        return False


# ## Testing Inputs of is_valid_word
# example_word = 'alpha'
# example_hand = {'a':3,'l':1, 'p':1, 'h':1, 'e':1, 'f':1}
# example_list = ['alpha','beta','gamma']
#
# print(is_valid_word(example_word,example_hand,example_list))
#
# example_word = 'alpha'
# example_hand = {'a':2,'l':1, 'p':1, 'h':1, 'g':1, 'f':1}
# example_list = ['alpha','beta','gamma','delta']
#
# print(is_valid_word(example_word,example_hand,example_list))
#
# example_word = 'alpha'
# example_hand = {'a':2,'l':1, 'p':1, 'h':1, 'g':1, 'f':1}
# example_list = ['alph','beta','gamma','delta']
#
# print(is_valid_word(example_word,example_hand,example_list))
#
# example_word = 'alphA'
# example_hand = {'a':2,'l':1, 'p':1, 'h':1, 'g':1, 'f':1}
# example_list = ['alpha','beta','gamma','delta']
#


# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: n, an integer
    """
    n = 0
    # Use ".values" to pull the quantity of each letter in the player's hand.
    # In the event that the code had 0s instead of removing keys, this would still work.
    for values in hand.values():
        n += values
    return n


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

    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    total_score = 0
    current_score = 0
    num_letters = calculate_handlen(hand)
    # As long as there are still letters left in the hand:
    ## As long As = While Loop
    ## use function 'calculate_hand_len' to find the number of letters in the hand.

    while num_letters > 0:

        # Display the hand
        print(hand)
        print('Display Hand Function Call in play_hand')
        display_hand(hand)

        # Ask user for input
        user_word = input('Enter a word, or "!!" to indicate that you are finished : ')

        # If the input is two exclamation points, end the game
        if user_word == '!!':
                break
        else:
            if is_valid_word(user_word,hand,word_list):
                #user_word is a valid word
                current_score = get_word_score(user_word,num_letters)
                total_score += current_score
                print('"'+user_word+'" earned',current_score,'points. Total:',total_score,'points')
            else:
                #user_word is not valid
                print("That is not a valid word. Please choose another word")


            # update the user's hand by removing the letters of their inputted word
            print('hand before call to update_hand',hand)
            hand = update_hand(hand,user_word)
            print('hand after call to update_hand', hand)
            num_letters = calculate_handlen(hand)

    print("Game is over. Total score for this hand is: ",total_score)
    print("- - - - - - - - - - - - - - - - ")

    return total_score




#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

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
    new_hand = hand.copy()
    new_letter = str.lower(letter)

    if new_letter in new_hand:
        print("Changing out letter",new_letter,"in function substitute_hand")
        new_value = hand.get(new_letter,0)
        while new_letter in hand:
            new_letter = random.choice(VOWELS+CONSONANTS)
        new_hand[new_letter] = new_value
        del(new_hand[str.lower(letter)])
    else:
        print("You do not have",new_letter,"in your hand")

    return new_hand


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

    game_score = 0
    hand_score = 0
    sub_int = 0
    replay_int = 0
    num_hands =  int(input("Enter total number of hands: "))
    print('Hand Size is set to',HAND_SIZE)
    for i in range(num_hands):

        hand = deal_hand(HAND_SIZE)
        print('Current hand:',hand)
        sub_letter = input("Would you like to substitute a letter? yes/no: ")
        if sub_letter == "yes" and sub_int == 0:
            sub_int += 1
            sub_letter = input("Which letter Would you like to substitute? ")
            hand = substitute_hand(hand,sub_letter)
            print()
            print('Current hand:', hand)
        elif sub_int != 0:
            print("you already substituted a letter in this game. Can't substitute again.")

        hand_score += play_hand(hand,word_list)
        replay_hand = input("Would you like to replay this hand? yes/no ")
        if replay_hand == "yes" and replay_int == 0:
            replay_int += 1
            hand_score = max(hand_score, play_hand(hand, word_list))
        elif replay_int != 0:
            print("You already replayed a hand. Can't replay again.")
        game_score += hand_score
        hand_score = 0

    print("Total score over all hands: ",game_score)


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)




# print(is_valid_word(example_word,example_hand,example_list))
#
# example_word = "*aLPHa"
# example_hand = {'a':1,'j':1, 'e':1, 'f':1, '*':1, 'r':1, 'x':1}
example_hand = {'a':6,'c':6, 'f':6, 'i':6, '*':6, 't':6, 'x':6}
example_letter = 'g'
new_letter = VOWELS+CONSONANTS
# print(random.choice(new_letter))
# print(random.choice(VOWELS+CONSONANTS))
# new_value = example_hand.values('c')

