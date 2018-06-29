# implementation of card game - Memory
# http://www.codeskulptor.org/#user43_LFcHdbczyA_0.py

import simplegui
import random

# helper function to initialize globals
def new_game():
    global lyst
    global exposed
    global state
    global turns
    state = 0
    turns = 0
    lyst1 = [x for x in range(0,8)]
    lyst2 = [x for x in range(0,8)]
    lyst = lyst1 + lyst2
    random.shuffle(lyst)
    exposed = [False for x in range(16)]

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global mpos
    global exposed
    global firstcard, secondcard
    global state
    global turns
    mpos = list(pos)
    cardno = mpos[0] / 50
    if state == 0:
        if exposed[cardno] == False:
            exposed[cardno] = True
            firstcard = cardno
            state = 1
    elif state == 1:
        if exposed[cardno] == False:
            exposed[cardno] = True
            secondcard = cardno
            state = 2
    else:
        turns += 1
        label.set_text('Turns =' + str(turns))
        if lyst[firstcard] != lyst[secondcard]:
            exposed[firstcard] = False
            exposed[secondcard] = False
        if exposed[cardno] == False:
            exposed[cardno] = True
            firstcard = cardno
            state = 1    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global lyst
    global exposed
    global cardno
    position = [0,80]
    #exposed[cardno] = True
    for idx in range(len(lyst)):
        if exposed[idx]:
            canvas.draw_text(str(lyst[idx]), [position[0] + 5, position[1]], 80, "White")
        else:
            canvas.draw_polygon([[position[0], 100], [position[0]+50, 100], [position[0]+50, 0], [position[0], 0]], 1, 'Black', 'Green')
        position = [position[0]+50, position[1]]
        
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
#label = frame.add_label("Turns = " + str(turns))
label = frame.add_label('Turns = 0')
# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric