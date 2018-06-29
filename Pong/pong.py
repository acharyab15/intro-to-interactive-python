# Implementation of classic arcade game Pong
# http://www.codeskulptor.org/#user43_keJufptINy_3.py


import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == RIGHT:
        ball_vel = [random.randrange(2,4), -random.randrange(1,3)]
    elif direction == LEFT:
        ball_vel = [-random.randrange(2,4), -random.randrange(1,3)]
     

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] <= BALL_RADIUS or (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen

    paddle1_pos = min(paddle1_pos + paddle1_vel , HEIGHT - PAD_HEIGHT)
    paddle1_pos = max(0, paddle1_pos + paddle1_vel)

    paddle2_pos = min(paddle2_pos + paddle2_vel , HEIGHT - PAD_HEIGHT)
    paddle2_pos = max(0, paddle2_pos + paddle2_vel)
        
    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos ), 
                         (PAD_WIDTH, paddle1_pos), 
                         (PAD_WIDTH, paddle1_pos + PAD_HEIGHT),
                         (0, paddle1_pos + PAD_HEIGHT)], 1, 'White', 'White')
    canvas.draw_polygon([(WIDTH, paddle2_pos), 
                         (WIDTH - PAD_WIDTH, paddle2_pos), 
                         (WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT),
                         (WIDTH, paddle2_pos + PAD_HEIGHT)], 1, 'White', 'White')
    
    # determine whether paddle and ball collide    
    if (ball_pos[0]-BALL_RADIUS) <= (PAD_WIDTH):
        if (ball_pos[1] + BALL_RADIUS) >= paddle1_pos and (ball_pos[1] - BALL_RADIUS) <= (paddle1_pos + PAD_HEIGHT):
            ball_vel[0] = -(1.1*ball_vel[0])
        else:
            spawn_ball(LEFT)
            score2 += 1
            
    if (ball_pos[0]+BALL_RADIUS) >= (WIDTH - PAD_WIDTH):
        if (ball_pos[1] + BALL_RADIUS) >= paddle2_pos and (ball_pos[1] - BALL_RADIUS) <= (paddle2_pos + PAD_HEIGHT):
            ball_vel[0] = -(1.1*ball_vel[0])     
        else:
            spawn_ball(RIGHT)
            score1 += 1
     
    # draw scores
    canvas.draw_text(str(score1),[WIDTH / 4, 80], 50, "Blue")
    canvas.draw_text(str(score2),[3 * WIDTH / 4, 80], 50, "Blue")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    con = 3
    if chr(key) == "W":
        paddle1_vel -= con
    elif chr(key) == "S":
        paddle1_vel += con
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= con
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += con
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if chr(key) == "W":
        paddle1_vel = 0
    elif chr(key) == "S":
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

def restart():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', restart)


# start frame
new_game()
frame.start()
