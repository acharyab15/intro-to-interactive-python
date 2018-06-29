# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []
        
    def __str__(self):
        # return a string representation of a hand
        s = 'Hand contains '
        for item in self.hand:
            s += str(item) + ' '
        return s
        
    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        has_ace = None
        for card in self.hand:
            if card.get_rank() == 'A':
                has_ace = True
            hand_value += VALUES[card.get_rank()]
        if has_ace:
            if hand_value + 10 <= 21:
                hand_value = hand_value + 10
        return hand_value

    def draw(self, canvas, pos):
        for card in self.hand:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            pos[0] += 100

        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        s = 'Deck contains ' 
        for item in self.deck:
            s += str(item) + ' '
        return s
    
#define event handlers for buttons
def deal():
    global outcome, in_play
    global deck
    global player_hand, dealer_hand
    global wins
    
    if in_play:
        wins -= 1
        outcome = "Player lost"
        
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    print "Player hand is " + str(player_hand)
    print "Dealer hand is " + str(dealer_hand)
    
    # your code goes here
    
    in_play = True
    outcome = "Hit or Stand?"

def hit():
    global in_play
    global outcome
    global wins
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        
        
        value = player_hand.get_value()
        # if busted, assign a message to outcome, update in_play and score
        if value > 21:
            outcome = "Busted"
            in_play = False
            wins -= 1
    
def stand(): 
    global outcome
    global in_play
    global wins
    if outcome == "Busted":
        print "Already busted!!"
        return
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    in_play = False
    while (dealer_hand.get_value() < 17):
        dealer_hand.add_card(deck.deal_card())
        print(dealer_hand)
    # assign a message to outcome, update in_play and score
    if dealer_hand.get_value() > 21:
        outcome = "Dealer busted, player won!"
        wins += 1
    elif player_hand.get_value() <= dealer_hand.get_value():
        outcome = "Dealer won! New deal?"
        wins -= 1
    else:
        outcome = "Player won! New deal?"
        wins += 1

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome
    global in_play
    global wins
    
    player_hand.draw(canvas, [150, 450])
    dealer_hand.draw(canvas, [150, 200])
    
    if (in_play):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [150+CARD_BACK_CENTER[0],200+CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    
    canvas.draw_text("Blackjack", [200,100], 50, 'Black')
    canvas.draw_text(str(outcome), [150,400] , 40, 'Blue')
    canvas.draw_text("Score: " + str(wins), [450, 50], 30, 'Red')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
wins = 0
deal()
frame.start()


# remember to review the gradic rubric