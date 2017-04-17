# template for "Stopwatch: The Game"
# This game keeps track of the number of times that you have stopped the 
# watch and how many times you manage to stop the watch on a whole second

# define global variables
# count is the number of timer ticks
# z is the number of successful stops 
# y is the number of total stops 
count = 0
z=0
y=0
stop = True

import simplegui

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    a = t//600
    b =((t//10)%60)//10
    c =((t//10)%60)%10
    d =(t%10)
    return str(a) + ":" + str(b) + str(c) + "." + str(d) 

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global stop
    stop = False
    timer.start()
    
def stop():
    global z, y, stop  
    if stop == False:
        y +=1
        if count % 10 == 0:
            z += 1
    stop = True
    timer.stop()    

def reset():
    global count,z,y    
    count = 0
    z = 0
    y = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count +=1
    
# define draw handler
def draw(canvas):
    time = str(format(count))
    counter = str(z) + "/" + str(y)
    canvas.draw_text(time,(100,100),12,"white")
    canvas.draw_text(counter,(250,20),12,"red")
    
# create frame
timer = simplegui.create_timer(100, tick)
frame = simplegui.create_frame("stopwatch", 300,200)
frame.add_button("start", start, 100)
frame.add_button("stop", stop, 100)
frame.add_button("reset", reset, 100)

frame.set_draw_handler(draw)
# register event handlers


# start frame
frame.start()
