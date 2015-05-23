# Alex King
# Deck.py - Deck of cards in Python
# 5/22/15

# Purpose of this file: Create a deck of cards in a random shuffled order

import random

# A Deck represents a stack of 52 face down standard playing cards.

class Deck:
        def __init__(self):
                self.cards = []
                for suit in "SHCD":
                        for rank in "A23456789TJQK":
                                card = rank + suit
                                self.cards.append(card)
                random.shuffle(self.cards)
        def draw(self):
                return self.cards.pop()