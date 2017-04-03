import simplegui,random 

# helper function to initialize globals
def new_game():
    global state, card1, card2, card, card_cover, count
    card = list(range(1,9) + range(1,9))
    card_cover = list(range(1,9) + range(1,9))
    state = 0
    card1 = 0
    card2 = 0
    count = 0
    label.set_text("Turns = " + str(count))
    random.shuffle(card)

# define event handlers
def mouseclick(pos):
    global state, card1, card2, card, card_cover, count
    #compute the index of the card
    index = pos[0]//50
    #flip current card, save it as the first card, next state is 1
    if state == 0:
        state = 1
        card1 = index 
        card_cover[card1] = False
        count +=1
    #flip current card, save it as the second card, next state is 2
    elif state == 1:
        state = 2
        card2 = index 
        card_cover[card2] = False
    #check if the first and second cards match, and if not unflip them.
    #Regardless of what happened in that check, flip current card, save it as the first card next state is 1
    else:
        state = 1
        if card[card1] != card[card2]:
            card_cover[card2] = True
            card_cover[card1] = True
        card1 = index 
        card_cover[card1] = False
        count +=1
    #total count of turns
    label.set_text("Turns = " + str(count))
   
def draw(canvas):
    global card, card_cover
    for card_index in range(len(card)):
        card_pos = 50*card_index
        #draw exposed cards
        if card_cover[card_index] == False:
            canvas.draw_text(str(card[card_index]),(card_pos+25,50), 30, "White")
        #draw flipped cards
        else:
            canvas.draw_polygon([[card_pos, 0],[card_pos, 100],[card_pos+50, 100],[card_pos+50,0]], 1, "Red", "Green") 

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()              

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
