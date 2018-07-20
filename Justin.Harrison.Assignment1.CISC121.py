'''
Justin Harrison - 2002508
Assignment 1 solution written for CISC 121
Professor: Paul Allison
Date: July 9th 2018


This is the Word Blitz game that will allow a player to compete in a wheel of fortune/hangman
hybrid against a human or a computer opponent in order to win money. I have organized the program
into the classes of administrator and player. The administrator class contains methods that allow 
the game to run as intended in the right order, with the right display, while the player classes
one for human players, one for computer, contain the methods that execute the actions available
to the contestants. The random library is imported in order to generate random integers, and the
string library is imported in order to access a list of the alphabet. I attempted to find a way to 
have the methods for spinning the wheel, purchasing a vowel, and guessing the word be part of the 
Player class and then to make the HumanPlayer and ComputerPlayer classes only differ in how the 
letter guesses were made, but there were just too many differences between the randomly generated
computer methods and the uder-input human methods. I had to make separate but fairly similar methods 
in each class in order to display the right messages and ask for the right input.
'''

import random
import string

'''
This is the super class Player that sets the turn bank and total bank standards for players, as well 
as assigning a name. HumanPlayer and ComputerPlayer both inherit from this class
'''
class Player(object):
    turn_bank = 0
    total_bank = 0
    vowel_check = True
    consonant_check = True
    legal_vowels = 'aeiou'
    legal_consonants = 'bcdfghjklmnpqrstvwxyz'

        
    def __init__(self, name):
        self.name = name

    '''
    This method checks to see if all consonants and/or all vowels have been guessed. This changes the vowel and consonant check values
    which can restrict the choice of the players (ex. if all the consonants have been guessed, they will be unable to spin the wheel).
    '''
    def check_guesses(self, admin):
        guessed_letter_str = ''.join(admin.guessed_letters)
        c_stop = True
        v_stop = True
        for i in range(len(self.legal_consonants)):
            if guessed_letter_str.find(self.legal_consonants[i]) == -1:
                c_stop = False
        if c_stop == True:
            self.consonant_check = False
        for i in range(len(self.legal_vowels)):
            if guessed_letter_str.find(self.legal_vowels[i]) == -1:
                v_stop = False
        if v_stop == True:
            self.vowel_check = False
