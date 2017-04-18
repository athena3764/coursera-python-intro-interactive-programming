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
play = False
player_busted = "You have busted and lose"
dealer_busted = "Dealer has busted. You win"
dealer_wins = "You lose"
player_wins = "You win"
game_over = False 
outcome = False
outcome1 = False
outcome2 = False
outcome3 = False
hit_or_stand = True
new_deal = False
hole = True
score = 0
card_num = 0

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
        card_loc = (CARD_CENTER[0]+CARD_SIZE[0]* RANKS.index(self.rank),
                    CARD_CENTER[1]+CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0]+CARD_CENTER[0], pos[1]+CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
    # create Hand object
        self.cards = []

    def __str__(self):
    # return a string representation of a hand
        ans = "Hand contains"
        for i in self.cards:
            ans += " " + str(i)
        return ans
     
    def add_card(self, card):
    # add a card object to a hand      
        return self.cards.append(card)

    def get_value(self):
    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    # compute the value of the hand, see Blackjack video
        value1 =[]
        value = 0 
        for j in self.cards:
            rank = j.get_rank()
            value1.append(rank)
            value += VALUES[rank]
            
        if "A" in value1 and value < 12:
            return value + 10
        else:
            return value    
    def draw(self, canvas, pos):
    # draw a hand on the canvas, use the draw method for cards
        if hole == True:
            canvas.draw_image(card_back, [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]], CARD_BACK_SIZE, [pos[0]+CARD_BACK_CENTER[0], pos[1]+CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

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
        return self.deck.pop()	# deal a card object from the deck
    
    def __str__(self):
    # return a string representing the deck
        ans = "Deck contains"
        for i in self.deck:  
            ans += " " + str(i)
        return ans

#define event handlers for buttons
def deal():
    global card_num,score, game_over,hit_or_stand, new_deal, hole, outcome, outcome1, outcome2, outcome3, play, dealer,my_deck, player 
    outcome = False
    outcome1 = False
    outcome2 = False
    outcome3 = False
    hit_or_stand = True
    new_deal = False
    hole = True
    
    if game_over:
        score = 0
        game_over = False
        hit_or_stand = True
    
    my_deck = Deck()
    player = Hand()
    dealer = Hand()
    
    my_deck.shuffle()    
    my_deck.deal_card()
       
    if card_num > 52:
        game_over = True
        card_num =0
    
    player.add_card(my_deck.deal_card())
    card_num +=1
    
    dealer.add_card(my_deck.deal_card())
    card_num +=1
    
    dealer.add_card(my_deck.deal_card())
    card_num +=1  
    
    play = True
    
def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score    
    global card_num,game_over,hit_or_stand, new_deal, score,hole, outcome, outcome1, outcome2, outcome3, play, dealer,my_deck, player 
    new_deal = True
    hit_or_stand = True
    if card_num > 52:
        card_num = 0
        game_over = True
        play =False   

    if play:
        player.add_card(my_deck.deal_card())
        card_num +=1           
        if player.get_value() > 21:
            new_deal = True
            hit_or_stand = False
            outcome = True
            score-=1
            hole = False
            play = False

def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global card_num, game_over,new_deal, hit_or_stand, score, hole, outcome, outcome1, outcome2, outcome3, play, dealer,my_deck, player 
    hit_or_stand = False
    new_deal = True
    hole = False
    
    if card_num > 52:
        game_over = True
        card_num = 0    
        play =False
    
    if play:
        while dealer.get_value() < 17:
            dealer.add_card(my_deck.deal_card())
            card_num +=1
            
        if dealer.get_value() > 21:
            outcome1 = True
            score+=1
             
        elif dealer.get_value()>= player.get_value():
            outcome2 = True
            score-=1
        
        elif dealer.get_value() >= 17 and player.get_value() <22 and player.get_value() > dealer.get_value():            
            outcome3 = True
            score+=1        
    play = False  

# draw handler    
def draw(canvas):
    global game_over, score,hole, outcome, outcome1, outcome2, outcome3, play, dealer,my_deck, player 
    
    #draw dealer card images
    for d in dealer.cards:
        d.draw(canvas, [CARD_SIZE[0]+dealer.cards.index(d) * CARD_SIZE[0]*0.5, 150])       
    
    #draw dealer card back
    dealer.draw(canvas, [CARD_BACK_SIZE[0], 150])
    
    #draw player card images
    for p in player.cards:
        p.draw(canvas, [CARD_SIZE[0]+player.cards.index(p) * CARD_SIZE[0]*0.5,300])
        
    canvas.draw_text("Player", (50, 290), 30, 'Black')
    canvas.draw_text("Dealer", (50, 140), 30, 'Black')   
    canvas.draw_text("Blackjack", (20, 50), 50, 'Black')    
    canvas.draw_text("Score = " + str(score), (300, 70), 30, 'Black')
    
    if outcome:
        canvas.draw_text(player_busted, (30, 100), 30, 'Black')
    if outcome1:
        canvas.draw_text(dealer_busted, (50, 100), 30, 'Black')
    if outcome2:
        canvas.draw_text(dealer_wins, (100, 100), 30, 'Black')
    if outcome3:
        canvas.draw_text(player_wins, (100, 100), 30, 'Black')
    
    if hit_or_stand == True and play == True and game_over == False:
        canvas.draw_text("Hit or stand?", (100, 500), 30, 'Black')
    if new_deal == True and play == False and game_over == False:
        canvas.draw_text("New deal?", (100, 500), 30, 'Black')
    if game_over == True:
        canvas.draw_text("Cards ran out and game over! New deal?", (100, 500), 30, 'Black')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")
 
#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
