# -*- coding: utf-8 -*-
"""
DEMONSTRATE iohub module versus event module
Crucial difference is for stuff that halts something
"""
from psychopy import iohub, visual, event, core
win = visual.Window()
textStim = visual.TextStim(win, text='press now', height=0.1, wrapWidth=100)

io = iohub.launchHubServer()
keyboard = io.devices.keyboard

# Wait for a particular key using iohub and event.getKeys
print 'waiting now...'
stuff = keyboard.waitForKeys(chars=['F', 'b', ' '])

event.waitKeys()
print('NOW')

# Comparing iohub.
while True:
    # Get responses
    event_getkeys = event.getKeys(timeStamped=True)
    io_getpresses = keyboard.getPresses()
    
    # Update text if a matching response was found
    if len(event_getkeys) and len(io_getpresses):
        textStim.text = """
            event.getKeys time: %.3f s\n
            iohub.getPresses time: %.3f s\n
            io time is %i ms before event
            """ %(event_getkeys[0][1], io_getpresses[0].time, 1000*(event_getkeys[0][1] - io_getpresses[0].time))
        
        if io_getpresses[0].char == 'q': 
            break
    
    # Animate and show results
    textStim.ori += 0.1
    textStim.draw()
    win.flip()
    # core.wait(0.2)  # to make it even more obvious TO DO

io.quit()