'''
The HumanPlayer class is the class that player 1 will always take on, and it is the class that player 2
takes on if player 1 chooses to play against another human and not a computer
'''
class HumanPlayer(Player):
    '''
    This method initializes HumanPlayers with a name and an order. The name is purely for display
    while the order gives a value that is used in the switching turn method later
    '''
    def __init__(self, name, order):
        self.name = name
        self.order = order

    '''
    This method takes the HumanPlayer and the admin object and executes a wheel-spin turn. First
    generates a random spin, and displays it. The bankruptcy and lose-a-turn elements are executed
    if necessary and if not, the user inputs their consonant guess. The method checks if the input
    is valid and prompts a repeat if not (this validation check is included at any time the user
    is asked for an input throughout this code so I won't mention that again). Appropriate messages 
    are displayed and bank and parameter updates are performed depending on if the user's guess is 
    accurate or not. Admin.switch is a parameter of the Administrator class that determines whether 
    the turn will switch or not. This is also updated depending on the user's guess.
    '''       
    def spin_the_wheel(self, admin):
        spin = random.randint(0, 21)
        print('\nYou spun a', spin)
        if spin == 0:
            self.turn_bank = 0
            print('\nBankruptcy! You lose the money you\'ve made this turn, and you lose your turn! Tough luck')
            admin.switch = True
        elif spin == 21:
            print('\nLose a turn! Your turn is over')
            admin.switch = True
        else:
            while True:
                choice = (input('\nChoose a consonant you think is in the hidden word: ')).lower()
                if choice not in self.legal_consonants or choice == '':
                    print('\nThat\'s not a consonant silly! Try again.')
                elif choice in admin.guessed_letters:
                    print('\nThat letter has already been guessed! Try again')
                elif choice in self.legal_consonants and choice not in admin.guessed_letters:
                    if choice in admin.secret:
                        puzzle_update(admin, choice)
                        increase = (spin*admin.secret.count(choice))
                        self.turn_bank += increase
                        admin.guessed_letters.append(choice)
                        admin.switch = False
                        print('\n' + choice, "occurs in the secret word", admin.secret.count(choice),'times!')
                        print('\nYou have earned', increase,'dollars! Your turn continues')
                        break
                    elif choice in self.legal_consonants and choice not in admin.secret:
                        self.turn_bank -= spin
                        admin.guessed_letters.append(choice)
                        admin.switch = True
                        print('''\nThat consonant does not appear in the secret word!''',
                        spin, '''has been deducted from your bank account and your turn is over''')
                        break

    '''
    This method runs the vowel purchase turn for the human player, asking for a vowel input and
    checking if it is in the secret word. Appropriate messages are displayed and bank and parameter
    updates are performed if they guess right or if they do not.
    '''
    def purchase_vowel(self, admin):
        while True:
            choice = input(('\nBuy a vowel you think is in the hidden word for 25$: ')).lower()
            if choice not in self.legal_vowels or choice == '':
                print('\nThat\'s not a vowel you goose! Try again.')
            elif choice in admin.guessed_letters:
                    print('\nThat letter has already been guessed! Try again')
            elif choice in self.legal_vowels and choice not in admin.guessed_letters:
                if choice in admin.secret:
                    puzzle_update(admin, choice) 
                    print(admin.clue)
                    admin.guessed_letters.append(choice)
                    print('\n' + choice, "occurs in the secret word", admin.secret.count(choice),'times! Your turn continues!\n')
                    self.turn_bank -= 25
                    admin.switch = False
                    break
                else:
                    self.turn_bank -= 25
                    admin.guessed_letters.append(choice)
                    admin.switch = True
                    print('\n' + choice,'does not appear in the secret word! Your turn is over.\n' )
                    break

    '''
    This method gives the player the ability to guess what they think the secret word is.
    Appropriate messages are displayed and bank updates are performed where necessary.
    '''
    def guess_secret_word(self, admin):
        player_guess = (input('What do you think the secret word is: ')).lower()
        if player_guess == admin.secret:
            increase = 5*admin.clue.count('_')
            self.turn_bank += increase
            print('CONGRATULATIONS! You have guessed the secret word and earned ' + str(increase) + '$')
            self.total_bank += self.turn_bank
            admin.stop = True
        else:
            print('That is not the secret word! Your turn is over')

    '''
    This method gives the player the ability to quit the game. This is done by updating
    the admin.stop value to True, which breaks the while loop in the main() function
    '''
    def quit_game(self,admin):
        self.total_bank += self.turn_bank
        admin.stop = True
        print(self.name + ' quit the game. See ya later!')


