import random, simplegui, math

# helper function to start and restart the game
def new_game():
    global count, secret_number
    secret_number = random.randrange(0,100)
    count = int(math.log(101,2))

# define event handlers for control panel
def range100():
    
    # button that changes the range to [0,100) and starts a new game 
    global secret_number, count
    secret_number = random.randrange(0,100)
    count = int(math.log(101,2))
    
    def range1000():
    
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number, count
    secret_number = random.randrange(0,1000)
    count = int(math.log(1001,2))

def input_guess(number):
    
    # main game logic goes here
    global count, secret_number    
    guess  = int(number)
    print "Guess was " + number
    print "Number of remaining guesses: " + str(count)
    count -= 1
    if count < 0:
        print "game over!"
        new_game()
        count = int(math.log(101,2))    
    if guess > secret_number:
        print "Go lower!"
    elif guess < secret_number:
        print "Go higher!"
    else:
        print "Correct!"
        new_game()

# create frame
frame = simplegui.create_frame("Set and print colors", 200, 200)
frame.add_button("range(0,100)", range100)
frame.add_button("range(0,1000)", range1000)
frame.add_button("New game", new_game,100) 
frame.add_input("Enter guess", input_guess,100)

# call new_game 
new_game()

