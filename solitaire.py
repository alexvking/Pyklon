# Alex King
# solitaire.py

from Deck import Deck
import sys

# Klondike Solitaire is represented by an object with several structures that keep
# track of cards. Cards are represented as pure strings; "2C" is the 2 of clubs.
# All are kept to be two characters, so 10 is represented as T. 

# The Solitaire class holds several structures to track card positions
class Solitaire:
    def __init__(self):
        self.deck = Deck() # grab a shuffled deck of cards
        self.columns = [["ZZ"], ["ZZ"], ["ZZ"], ["ZZ"], 
                ["ZZ"], ["ZZ"], ["ZZ"]] # empty sentinel
        self.faceup = [1, 1, 1, 1, 1, 1, 1] # beginning configuration
        self.draw = [] # To begin, no cards are face up
        self.stacks = [["ZZ"], ["ZZ"], ["ZZ"], ["ZZ"]] # empty stacks

        # Deal a new game
        for i in range(7):
            self.columns.append([])
            for j in range (i + 1):
                self.columns[i].append(self.deck.draw())

    # Prints board layout in traditional Klondike style
    def printvert(self):
        # Top row: Draw cards and accumulation piles
        if len(self.deck.cards) > 0:
            sys.stdout.write("[.]")
        else:
            sys.stdout.write("[ ]")
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
                sys.stdout.write("[]")
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
                        sys.stdout.write("XX") # face down

                    sys.stdout.write("  ")
                else:
                    sys.stdout.write("    ")
            sys.stdout.write("\n")
        sys.stdout.write("\n")


    # Returns whether c1 can be placed on top of c2 in an accumulation pile
    def can_stack_up(self, c1, c2):
        # print("Checking: ", c1, c2)
        ranks = "A23456789TJQK"
        order = c2[0] + c1[0] # e.g. "28", "JQ", "43"

        if c2[0] == "Z" and c1[0] == "A": 
            return True # base case

        # Check for sequential order and same suit
        else:
            return c1[1] == c2[1] and order in ranks

    # Returns whether a card can be added to the bottom of a column
    def can_stack_down(self, c1, c2):
        print("Checking: ", c1, c2)
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

    # Draw cards from deck and hold face up as long as there are cards left
    def draw_cards(self):
        # if deck is empty, the face-up stack becomes the deck again
        length = len(self.deck.cards)
        if length == 0:
            self.deck.cards = self.draw
            self.draw = []
            return
        else:
            # Draw up to three new cards, depending on how many are left
            if length >= 3:
                cards_to_draw = 3
            else:
                cards_to_draw = length
        for card in range(cards_to_draw):
            self.draw.append(self.deck.draw())

    # Parses user input, and if legal, moves card(s) from m1 to m2
    def move_cards(self, m1, m2):
        # Convert each move to a card representation
        if m1[0] in "1234567":
            try:
                c1_col = int(m1[0]) - 1
                c1_row = m1[1]
                if   c1_row == "T": c1_row = 10
                elif c1_row == "E": c1_row = 11
                elif c1_row == "W": c1_row = 12
                c1_row = int(c1_row)
                c1 = self.columns[int(m1[0]) - 1][int(m1[1])]
            except IndexError:
                print "That's not a valid coordinate. Try again."
                return
            source = "col"

        elif m1 == "DC":
            if len(self.draw) == 0:
                print "There are no draw cards available. Try again."
                return
            c1 = self.draw[-1]
            source = "draw"

        elif m1[0] == "A":
            c1 = self.stacks[int(m1[1]) - 1][-1]
            c1_stack = int(m1[1]) - 1
            source = "accum"

        if m2[0] in "1234567":
            try:
                c2_col = int(m2[0]) - 1
                c2_row = int(m2[1])
                if   c2_row == "T": c2_row = 10
                elif c2_row == "E": c2_row = 11
                elif c2_row == "W": c2_row = 12
                c2_row = int(c2_row)
                c2 = self.columns[int(m2[0]) - 1][int(m2[1])]
            except IndexError:
                print "That's not a valid coordinate. Try again."
                return
            dest = "col"

        elif m2 == "DC":
            if len(self.draw) == 0:
                print "There are no draw cards available. Try again."
                return
            c2 = self.draw[-1]
            dest = "draw"

        elif m2[0] == "A":
            c2 = self.stacks[int(m2[1]) - 1][-1]
            c2_stack = int(m2[1]) - 1
            dest = "accum"
        else:
            print "Your destination isn't valid. Try again."
            return

        # Deal with each possible movement case

        if source == "col" and dest == "col":
            if self.can_stack_down(c1, c2):
                num_cards = len(self.columns[c1_col]) - c1_row
                moving = []
                for card in range(num_cards):
                    moving.append(self.columns[c1_col].pop())
                    self.faceup[c1_col] -= 1
                    if self.faceup[c1_col] == 0: self.faceup[c1_col] = 1
                for card in range(num_cards):
                    self.columns[c2_col].append(moving.pop())
                    self.faceup[c2_col] += 1
                return
            else:
                print "That card can't go there. Try again."

        elif source == "col" and dest == "accum":
            if self.can_stack_up(c1, c2):
                moving = self.columns[c1_col].pop()
                self.stacks[c2_stack].append(moving)
                self.faceup[c1_col] -= 1
                if self.faceup[c1_col] == 0: self.faceup[c1_col] = 1
                return
            else:
                print "That card can't go there. Try again."

        elif source == "draw" and dest == "col":
            if self.can_stack_down(c1, c2):
                moving = self.draw.pop()
                self.columns[c2_col].append(moving)
                self.faceup[c2_col] += 1
                return
            else:
                print "That card can't go there. Try again."

        elif source == "draw" and dest == "accum":
            if self.can_stack_up(c1, c2):
                moving = self.draw.pop()
                self.stacks[c2_stack].append(moving)
                return
            else:
                print "That card can't go there. Try again."

        elif source == "accum" and dest == "col":
            if self.can_stack_down(c1, c2):
                moving = self.stacks[c1_stack].pop()
                self.columns[c2_col].append(moving)
                self.faceup[c2_col] += 1
                return
            else:
                print "That card can't go there. Try again."
        else:
            print "You can't move from there to there. Try again."
            return
        return

    # Input loop to play game
    def play(self):
        sys.stdout.write("\n\n\n")
        print "Welcome to Solitaire! To play, enter two coordinates: a source and a destination."
        print "Columns are addressed first, 1-7, then rows are addressed 1-9, then T, E, and W for 10, 11 and 12."
        print "Accumulation piles are addressed as A1-A4."
        print "To draw new cards from the deck, type d or D."
        print "To access the top card of the draw pile, address as DC."
        print 'Some legal moves: "11 22", "DC 54", "32 A3". Type help if you want to see this again.' 
        print 'Have fun!\n\n'
        while True:
            self.printvert()
            ans = raw_input("Enter a move: ")
            if   ans in ["Q", "q", "quit", "exit"]: 
                exit(1)
            elif ans in ["d", "D"]: 
                self.draw_cards()
            elif ans in ["help", "h", "Help"]:
                self.play()
            else:
                move = ans.split()
                if len(move) != 2:
                    print "That's not a valid move. Try again."
                    continue
                else:
                    self.move_cards(move[0], move[1])
        print "Thanks for playing!"
        return