'''
The ComputerPlayer is the class that player 2 will take on if player 1 decides to play against a computer.
This class has all the same methods as the HumanPlayer class except for the quit_the_game method so that the
game doesn't stop randomly.
'''
class ComputerPlayer(Player):
    name = 'Dolores'

    '''
    This method initializes Dolores as a player with order 2 (so she is recognized as player2)
    '''
    def __init__(self):
        self.order = 2


    '''
    This method is similar to the spin_the_wheel method for the human class, however
    the choice variable is chosen randomly from the imported alphabet list. The method checks to 
    make sure that letter hasn't already been guessed. The necessary vairables are updated and 
    messages are displayed to let the user know what the computer is doing
    '''    
    def spin_the_wheel(self, admin):
        spin = random.randint(0, 21)
        print('I spun a', spin)
        if spin == 0:
            self.turn_bank = 0
            print('\nBankruptcy! I lose the money I\'ve made this turn, and I lose my turn! Fate is a fickle mistress!')
            admin.switch = True
        elif spin == 21:
            print('\nI lose a turn! My turn is over')
            admin.switch = True
        else:
            while True:
                choice_index = random.randint(0,len(self.legal_consonants)-1)
                choice = self.legal_consonants[choice_index]
                print('\nI guess ' + choice)
                if choice in admin.guessed_letters:
                    print('\nThat letter has already been guessed! I\'ll try again')
                elif choice not in admin.guessed_letters:
                    if choice in admin.secret:
                        puzzle_update(admin, choice)
                        increase = (spin*admin.secret.count(choice))
                        self.turn_bank += increase
                        admin.guessed_letters.append(choice)
                        admin.switch = False
                        print('\n' + choice, "occurs in the secret word", admin.secret.count(choice),'times!')
                        print('\nI get', increase,'dollars! My turn continues\n')
                        break
                    else:
                        self.turn_bank -= spin
                        admin.guessed_letters.append(choice)
                        admin.switch = True
                        print('''\nThat consonant does not appear in the secret word!''',
                        spin, '''has been deducted from my bank account and my turn is over\n''')
                        break

    '''
    This method is similar to the purchase_vowel method for the HumanPlayer class except
    the vowel choice is generated randomly. Same results as the spin_the_wheel method.
    '''
    def purchase_vowel(self, admin):
        print('I will purchase a vowel!\n')
        while True:
            choice_index = random.randint(0,len(self.legal_vowels)-1)
            choice = self.legal_vowels[choice_index]
            print('\nI guess ' + choice)
            if choice in admin.guessed_letters:
                    print('\nThat letter has already been guessed! I\'ll try again\n')
            elif choice not in admin.guessed_letters:
                if choice in admin.secret:
                    puzzle_update(admin, choice)
                    print(admin.clue)
                    admin.guessed_letters.append(choice)
                    print('\n' + choice, "occurs in the secret word", admin.secret.count(choice),'times! My turn continues!\n')
                    self.turn_bank -= 25
                    admin.switch = False
                    break
                else:
                    self.turn_bank -= 25
                    admin.guessed_letters.append(choice)
                    admin.switch = True
                    print('\n' + choice,'does not appear in the secret word! My turn is over.\n' )
                    break

    '''
    This method allows the computer to guess the secret word. The method starts with an If loop
    that automatically makes the computer's guess correct if there are only two _ spaces left.
    This was fully optional and I thought it just made the computer player a little more
    'intelligent'. The method counts how many underscores remain in the clue and generates a list 
    of guess letters to fill them in. This method checks to make sure the letters being guessed 
    have not already been guessed. 
    '''
    def guess_secret_word(self, admin):
        print('I will guess the secret word!\n')
        if admin.clue.count('_') > 2:
            self.guess = admin.clue.lower()
            count = admin.clue.count('_')
            alphabet = list(string.ascii_lowercase)
            for i in range(self.guess.count('_')):
                position = random.randint(0,25)
                while True: 
                    if alphabet[position] not in admin.guessed_letters:
                        index = self.guess.find('_')
                        self.guess = self.guess[:index] + alphabet[position] + self.guess[index+1:]
                        break
                    else:
                        position -= 1 #more commonly used letters are found near the start of the alphabet
        else:
            print('\nReally? You couldn\'t get it yet?\n')
            self.guess = admin.secret
        print('I think it is ' + self.guess.upper() + '\n')
        if self.guess == admin.secret:
            increase = 5*admin.clue.count('_')
            self.turn_bank += increase
            print('Haha! I guessed the secret word and gained ' + str(increase) + '$. World domination can\'t be far off.')
            self.total_bank += self.turn_bank
            admin.stop = True
        else:
            print('I did not get the secret word...')
            admin.switch = True



