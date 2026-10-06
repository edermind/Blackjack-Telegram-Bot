
import random

SUITS = ["♥", "♦", "♣", "♠"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


WEIGHTS = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11,
}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit            # масть
        self.rank = rank            # фигура
        self.weight = WEIGHTS[rank] # вес 

    def __str__(self):
        return self.rank + self.suit


class Deck:
    def __init__(self, decks_count=6):
        self.cards = []
        for _ in range(decks_count):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(suit, rank))
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def total(self):
        total = 0
        aces = 0
        for card in self.cards:
            total += card.weight
            if card.rank == "A":
                aces += 1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self):
        return len(self.cards) == 2 and self.total() == 21

    def is_bust(self):
        return self.total() > 21

    def __str__(self):
        return " ".join(str(card) for card in self.cards)
