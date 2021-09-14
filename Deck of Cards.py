import random


class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def show(self):
        print(f"{self.value} of {self.suit}")

    def array(self):
        return f"{self.value} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in range(1,14):
                self.cards.append(Card(s, v))

    def show(self):
        for c in self.cards:
            c.show()

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self):
        return self.cards.pop()
        pass


class Board:
    def __init__(self):
        self.hand = []

    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self

    def showHand(self):
        for card in self.hand:
            card.show()


deck = Deck()
deck.shuffle()

c1 = Board()
c2 = Board()
c3 = Board()
c4 = Board()
c5 = Board()
c6 = Board()
c7 = Board()


def deal():
    c1.draw(deck)
    c2.draw(deck)
    c3.draw(deck)
    c4.draw(deck)
    c5.draw(deck)
    c6.draw(deck)
    c7.draw(deck)

    c2.draw(deck)
    c3.draw(deck)
    c4.draw(deck)
    c5.draw(deck)
    c6.draw(deck)
    c7.draw(deck)

    c3.draw(deck)
    c4.draw(deck)
    c5.draw(deck)
    c6.draw(deck)
    c7.draw(deck)

    c4.draw(deck)
    c5.draw(deck)
    c6.draw(deck)
    c7.draw(deck)

    c5.draw(deck)
    c6.draw(deck)
    c7.draw(deck)

    c6.draw(deck)
    c7.draw(deck)

    c7.draw(deck)


deal()

c7.showHand()
print(f"Column 7: {c7.hand[0].array()}")