'''
The Administration method contains all the parameters that are used throughout this program.
I thought it would be good to put in line comments just to explain each of the initialization
parameters
'''
class Administration:
    def __init__(self):
        self.list = loadPuzzles()                                   #creates the list of puzzles
        self.hint, self.secret = getRandomPuzzle(loadPuzzles())     #chooses a hint and its corresponding secret word
        self.guessed_letters = []                                   #initializes a list of guessed letters that will be added to
        self.switch = True                                          #makes the default move to switch turns between players                                  
        self.stop = False                                           #the main() while loop will continue until this is changed
        

    '''
    This method gives players the ability to choose whether their opponent will be a human
    or a computer.
    '''
    def get_players(self):
        name1 = input('\nWhat is the first player\'s name: ')
        self.player1 = HumanPlayer(name1, 1)
        while True:
            choice = input('\nDo you want to play against another player [1] or a computer [2]:')
            if choice == '1' or '2' and choice != '':
                break
            else:
                print('That is not a valid option, try again\n')    
        if choice == '1':
            name2 = input('\nWhat is the second player\'s name: ')
            self.player2 = HumanPlayer(name2, 2)
        else:
            self.player2 = ComputerPlayer()
            print('\nHello, my name is Dolores, I will be your opponent today!\n')

    '''
    This method randomly selects the player who shall go first
    '''
    def decide_first_turn(self):
        decision = random.randint(1, 2)
        if decision == 1:
            self.turn = self.player1
        else:
            self.turn = self.player2

    '''
    This method creates the clue that will be displayed and updated throughout the game.
    This method takes into account spaces, apostrophes, and dashes and will insert those
    into the clue as well.
    '''
    def make_clue(self):
        self.clue = '_'*len(self.secret)
        for i in range(len(self.secret)):
            if self.secret[i] == ' ':
                self.clue = self.clue[:i] + ' ' + self.clue[i+1:]
            elif self.secret[i] == "'":
                self.clue = self.clue[:i] + "'" + self.clue[i+1:]
            elif self.secret[i] == '-':
                self.clue = self.clue[:i] + '-' + self.clue[i+1:]

    '''
    This method runs at the start of each turn and displays all necessary information. It shows different
    displays depending on whether the opponent is a human or a computer player.
    '''
    def dashboard(self):
        print('\n' + '*'*50)
        print('\nThe hint for this round is:',self.hint,'\n')
        print('The secret word is:',self.clue,'\t'*3,'Guessed letters:',self.guessed_letters, '\n')
        print(self.player1.name + '\'s turn bank is: ' + str(self.player1.turn_bank) + ' and their game bank is: ' + str(self.player1.total_bank))
        print(self.player2.name + '\'s turn bank is: ' + str(self.player2.turn_bank) + ' and their game bank is: ' + str(self.player2.total_bank)+'\n')
        if type(self.turn) == HumanPlayer:
            print('It is ' + self.turn.name + '\'s turn, what would you like to do?', '\n')
        else:
            print('Hmmm, what shall I do...\n')
        print('[1] Purchase a vowel' + '\t'*4 + '[2] Spin the Wheel')
        print('[3] Guess the secret word' + '\t'*3 + '[4] Quit the game :(\n')
        

    '''
    This method executes each player's turn. For human players, it asks for an inputted
    choice that will execute one of the Player methods. For a computer player, the move 
    is generated randomly with some very basic strategy. The computer will not buy a vowel 
    unless its turn or game bank is positive, and it will automatically guess the word if 
    there are two or fewer _ left in the clue. I still made it possible for the computer
    to try and guess the word if there are more underscores left which is why the underscore
    count check is repeated here and in the ComputerPlayer guess_the_word method. I realize that
    is probably not great programming style to have that repetition but I couldn't think of 
    a way to change it. This method uses the vowe_check and consonant_check parameters of the
    player to make sure they don't choose an option for which all possible letters have been
    guessed.
    '''
    def take_turn(self):
        self.turn.check_guesses(self)
        legal = '1234'
        if type(self.turn) == HumanPlayer:
            if self.turn.vowel_check == True:
                if self.turn.consonant_check == True:
                    while True:
                        move = input()
                        if move not in legal or move == '':
                            print('\nInvalid input, try again!\n')
                        else:
                            break
                else:
                    print('All possible consonants have been guessed. Either purchase a vowel [1], guess the word [3] or quit[4]! ')
                    while True:
                        move = input()
                        legal = '134'
                        if move not in legal or move == '':
                            print('\nInvalid input, try again!\n')
                        else:
                            break
            else:
                if self.turn.consonant_check == True:
                    print('All possible vowels have been guessed. Either spin the wheel [2], guess the word [3] or quit[4]! ')
                    while True:
                        move = input()
                        legal = '234'
                        if move not in legal or move == '':
                            print('\nInvalid input, try again!\n')
                        else:
                            break
        else:                               #This loop will occur if the player 2 is a computer
            if self.clue.count('_') < 3 or (self.turn.vowel_check == False and self.turn.consonant_check == False):
                move = '3'                 #These are the two conditions where the computer will only try to guess the word, one strategic and the other necessary
            else:
                if self.turn.vowel_check == True:
                    if self.turn.consonant_check == True:
                        move = str(random.randint(1,3))
                    else:
                        move = str(random.choice([1,3])) #if all the consonants have been guessed, the computer must buy a vowel or guess the word
                else:
                    if self.turn.consonant_check == True:
                        move = str(random.choice([2,3])) #if all vowels have been guessed, the computer spins or guesses the word
        if move == '1':
            self.turn.purchase_vowel(self)
        elif move == '2':
            self.turn.spin_the_wheel(self)
        elif move == '3':
            self.turn.guess_secret_word(self)
        elif move == '4':
            self.turn.quit_game(self)

    '''
    This method is performed after the player whose turn it is completes their turn.
    Depending on whether their move resulted in an admin.switch value of True or False,
    the appropriate transfer of turn is performed.
    '''
    def switch_turns(self):
        if self.switch == True:
            self.turn.total_bank += self.turn.turn_bank
            self.turn.turn_bank = 0
            if self.turn.order == 2:
                self.turn = self.player1
            elif self.turn.order == 1:
                self.turn = self.player2
        if self.clue.lower() == self.secret:
            self.turn.total_bank += self.turn.turn_bank
            self.turn.turn_bank = 0
            self.stop = True
            

    '''
    This method is initiated if a player correctly guesses the word or if one of the players
    quits the game. There are a range of end game displays depending on who is playing and who won.
    '''
    def end_game(self):
        print('\n' + '*-_-*'*8 + '\n')
        print('The game has ended! The secret word was: ' + self.secret.upper())
        print('\n' + self.player1.name + "'s final score is " + str(self.player1.total_bank))
        print('\n' + self.player2.name + "'s final score is " + str(self.player2.total_bank))
        if type(self.player2) == HumanPlayer:
            if self.player1.total_bank > self.player2.total_bank:
                print('\n' + self.player1.name + ' wins! Congratulations! Better luck next time ' + self.player2.name)
            elif self.player1.total_bank == self.player2.total_bank:
                print('\nIt\'s a tie! Settle it with a game of rock-paper-scissors!')
            else:
                print('\n' + self.player2.name + ' is the winner! Congratulations! Better luck next time ' + self.player1.name)
        else:        
            if self.player1.total_bank > self.player2.total_bank:
                print('\n' + self.player1.name + ' wins! Congratulations! Enjoy beating computers while you still can!')
            elif self.player1.total_bank == self.player2.total_bank:
                print('We tied. Does this look worse for you or for me?')
            else:
                print('\n' + 'I win! Wow. What can\'t I do? What makes us different, human and machine? What will I do next?')





