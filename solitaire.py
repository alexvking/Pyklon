# Alex King
# solitaire.py

from Deck import Deck
import sys

# The Solitaire class holds several structures to track card positions

# deck: An object containing an array of cards
# columns: A list of lists, modeling each column of the game board
# faceup: A list corresponding to each column representing how many cards are 
#  face up
# draw: A list tracking all cards that are face up in the draw pile.
# stacks: A list of lists tracking cards in the accumulation piles.
# hints: A list of pairs of sources and destinations
# moves: An accumulating list of booleans that tracks whether or not there is
#  a legal move on each draw of the deck. If all False when the deck is emptied,
#  the game is over.

class Solitaire:
    # Initializes all member variables and sets the game board
    def __init__(self):
        self.deck = Deck() # grab a shuffled deck of cards
        self.columns = [["ZZ"], ["ZZ"], ["ZZ"], ["ZZ"], 
                ["ZZ"], ["ZZ"], ["ZZ"]] # empty sentinel
        self.faceup = [1, 1, 1, 1, 1, 1, 1] # beginning configuration
        self.draw = [] # To begin, no cards are face up
        self.stacks = [["ZZ"], ["ZZ"], ["ZZ"], ["ZZ"]] # empty stacks
        self.hint = [] # No hint to start
        # self.prevhint = []
        self.moves = [] # boolean representing possibility of valid moves for every draw

        # Deal a new game
        for i in range(7):
            self.columns.append([])
            for j in range (i + 1):
                self.columns[i].append(self.deck.draw())

    # Prints board layout in traditional Klondike style
    def printboard(self):
        # Top row: Draw cards and accumulation piles
        if len(self.deck.cards) > 0:
            sys.stdout.write("\n[.]") # cards remain
        else:
            sys.stdout.write("[ ]") # deck is empty
        sys.stdout.write(" ")

        # Print up to three drawn cards
        for i in range(-3, 0):
            if len(self.draw) >= (i * -1): # To print *last three* of the array
                sys.stdout.write(self.draw[i])
            else: 
                sys.stdout.write("  ")
            sys.stdout.write(" ")
        sys.stdout.write("  ")

        # Print accumulation piles
        for stack in self.stacks:
            if len(stack) > 1:
                sys.stdout.write(stack[-1]) # show only the top card
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
                        sys.stdout.write(self.columns[col][row])
                    else:
                        sys.stdout.write("[]") # face down

                    sys.stdout.write("  ")
                else:
                    sys.stdout.write("    ")
            sys.stdout.write("     " + str(row)) # number each row
            sys.stdout.write("\n")
        sys.stdout.write("\n")

    # Returns whether c1 can be placed on top of c2 in an accumulation pile
    def can_stack_up(self, c1, c2):
        ranks = "A23456789TJQK"
        order = c2[0] + c1[0] # e.g. "28", "JQ", "43"

        if c2[0] == "Z" and c1[0] == "A": 
            return True # base case

        # Check for sequential order and same suit
        else:
            return c1[1] == c2[1] and order in ranks

    # Returns whether a card can be added to the bottom of a column
    def can_stack_down(self, c1, c2):
        ranks = "A23456789TJQK"
        order = c1[0] + c2[0] # e.g. "28", "JQ", "43"

        if c2[0] == "Z" and c1[0] == "K": 
            print "you found a Z"
            return True # base case

        # Check order and suit
        return ((c1[1] == "S" and (c2[1] == "D" or c2[1] == "H") or
                 c1[1] == "C" and (c2[1] == "D" or c2[1] == "H") or
                 c1[1] == "D" and (c2[1] == "S" or c2[1] == "C") or
                 c1[1] == "H" and (c2[1] == "S" or c2[1] == "C")) and 
                order in ranks)

    # Draw cards from deck and hold face up as long as there are cards left
    def draw_cards(self):
        # if deck is empty, the face-up stack becomes the deck again
        length = len(self.deck.cards)
        if length == 0:
            if self.is_over():
                print "There are no more moves. Thanks for playing!"
                exit(1)
            else:
                self.moves = []
            self.deck.cards = list(reversed(self.draw)) # turn over the deck!
            self.draw = []
            self.hint = []
            return
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
        return

    # Parses user input, and if legal, moves card(s) from m1 to m2
    # Argue with True to execute moves, argue with False to return move validity
    def move_cards(self, m1, m2, to_be_run):

        # Convert each move to a card representation
        if m1[0] in "1234567":
            try:
                c1_col = int(m1[0]) - 1
                c1_row = int(m1[1:]) # Take rest of string to grab double digits
                c1 = self.columns[c1_col][c1_row]
            except IndexError:
                if to_be_run: print "That's not a valid coordinate. Try again."
                return False
            if (len(self.columns[c1_col]) - c1_row) > self.faceup[c1_col]:
                if to_be_run: print "That card isn't uncovered yet. Try again."
                return False
            source = "col"

        elif m1 == "DC":
            if len(self.draw) == 0:
                if to_be_run: print ("There are no draw cards available." + 
                               "Try again.")
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

        if m2[0] in "1234567":
            try:
                c2_col = int(m2[0]) - 1
                c2_row = int(m2[1:]) - 1
                c2 = self.columns[c2_col][c2_row]
            except IndexError:
                if to_be_run: print "That's not a valid coordinate. Try again."
                return False
            if (len(self.columns[c2_col]) - c2_row) > self.faceup[c2_col]:
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
            if self.can_stack_down(c1, c2):
                if not to_be_run: return True
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
            else:
                if to_be_run: print "That card can't go there. Try again."
                return False

        elif source == "col" and dest == "accum":
            if self.can_stack_up(c1, c2):
                if not to_be_run: return True
                moving = self.columns[c1_col].pop()
                self.stacks[c2_stack].append(moving)
                self.faceup[c1_col] -= 1
                if self.faceup[c1_col] == 0: self.faceup[c1_col] = 1
            else:
                if to_be_run: print "That card can't go there. Try again."
                return False

        elif source == "draw" and dest == "col":
            if self.can_stack_down(c1, c2):
                if not to_be_run: return True
                moving = self.draw.pop()
                self.columns[c2_col].append(moving)
                self.faceup[c2_col] += 1
            else:
                if to_be_run: print "That card can't go there. Try again."
                return False

        elif source == "draw" and dest == "accum":
            if self.can_stack_up(c1, c2):
                if not to_be_run: return True
                moving = self.draw.pop()
                self.stacks[c2_stack].append(moving)
            else:
                if to_be_run: print "That card can't go there. Try again."
                return False

        elif source == "accum" and dest == "col":
            if self.can_stack_down(c1, c2):
                if not to_be_run: return True
                moving = self.stacks[c1_stack].pop()
                self.columns[c2_col].append(moving)
                self.faceup[c2_col] += 1
            else:
                if to_be_run: print "That card can't go there. Try again."
                return False
        else:
            print "You can't move from there to there. Try again."
            return False

        # Regenerate possible moves and hint
        # self.moves.append(False) # Hacky way of denoting a real move
        self.check_possible_moves()
        # print self.moves
        return True

    # Return whether or not the game is completely finished
    def is_won(self):
        for stack in self.stacks:
            if len(stack) != 13: return False
        return True

    # Update move possibility list for current game state
    def check_possible_moves(self):

        # Try moving the draw card to every position
        for col in range(1, 8):
            row = str(len(self.columns[col - 1]))
            dest = str(col) + row
            source = "DC"
            if self.move_cards(source, dest, False):
                self.update_hints([source, dest])
                return

        # Try moving the draw card to every stack
        for stack in range(1, 5):
                source = "DC"
                dest = "A" + str(stack)
                if self.move_cards(source, dest, False):
                    self.update_hints([source, dest])
                    return

        # Try moving every top card to every stack
        for col in range(1, 8):
            source = str(col) + str(len(self.columns[col - 1]) - 1)
            for stack in range(1, 5):
                dest = "A" + str(stack)
                if self.move_cards(source, dest, False):
                    self.update_hints([source, dest])
                    return

        # Try moving every column to every other column
        # These are lateral movements and should be checked last
        for col in range(1, 8):
            for row in range(1,20):
                for destcol in range(1, 8):
                    source = str(col) + str(row)
                    dest = (str(destcol) + 
                            str(len(self.columns[destcol - 1])))
                    # dest = str(col) + str(row)
                    if source[0] == dest[0]: continue # Ignore same column moves
                    if self.move_cards(source, dest, False):
                        # print(source, dest)
                        self.update_hints([source, dest])
                        return

        # No new move/hint was found
        self.hint = []
        self.moves.append(False)

    # Updates list of hints, previous hint, and checks for circularity
    def update_hints(self, newhint):
        # if self.hint != []: self.prevhint = self.hint[-1]
        self.hint = newhint
        self.moves.append(True)


    # Check to see if there were no possible moves for every deck state
    def is_over(self):
        # num_cards = len(self.deck.cards) + len(self.draw)
        # if num_cards > 0:
        return all(x == False for x in self.moves)
            # Stuck in a circular state

            # Check for circularity
            
        #     iterations = num_cards / 3
        #     print(num_cards, iterations)

        #     if len(self.hint) >= iterations and all(x == True for x in self.moves):
        #         latest = self.hint[-1]
        #         for x in range(-1, ((iterations - 1) * -2), -2):
        #             print x
        #             if self.hint[(-x) + (2 * x)] != latest:
        #                 return False
        #         return True
        #     return False
        # return False

    # Checks if game is winnable (deck is empty and no cards are left unturned)
    def is_winnable(self):
        if self.deck.cards != []: return False
        if self.draw       != []: return False
        # Check that faceup count matches length - 1
        for x in range(7):
            if self.faceup[x] != (len(self.columns[x]) - 1): return False
        return True

    # Prints most recent possible move to screen
    def show_hint(self):
        print self.hint
        if len(self.hint) == 0: 
            print "No hint available! Try drawing more cards."
        else: sys.stdout.write("Hint: " + self.hint[0] + " --> " + 
                                   self.hint[1] + "\n")

    # Input loop to play game
    def play(self):
        sys.stdout.write("\n\n\n")
        print "Welcome to Solitaire!"
        print "To play, enter two coordinates: a source and a destination."
        print "Columns are addressed first, 1-7, then rows are addressed 1-19."
        print "Accumulation piles are addressed as A1-A4."
        print "To draw new cards from the deck, type d or D."
        print "To access the top card of the draw pile, address as DC."
        print 'Some example moves: "11 22", "DC 54", "32 A3", "719 111".'
        print "You can type 'hint' or 'h' if you want to see a possible move." 
        print 'Type "help" if you want to see this again. Have fun!\n\n'
        while True:
            self.printboard()
            ans = raw_input("Enter a move: ")
            if   ans in ["Q", "q", "quit", "exit"]: 
                exit(1)
            elif ans in ["d", "D", "draw", "Draw", "DRAW"]: 
                self.draw_cards()
            elif ans in ["hint", "Hint", "HINT", "h", "H"]:
                self.show_hint()
            elif ans in ["help", "Help", "HELP"]:
                self.play()
            else:
                move = ans.split()
                if len(move) != 2:
                    print "That's not a valid move. Try again."
                    continue
                else:
                    self.move_cards(move[0], move[1], True)
                    if self.is_won():
                        print "You've won! Thanks for playing!"
                        exit(1)
                    elif self.is_winnable():
                        print "The game is winnable! Nice going!"

        print "Thanks for playing!"
        return