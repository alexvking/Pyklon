# Alex King
# Solitaire.py

from Deck import Deck
import sys
import copy

# The Solitaire class holds several structures to track card positions

# deck: An object containing an array of cards
# columns: A list of lists, modeling each column of the game board
# faceup: A list corresponding to each column representing how many cards are 
#  face up
# draw: A list tracking all cards that are face up in the draw pile.
# stacks: A list of lists tracking cards in the accumulation piles.
# hint: Either the empty list or a source and a destination
# moves: An accumulating list of bools that tracks whether or not there is
#  a legal move on each draw of the deck. If all False when the deck is emptied,
#  the game is over.

# lateral_list: Every move from column to column should be productive; the same
#  move cannot happen twice and move the player closer towards a solution.
#  therefore, any time a lateral move is suggested, or a lateral move is made,
#  the move is added to a dictionary.

class Solitaire:

    # __init__ : void
    # Initializes all member variables and sets the game board
    def __init__(self):
        self.deck = Deck() # grab a shuffled deck of cards
        self.columns = [["ZZ"], ["ZZ"], ["ZZ"], ["ZZ"], 
                ["ZZ"], ["ZZ"], ["ZZ"]] # empty sentinel
        self.faceup = [1, 1, 1, 1, 1, 1, 1] # beginning configuration
        self.draw = [] # To begin, no cards are face up
        self.stacks = [["ZZ"], ["ZZ"], ["ZZ"], ["ZZ"]] # empty stacks
        self.hint = [] # No hint to start
        self.moves = [] # list of bools telling if the draw holds valid moves
        self.lateral_list = {}
        self.prev = copy.deepcopy(self)
        self.can_undo = False

        # Deal a new game
        for i in range(7):
            # self.columns.append([])
            for j in range (i + 1):
                self.columns[i].append(self.deck.draw())

    # printboard : void
    # Prints board layout in traditional Klondike style
    def printboard(self):
        # Top row: Draw cards and accumulation piles
        sys.stdout.write("\n")
        print "          DC   A1 A2 A3 A4"
        print "          \/"
        if len(self.deck.cards) > 0:
            sys.stdout.write('\033[44m' + "[.]" + '\033[0m') # cards remain
        else:
            sys.stdout.write('\033[44m' + "[ ]" + '\033[0m') # deck is empty
        sys.stdout.write(" ")

        # Print up to three drawn cards
        for i in range(-3, 0):
            if len(self.draw) >= (i * -1): # To print *last three* of the array
                self.print_card(self.draw[i])
            else: 
                sys.stdout.write("  ")
            sys.stdout.write(" ")
        sys.stdout.write("  ")

        # Print accumulation piles
        for stack in self.stacks:
            if len(stack) > 1:
                self.print_card(stack[-1])
                # sys.stdout.write(stack[-1]) # show only the top card
            else:
                sys.stdout.write("__")
            sys.stdout.write(" ")
        sys.stdout.write("\n\n")

        # Number the columns for ease of reference
        sys.stdout.write(" ")
        for num in range(1, 8):
            sys.stdout.write(str(num))
            sys.stdout.write("   ")
        sys.stdout.write("\n\n")

        # Find the largest column of working cards for array bounds
        max_length = max(len(x) for x in self.columns)

        # Print each column of cards one row at a time
        for row in range(1, (max_length + 1)):
            for col in range(7):
                if len(self.columns[col]) > row:
                    if (len(self.columns[col]) - (row)) <= self.faceup[col]:
                        self.print_card(self.columns[col][row])
                        # sys.stdout.write('\033[93m' + self.columns[col][row] + '\033[0m')
                    else:
                        sys.stdout.write('\033[44m' + "[]" + '\033[0m') # face down

                    sys.stdout.write("  ")
                else:
                    sys.stdout.write("    ")
            sys.stdout.write("     " + str(row)) # number each row
            sys.stdout.write("\n")
        sys.stdout.write("\n")

    # print_card : card -> void
    # Prints card with color depending on suit
    def print_card(self, c):
        if c[1] == "D":
            sys.stdout.write('\033[37;41m' + c + '\033[0m')
        elif c[1] == "H":
            sys.stdout.write('\033[32;41m' + c + '\033[0m')
        elif c[1] == "S":
            sys.stdout.write('\033[36;40m' + c + '\033[0m')
        elif c[1] == "C":
            sys.stdout.write('\033[33;40m' + c + '\033[0m')

    # can_stack_up : card card -> bool
    # Returns whether c1 can be placed on top of c2 in an accumulation pile
    def can_stack_up(self, c1, c2):
        ranks = "A23456789TJQK"
        order = c2[0] + c1[0] # e.g. "28", "JQ", "43"

        if c2[0] == "Z" and c1[0] == "A": 
            return True # base case

        # Check for sequential order and same suit
        else:
            return c1[1] == c2[1] and order in ranks

    # can_stack_down : card card -> bool
    # Returns whether a card can be added to the bottom of a column
    def can_stack_down(self, c1, c2):
        ranks = "A23456789TJQK"
        order = c1[0] + c2[0] # e.g. "28", "JQ", "43"

        if c2[0] == "Z" and c1[0] == "K": 
            return True # base case

        # Check order and suit
        return ((c1[1] == "S" and (c2[1] == "D" or c2[1] == "H") or
                 c1[1] == "C" and (c2[1] == "D" or c2[1] == "H") or
                 c1[1] == "D" and (c2[1] == "S" or c2[1] == "C") or
                 c1[1] == "H" and (c2[1] == "S" or c2[1] == "C")) and 
                order in ranks)

    # draw_cards : bool
    # Draw cards from deck and hold face up as long as there are cards left
    # returns True if the move is successful, False if the game is over
    def draw_cards(self):
        # if deck is empty, the face-up stack becomes the deck again
        length = len(self.deck.cards)
        if length == 0:
            if self.is_over():
                print "There are no more moves. Thanks for playing!"
                return False
            elif self.is_winnable():
                print "The game is winnable! Nice going!"
                return True
            else:
                self.moves = []
                self.deck.cards = list(reversed(self.draw)) # turn over the deck!
                self.draw = []
                self.hint = []
                return True
        else:
            # Draw up to three new cards, depending on how many are left
            if length >= 3:
                cards_to_draw = 3
            else:
                cards_to_draw = length
        for card in range(cards_to_draw):
            self.draw.append(self.deck.draw())

        # Detect if new board state has valid moves; update hint
        self.check_possible_moves()
        return True

    # parse_move : move move bool -> bool
    # Parses user input, and if legal, moves card(s) from m1 to m2
    # Argue with True to execute moves, argue with False to return move validity
    def parse_move(self, m1, m2, to_be_run):

        # Parse source
        if m1[0] in "1234567":
            try:
                c1_col = int(m1[0]) - 1
                c1_row = int(m1[1:]) # Take rest of string to grab double digits
                c1 = self.columns[c1_col][c1_row]
            except IndexError:
                if to_be_run: print "That's not a valid coordinate. Try again."
                return False
            except ValueError:
                if to_be_run: print "That's not a valid coordinate. Try again."
                return False
            if (len(self.columns[c1_col]) - c1_row) > self.faceup[c1_col]:
                if to_be_run: print "That card isn't uncovered yet. Try again."
                return False
            source = "col"

        elif m1 == "DC":
            if len(self.draw) == 0:
                if to_be_run: print ("There are no draw cards available." + 
                               " Try again.")
                return False
            c1 = self.draw[-1]
            source = "draw"

        elif m1[0] == "A":
            c1 = self.stacks[int(m1[1]) - 1][-1]
            c1_stack = int(m1[1]) - 1
            source = "accum"
        else:
            if to_be_run: print "That's not a valid coordinate. Try again."
            return False

        # Parse destination
        if m2[0] in "1234567":
            try:
                c2_col = int(m2[0]) - 1
                c2_row = int(m2[1:]) - 1
                c2 = self.columns[c2_col][c2_row]
            except IndexError:
                if to_be_run: print "That's not a valid coordinate. Try again."
                return False
            except ValueError:
                if to_be_run: print "That's not a valid coordinate. Try again."
                return False
            if (len(self.columns[c2_col]) - c2_row) > self.faceup[c2_col]:
                if to_be_run: print "That's not a valid coordinate. Try again."
                return False
            # Ensure destination is the bottom of the stack
            if c2_row != len(self.columns[c2_col]) - 1:
                if to_be_run: print "That's not a valid coordinate. Try again."
                return False
            dest = "col"

        elif m2[0] == "A":
            c2 = self.stacks[int(m2[1]) - 1][-1]
            c2_stack = int(m2[1]) - 1
            dest = "accum"
        else:
            if to_be_run: print "Your destination isn't valid. Try again."
            return False

        # Deal with each possible movement case

        if source == "col" and dest == "col":
            result = self.move_col_to_col(c1, c2, m1, m2, c1_col, c1_row, 
                                        c2_col, c2_row, to_be_run)
        elif source == "col" and dest == "accum":
            result = self.move_col_to_accum(c1, c2, c1_col, c2_stack, to_be_run)
        elif source == "draw" and dest == "col":
            result = self.move_draw_to_col(c1, c2, c2_col, to_be_run)
        elif source == "draw" and dest == "accum":
            result = self.move_draw_to_accum(c1, c2, c2_stack, to_be_run)
        elif source == "accum" and dest == "col":
            result = self.move_accum_to_col(c1, c2, c1_stack, c2_col, to_be_run)
        else:
            print "You can't move from there to there. Try again."
            return False

        return result

    # move_col_to_col : card card move move pos pos pos bool -> bool
    # If legal, moves c1 to c2
    def move_col_to_col(self, c1, c2, m1, m2, c1_col, c1_row, 
                        c2_col, c2_row, to_be_run):
        if self.can_stack_down(c1, c2):
            if not to_be_run: return True

            # Add this move to the lateral move list
            move = m1 + " " + m2
            self.lateral_list[move] = 1

            # Find how many cards will be moved
            num_cards = len(self.columns[c1_col]) - c1_row
            moving = []
            # Shuffle them from one stack to the other
            for card in range(num_cards):
                moving.append(self.columns[c1_col].pop())
                self.faceup[c1_col] -= 1
                if self.faceup[c1_col] == 0: self.faceup[c1_col] = 1
            for card in range(num_cards):
                self.columns[c2_col].append(moving.pop())
                self.faceup[c2_col] += 1
            self.check_possible_moves()
            return True
        else:
            if to_be_run: print "That card can't go there. Try again."
            return False

    # move_col_to_accum : card card pos pos bool -> bool
    # If legal, moves c1 to c2
    def move_col_to_accum(self, c1, c2, c1_col, c2_stack, to_be_run):
        if self.can_stack_up(c1, c2):
            if not to_be_run: return True
            moving = self.columns[c1_col].pop()
            self.stacks[c2_stack].append(moving)
            self.faceup[c1_col] -= 1
            if self.faceup[c1_col] == 0: self.faceup[c1_col] = 1
            self.check_possible_moves()
            return True
        else:
            if to_be_run: print "That card can't go there. Try again."
            return False

    # move_draw_to_col : card card pos bool -> bool
    # If legal, moves c1 to c2
    def move_draw_to_col(self, c1, c2, c2_col, to_be_run):
        if self.can_stack_down(c1, c2):
            if not to_be_run: return True
            moving = self.draw.pop()
            self.columns[c2_col].append(moving)
            self.faceup[c2_col] += 1
            self.check_possible_moves()
            return True
        else:
            if to_be_run: print "That card can't go there. Try again."
            return False

    # move_draw_to_accum : card card pos bool -> bool
    # If legal, moves c1 to c2
    def move_draw_to_accum(self, c1, c2, c2_stack, to_be_run):
        if self.can_stack_up(c1, c2):
            if not to_be_run: return True
            moving = self.draw.pop()
            self.stacks[c2_stack].append(moving)
            self.check_possible_moves()
            return True
        else:
            if to_be_run: print "That card can't go there. Try again."
            return False

    # move_accum_to_col : card card pos pos bool -> bool
    # If legal, moves c1 to c2
    def move_accum_to_col(self, c1, c2, c1_stack, c2_col, to_be_run):
        if self.can_stack_down(c1, c2):
            if not to_be_run: return True
            moving = self.stacks[c1_stack].pop()
            self.columns[c2_col].append(moving)
            self.faceup[c2_col] += 1
            self.check_possible_moves()
            return True
        else:
            if to_be_run: print "That card can't go there. Try again."
            return False
 
    # is_won : bool
    # Return whether or not the game is completely finished
    def is_won(self):
        for stack in self.stacks:
            if len(stack) != 14: return False
        return True

    # check_possible_moves : void
    # Update move possibility list for current game state
    def check_possible_moves(self):

        # Try moving the draw card to every position
        for col in range(1, 8):
            row = str(len(self.columns[col - 1]))
            dest = str(col) + row
            source = "DC"
            if self.parse_move(source, dest, False):
                self.update_hint([source, dest])
                return

        # Try moving the draw card to every stack
        for stack in range(1, 5):
                source = "DC"
                dest = "A" + str(stack)
                if self.parse_move(source, dest, False):
                    self.update_hint([source, dest])
                    return

        # Try moving every top card to every stack
        for col in range(1, 8):
            source = str(col) + str(len(self.columns[col - 1]) - 1)
            for stack in range(1, 5):
                dest = "A" + str(stack)
                if self.parse_move(source, dest, False):
                    self.update_hint([source, dest])
                    return

        # Try moving every column to every other column
        # These are lateral movements and should be checked last
        for col in range(1, 8):
            for row in range(1,20):
                for destcol in range(1, 8):
                    source = str(col) + str(row)
                    dest = (str(destcol) + 
                            str(len(self.columns[destcol - 1])))
                    if source[0] == dest[0]: continue # Ignore same column moves
                    if self.parse_move(source, dest, False):
                        # ensure the move is unique before adding it
                        move = source + " " + dest
                        # Don't bother with moving K-anchored stacks col->col
                        if not (source[1:] == "1" and dest[1:] == "1"):
                            if not self.lateral_list.has_key(move):
                                self.update_hint([source, dest])
                                return

        # No new move/hint was found
        self.hint = []
        self.moves.append(False)

    # update_hint : hint -> void
    # Overwrites hint and adds a True (playable) state to the move list
    def update_hint(self, newhint):
        self.hint = newhint
        self.moves.append(True)

    # is_over : bool
    # Check to see if there were no possible moves for every deck state
    def is_over(self):
        if not self.is_winnable():
            return all(x == False for x in self.moves)
        return False

    # is_winnable : bool
    # Checks if game is winnable (deck is empty and no cards are left unturned)
    def is_winnable(self):
        if self.deck.cards != []: return False
        if self.draw       != []: return False
        # Check that all cards are face up
        for x in range(7):
            if self.faceup[x] < (len(self.columns[x]) - 1): return False
        return True

    # show_hint : void
    # Prints most recent possible move to screen
    def show_hint(self):
        if len(self.hint) == 0: 
            print "No hint available! Try drawing more cards."
        else: sys.stdout.write("Hint: " + self.hint[0] + " --> " + 
                               self.hint[1] + "\n")

    # undo : void
    # Replaces object data with that of the previous game state
    def undo(self):
        if not self.can_undo:
            print "Sorry, you can only undo the most recent move."
            return
        self.deck = self.prev.deck
        self.columns = self.prev.columns
        self.faceup = self.prev.faceup
        self.draw = self.prev.draw
        self.stacks = self.prev.stacks
        self.hint = self.prev.hint
        self.move = self.prev.moves
        self.lateral_list = self.prev.lateral_list
        print "Undid previous move."
        self.can_undo = False

    # backup : void
    # Backs up current game state for undo feature
    def backup(self):
        self.prev = copy.deepcopy(self)
        self.can_undo = True

    # get_input : input -> bool
    # Parses user input and executes command
    def get_input(self, move):
        if (len(move) != 2) or (len(move[0]) < 2) or (len(move[1]) < 2):
            print "That's not a valid move. Try again."
            return False
        else:
            self.backup()
            self.parse_move(move[0].upper(), move[1].upper(), True)

    def print_intro(self):
        print ("\n\n\nWelcome to Solitaire!\n" + 
               "To move cards, enter two coordinates: a source and a destination.\n" +
               "A coordinate is either two numbers without a space, or a letter code.\n" +
               "For the letter codes shown below, case does not matter.\n" + 
               "Columns are addressed first with numbers 1-7,\n" + 
               "then rows are addressed with numbers 1-19.\n" 
               + "Accumulation piles are addressed as A1, A2, A3 and A4.\n" +
               "To draw new cards from the deck, type D.\n" + 
               "To access the top card of the draw pile, address as DC.\n" + 
               'Some example moves: "11 22", "DC 54", "32 A3", "719 111".\n' + 
               'You can undo your previous move by typing "undo".\n' + 
               'Type "hint" or "h" to see a possible move, which is helpful when stuck.\n'
               + 'Type "help" if you want to see this again or "q" to quit. Have fun!\n\n')

    # play : bool
    # Input loop to play game, returns whether or not the game was won
    def play(self):
        self.print_intro()
        while True:
            self.printboard()
            ans = raw_input("Enter a move: ")
            if ans in ["Q", "q", "quit", "exit"]: 
                exit(1)
            elif ans in ["d", "D", "draw", "Draw", "DRAW"]: 
                self.backup()
                if not self.draw_cards():
                    return False
            elif ans in ["hint", "Hint", "HINT", "h", "H"]:
                self.show_hint()
            elif ans in ["u", "undo", "UNDO", "Undo"]:
                self.undo()
            elif ans in ["help", "Help", "HELP"]:
                self.print_intro()
            else:
                self.get_input(ans.split())
                if self.is_won():
                    self.printboard()
                    print "You've won! Thanks for playing!"
                    return True
        print "Thanks for playing!"
        return