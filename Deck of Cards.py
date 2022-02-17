"""
Created by Matthew DiMaggio
01 January 2022
Game of "Golf"
----
In Golf, a player is dealt 9 cards, which they layout in a 3x3 grid on the table FACE DOWN. Three cards are then
flipped; ONE in EACH COLUMN. Players take turns around the table drawing a card from the main deck or from the discard
pile and choose to replace any card in their grid and discard, or do nothing and discard the drawn card. If a column
has 3 of the same number, the whole column is discarded. The game ends once any player has no face down cards left,
and one additional turn around the table has completed. The value of each card is totaled and added to the players
score (9 rounds are played). The player with the smallest score wins.

Card Values: (ACE - TEN = Face Value)(KING = 0)(JACK, QUEEN = 10)(JOKER = -2)
"""
import random


class GameEnd(Exception):
    pass


class PlayError(Exception):
    pass


class Game:
    player_count = 4


class Card:
    def __init__(self, suit, val, deck_num):
        self.suit = suit
        self.value = val
        self.deck = deck_num

    def show(self):
        print(f"{self.value} of {self.suit} ({self.deck})")

    def array(self):
        return f"{self.value} of {self.suit} ({self.deck})"


class Deck:
    def __init__(self):
        self.cards = []
        self.discard = []
        self.build()

    def build(self):
        for d in range(2):
            for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
                for v in range(1,14):
                    self.cards.append(Card(s, v, d))
            for j in range(2):
                self.cards.append(Card("None", 14, d))

    def show(self):
        for c in self.cards:
            c.show()

    def array(self):
        for c in self.cards:
            c.array()

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self, type):
        if type == "main":
            return self.cards.pop()
        if type == "discard":
            return self.discard.pop()

    def show_discard(self):
        return self.discard[len(self.discard)-1].value


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.c1_up = []
        self.c1_down = []
        self.c2_up = []
        self.c2_down = []
        self.c3_up = []
        self.c3_down = []

    def draw(self, deck, type):
        if type == "main":
            self.hand.append(deck.drawCard("main"))
            return self
        if type == "discard":
            self.hand.append(deck.drawCard("discard"))
            return self

    def showGridUp(self):
        print('******')
        for card in self.c1_up:
            print(f'{self.name} - Column 1: {card.array()}')
        print('')
        for card in self.c2_up:
            print(f'{self.name} - Column 2: {card.array()}')
        print('')
        for card in self.c3_up:
            print(f'{self.name} - Column 3: {card.array()}')
        print('******')
        print('\n')

    def arrayHand(self):
        return self.hand[0].value

    def board_init(self):
        for i in range(len(self.hand) - 1, 0, -1):
            r = random.randint(0, i)
            self.hand[i], self.hand[r] = self.hand[r], self.hand[i]

        self.c1_up.append(self.hand.pop())
        for h in range(2):
            self.c1_down.append(self.hand.pop())
        self.c2_up.append(self.hand.pop())
        for h in range(2):
            self.c2_down.append(self.hand.pop())
        self.c3_up.append(self.hand.pop())
        for h in range(2):
            self.c3_down.append(self.hand.pop())

    def play_turn(self):
        c1 = []
        c2 = []
        c3 = []
        for c in self.c1_up:
            c1.append(c.value)
        for c in self.c2_up:
            c2.append(c.value)
        for c in self.c3_up:
            c3.append(c.value)

        # Check discard for wants
        if (drawpile.show_discard() in c1) or (drawpile.show_discard() in c2) or (drawpile.show_discard() in c3):
            print(f'{self.name} Choice = DISCARD PILE')
            self.hand.append(drawpile.discard.pop())

        # Randomly replace a flipped down card in matching column with drawn discard
            if self.hand[0].value in c1:
                r = random.randint(0, len(self.c1_down) - 1)
                drawpile.discard.append(self.c1_down.pop(r))
                self.c1_up.append(self.hand.pop())
            elif self.hand[0].value in c2:
                r = random.randint(0, len(self.c2_down) - 1)
                drawpile.discard.append(self.c2_down.pop(r))
                self.c2_up.append(self.hand.pop())
            elif self.hand[0].value in c3:
                r = random.randint(0, len(self.c3_down) - 1)
                drawpile.discard.append(self.c3_down.pop(r))
                self.c3_up.append(self.hand.pop())
            else:
                print(f"ERROR: {self.name} TAKE DISCARD ON TURN START")
                raise PlayError

        # Take from standard drawpile
        else:
            # If discard was a joker and not taken, put it into the drawpile to force it into the player's hand
            if drawpile.show_discard() == 14:
                drawpile.cards.append(drawpile.discard.pop())
            print(f'{self.name} Choice = DRAWPILE')
            self.hand.append(drawpile.cards.pop())

            # Decide what to do if a joker is drawn
            if self.hand[0].value == 14:
                print("***JOKER***")

                # Check row 1
                if len(c1) == 1:
                    if self.c1_up[0].value > 4:
                        drawpile.discard.append(self.c1_up[0])
                        self.c1_up[0] = self.hand.pop()
                    else:
                        r = random.randint(0, len(self.c1_down) - 1)
                        drawpile.discard.append(self.c1_down.pop(r))
                        self.c1_up.append(self.hand.pop())
                elif len(c1) == 2:
                    if c1[0] != c1[1]:
                        if c1[0] > c1[1]:
                            drawpile.discard.append(self.c1_up[0])
                            self.c1_up[0] = self.hand.pop()
                        else:
                            drawpile.discard.append(self.c1_up[1])
                            self.c1_up[1] = self.hand.pop()
                    if c1[0] == c1[1] and (len(self.c1_up)+len(self.c2_up)+len(self.c3_up)) >= 7:
                        drawpile.discard.append(self.c1_down.pop())
                        self.c1_up.append(self.hand.pop())
                elif len(c1) == 3:
                    if c1[0] == c1[1] and c1[0] == c1[3]:
                        pass
                    else:
                        if c1[0] > c1[1] and c1[0] > c1[2]:
                            drawpile.discard.append(self.c1_up[0])
                            self.c1_up[0] = self.hand.pop()
                        elif c1[1] > c1[0] and c1[1] > c1[2]:
                            drawpile.discard.append(self.c1_up[1])
                            self.c1_up[1] = self.hand.pop()
                        else:
                            drawpile.discard.append(self.c1_up[2])
                            self.c1_up[2] = self.hand.pop()

                # Check row 2
                elif len(c2) == 1:
                    if self.c2_up[0].value > 4:
                        drawpile.discard.append(self.c2_up[0])
                        self.c2_up[0] = self.hand.pop()
                    else:
                        r = random.randint(0, len(self.c2_down) - 1)
                        drawpile.discard.append(self.c2_down.pop(r))
                        self.c2_up.append(self.hand.pop())
                elif len(c2) == 2:
                    if c2[0] != c2[1]:
                        if c2[0] > c2[1]:
                            drawpile.discard.append(self.c2_up[0])
                            self.c2_up[0] = self.hand.pop()
                        else:
                            drawpile.discard.append(self.c2_up[1])
                            self.c2_up[1] = self.hand.pop()
                    if c2[0] == c2[1] and (len(self.c2_up)+len(self.c2_up)+len(self.c3_up)) >= 7:
                        drawpile.discard.append(self.c2_down.pop())
                        self.c2_up.append(self.hand.pop())
                elif len(c2) == 3:
                    if c2[0] == c2[1] and c2[0] == c2[3]:
                        pass
                    else:
                        if c2[0] > c2[1] and c2[0] > c2[2]:
                            drawpile.discard.append(self.c2_up[0])
                            self.c2_up[0] = self.hand.pop()
                        elif c2[1] > c2[0] and c2[1] > c2[2]:
                            drawpile.discard.append(self.c2_up[1])
                            self.c2_up[1] = self.hand.pop()
                        else:
                            drawpile.discard.append(self.c2_up[2])
                            self.c2_up[2] = self.hand.pop()

                # Check Row 3
                elif len(c3) == 1:
                    if self.c3_up[0].value > 4:
                        drawpile.discard.append(self.c3_up[0])
                        self.c3_up[0] = self.hand.pop()
                    else:
                        r = random.randint(0, len(self.c3_down) - 1)
                        drawpile.discard.append(self.c3_down.pop(r))
                        self.c3_up.append(self.hand.pop())
                elif len(c3) == 2:
                    if c3[0] != c3[1]:
                        if c3[0] > c3[1]:
                            drawpile.discard.append(self.c3_up[0])
                            self.c3_up[0] = self.hand.pop()
                        else:
                            drawpile.discard.append(self.c3_up[1])
                            self.c3_up[1] = self.hand.pop()
                    if c3[0] == c3[1] and (len(self.c3_up)+len(self.c2_up)+len(self.c3_up)) >= 7:
                        drawpile.discard.append(self.c3_down.pop())
                        self.c3_up.append(self.hand.pop())
                elif len(c3) == 3:
                    if c3[0] == c3[1] and c3[0] == c3[3]:
                        pass
                    else:
                        if c3[0] > c3[1] and c3[0] > c3[2]:
                            drawpile.discard.append(self.c3_up[0])
                            self.c3_up[0] = self.hand.pop()
                        elif c3[1] > c3[0] and c3[1] > c3[2]:
                            drawpile.discard.append(self.c3_up[1])
                            self.c3_up[1] = self.hand.pop()
                        else:
                            drawpile.discard.append(self.c3_up[2])
                            self.c3_up[2] = self.hand.pop()

                else:
                    drawpile.discard.append(self.hand.pop())

            # Decide what to do if a card less than or equal to 4 is drawn
            elif self.hand[0].value <= 4:
                print(f'***LESS THAN FOUR***')

                # Check row 1
                # If there is only 1 card face-up...
                if len(c1) == 1:
                    if self.c1_up[0].value == self.hand[0].value:
                        r = random.randint(0, len(self.c1_down) - 1)
                        drawpile.discard.append(self.c1_down.pop(r))
                        self.c1_up.append(self.hand.pop())
                    elif self.c1_up[0].value > 4:
                        drawpile.discard.append(self.c1_up[0])
                        self.c1_up[0] = self.hand.pop()
                    else:
                        r = random.randint(0, len(self.c1_down) - 1)
                        drawpile.discard.append(self.c1_down.pop(r))
                        self.c1_up.append(self.hand.pop())
                # if there is 2 cards face-up...
                elif len(c1) == 2:
                    if c1[0] != c1[1]:
                        if c1[0] > c1[1] and c1[0] > 4:
                            drawpile.discard.append(self.c1_up[0])
                            self.c1_up[0] = self.hand.pop()
                        elif c1[0] < c1[1] and c1[1] > 4:
                            drawpile.discard.append(self.c1_up[1])
                            self.c1_up[1] = self.hand.pop()
                        else:
                            drawpile.discard.append(self.c1_down.pop())
                            self.c1_up.append(self.hand.pop())
                    elif c1[0] == c1[1] and c1[0] == self.hand[0].value:
                        drawpile.discard.append(self.c1_down.pop())
                        self.c1_up.append(self.hand.pop())
                # if there are 3 cards face-up...
                elif len(c1) == 3:
                    if c1[0] == c1[1] and c1[0] == c1[3]:
                        pass
                    else:
                        if c1[0] > c1[1] and c1[0] > c1[2] and c1[0] > self.hand[0].value:
                            drawpile.discard.append(self.c1_up[0])
                            self.c1_up[0] = self.hand.pop()
                        elif c1[1] > c1[0] and c1[1] > c1[2] and c1[1] > self.hand[0].value:
                            drawpile.discard.append(self.c1_up[1])
                            self.c1_up[1] = self.hand.pop()
                        elif c1[2] > c1[0] and c1[2] > c1[1] and c1[2] > self.hand[0].value:
                            drawpile.discard.append(self.c1_up[2])
                            self.c1_up[2] = self.hand.pop()

                # Check row 2
                # If there is only 1 card face-up...
                elif len(c2) == 1:
                    if self.c2_up[0].value == self.hand[0].value:
                        r = random.randint(0, len(self.c2_down) - 1)
                        drawpile.discard.append(self.c2_down.pop(r))
                        self.c2_up.append(self.hand.pop())
                    elif self.c2_up[0].value > 4:
                        drawpile.discard.append(self.c2_up[0])
                        self.c2_up[0] = self.hand.pop()
                    else:
                        r = random.randint(0, len(self.c2_down) - 1)
                        drawpile.discard.append(self.c2_down.pop(r))
                        self.c2_up.append(self.hand.pop())
                # if there is 2 cards face-up...
                elif len(c2) == 2:
                    if c2[0] != c2[1]:
                        if c2[0] > c2[1] and c2[0] > 4:
                            drawpile.discard.append(self.c2_up[0])
                            self.c2_up[0] = self.hand.pop()
                        elif c2[0] < c2[1] and c2[1] > 4:
                            drawpile.discard.append(self.c2_up[1])
                            self.c2_up[1] = self.hand.pop()
                        else:
                            drawpile.discard.append(self.c2_down.pop())
                            self.c2_up.append(self.hand.pop())
                    elif c2[0] == c2[1] and c2[0] == self.hand[0].value:
                        drawpile.discard.append(self.c2_down.pop())
                        self.c2_up.append(self.hand.pop())
                # if there are 3 cards face-up...
                elif len(c2) == 3:
                    if c2[0] == c2[1] and c2[0] == c2[3]:
                        pass
                    else:
                        if c2[0] > c2[1] and c2[0] > c2[2] and c2[0] > self.hand[0].value:
                            drawpile.discard.append(self.c2_up[0])
                            self.c2_up[0] = self.hand.pop()
                        elif c2[1] > c2[0] and c2[1] > c2[2] and c2[1] > self.hand[0].value:
                            drawpile.discard.append(self.c2_up[1])
                            self.c2_up[1] = self.hand.pop()
                        elif c2[2] > c2[0] and c2[2] > c2[1] and c2[2] > self.hand[0].value:
                            drawpile.discard.append(self.c2_up[2])
                            self.c2_up[2] = self.hand.pop()

                # Check Row 3
                # If there is only 1 card face-up...
                elif len(c3) == 1:
                    if self.c3_up[0].value == self.hand[0].value:
                        r = random.randint(0, len(self.c3_down) - 1)
                        drawpile.discard.append(self.c3_down.pop(r))
                        self.c3_up.append(self.hand.pop())
                    elif self.c3_up[0].value > 4:
                        drawpile.discard.append(self.c3_up[0])
                        self.c3_up[0] = self.hand.pop()
                    else:
                        r = random.randint(0, len(self.c3_down) - 1)
                        drawpile.discard.append(self.c3_down.pop(r))
                        self.c3_up.append(self.hand.pop())
                # if there is 2 cards face-up...
                elif len(c3) == 2:
                    if c3[0] != c3[1]:
                        if c3[0] > c3[1] and c3[0] > 4:
                            drawpile.discard.append(self.c3_up[0])
                            self.c3_up[0] = self.hand.pop()
                        elif c3[0] < c3[1] and c3[1] > 4:
                            drawpile.discard.append(self.c3_up[1])
                            self.c3_up[1] = self.hand.pop()
                        else:
                            drawpile.discard.append(self.c3_down.pop())
                            self.c3_up.append(self.hand.pop())
                    elif c3[0] == c3[1] and c3[0] == self.hand[0].value:
                        drawpile.discard.append(self.c3_down.pop())
                        self.c3_up.append(self.hand.pop())
                # if there are 3 cards face-up...
                elif len(c3) == 3:
                    if c3[0] == c3[1] and c3[0] == c3[3]:
                        pass
                    else:
                        if c3[0] > c3[1] and c3[0] > c3[2] and c3[0] > self.hand[0].value:
                            drawpile.discard.append(self.c3_up[0])
                            self.c3_up[0] = self.hand.pop()
                        elif c3[1] > c3[0] and c3[1] > c3[2] and c3[1] > self.hand[0].value:
                            drawpile.discard.append(self.c3_up[1])
                            self.c3_up[1] = self.hand.pop()
                        elif c3[2] > c3[0] and c3[2] > c3[1] and c3[2] > self.hand[0].value:
                            drawpile.discard.append(self.c3_up[2])
                            self.c3_up[2] = self.hand.pop()

                else:
                    drawpile.discard.append(self.hand.pop())

            # Decide what to do if a card more than 4 is drawn
            else:
                print(f'***MORE THAN FOUR***')



drawpile = Deck()
drawpile.shuffle()

for players in range(Game.player_count):
    exec(f'player{players} = Player("Player {players + 1}")')


def deal():
    for i in range(9):
        for players in range(Game.player_count):
            eval(f'player{players}').draw(drawpile, "main")

    for players in range(Game.player_count):
        eval(f'player{players}').board_init()

    drawpile.discard.append(drawpile.cards.pop())


deal()

for players in range(Game.player_count):
    eval(f'player{players}').play_turn()
    eval(f'player{players}').showGridUp()

