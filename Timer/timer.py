# template for "Stopwatch: The Game"
import simplegui

# define global variables
counter = 0
stop_counter = 0
whole_counter = 0
is_running = False
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    first = t // 600
    temp = t % 600
    second = float(temp) / 10
    if len(str(second)) == 3:
        tyme = str(first)+":0"+str(second)
    else:
        tyme = str(first)+":"+str(second)
    return tyme

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global is_running
    is_running = True
    timer1.start() 
    
def stop():
    global stop_counter
    global whole_counter
    global is_running
    if is_running == True:
        is_running = False
        stop_counter += 1
        if counter % 10 == 0:
            whole_counter += 1
    
        timer1.stop()
    
def reset():
    global counter
    global whole_counter 
    global stop_counter
    whole_counter = 0
    stop_counter = 0
    counter = 0
    timer1.stop()

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global counter
    counter += 1
    print counter
    
    
# define draw handler
def draw(canvas):
    canvas.draw_text(format(counter), [150,150], 36, "Red")  
    tally = str(whole_counter) + "/" + str(stop_counter)
    canvas.draw_text(tally, [220, 50], 36, "Blue")
    
# create frame
frame = simplegui.create_frame("Timer", 300, 300)
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)
frame.set_draw_handler(draw)

# register event handlers
timer1 = simplegui.create_timer(100, timer_handler)

# start frame
frame.start()

# Please remember to review the grading rubric
print format(613)