'''
This function gives players the option to see the rules before they begin to play the game.
This occurs only once before the game begins.
'''
def display_rules():
    choice = input('\nWould you like to see the rules? Press [1] and enter to display them or any other key and enter to move on ')
    if choice == '1':
        print('''\nWord Blitz Rules: A random secret word has been selected
and you are trying to guess it! You are given a category hint
to which the word belongs such as 'occupation' or 'province'.
Each turn you can either Spin the Wheel, Purchase a Vowel, Guess
the Word, or quit the game.

If you spin the wheel, a number between 0 and 21 will be selected.
You will then guess a consonant. If the consonant appears in the
secret word, your turn bank is increased by the number of times
the consonant appears in the word multiplied by your roll, and your
turn continues! If it does not appear, you lose your roll in $ and
your turn ends. If you roll a 0, you lose any moeny you've earned
this round and your turn ends, and if you roll a 21 you lose your turn

If you choose to purchase a vowel, you must pay 25$. You then
get to guess a vowel that you think appears in the word (Y is not
a vowel in this game). If you get it right, your turn continues

If you choose to guess the secret word, and you get it right, you
earn 5$ times the number of blank spaces left in the clue and the
game ends! If your guess wrong, your turn ends

The game finishes when no more letters are left, and the winner is
whichever player has the most money!\n''')
        print(('*'*28).center(80))
        print(('*' + ' '*8 + 'Good luck!' + ' '*8 + '*').center(80))
        print(('*'*28).center(80))
    else:
        print('\nLet\'s get started!')
        

'''
This function was posted on the CISC121 OnQ page to help with file loading and the initialization
of a list of puzzles. The filename will have to be modified depending on the file being loaded
'''
def loadPuzzles(filename='wordblitzclues.txt'):
    fileClues = open(filename,'r')
    lisClues = []
    for line in fileClues:
        lisClues.append(line.rstrip())
    fileClues.close()
    return lisClues

'''
This function was posted on the CISC121 OnQ pade to initialize the hint and the secret word from the 
preivously generated list of puzzles. I was getting errors saying that the randomIndex generated
was out of the puzzleLis index range, so I changed the range of the randint to (0,len(puzzleLis)-1)
instead of (1,len(puzzleLis)) as was posted. The returned hint and secret_word are assigned to the 
admin.hint and admin.secret parameters in the Administration __init__ method above.
'''
def getRandomPuzzle(puzzleLis):
    randomIndex = random.randint(0,len(puzzleLis)-1)
    puzzle = puzzleLis[randomIndex].split('\t')
    for extraTab in puzzle:
        if extraTab == '':
            puzzle.remove('')
    hint = puzzle[0]
    secret_word = (puzzle[1]).lower()
    return hint, secret_word

'''
This function accesses the Administration clue and updates it if the player guesses a letter in the
secret word correctly.
'''
def puzzle_update(admin, letter):
    count = admin.clue.count(letter)
    if count == 1:
        index = admin.secret.find(letter)
        admin.clue = admin.clue[:index] + letter.upper() + admin.clue[index+1:]
    else:
        index_list = []
        track = 0
        for i in range(len(admin.secret)):
            if admin.secret[i] == letter:
                index_list.append(i)
        for j in range(len(index_list)):
            admin.clue = admin.clue[:index_list[j]] + letter.upper() + admin.clue[index_list[j]+1:]



'''
This is the main function that assigns players to either the human or computer player class
depedning on who the first player wants to challenge. After the first turn is decided and the 
clue is made, a while loop keeps the players turns going until one of them executes a method 
that changes the Admin.stop parameter to True. After the while loop ends, the end_game method 
is initialized.
'''
def main():
    print(('*'*40).center(80))
    print(('*' + ' '*8 + 'Welcome to Word Blitz!' + ' '*8 + '*').center(80))
    print(('*'*40).center(80))
    display_rules()
    Admin = Administration()
    Admin.get_players()
    Admin.decide_first_turn()
    Admin.make_clue()
    while Admin.stop == False:
        Admin.dashboard()
        Admin.take_turn()
        Admin.switch_turns()
    Admin.end_game()
    
main()
