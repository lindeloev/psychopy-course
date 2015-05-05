# -*- coding: utf-8 -*-
"""
Demonstrate iohub module versus event module with a flip-loop.
iohub registers responses during win.flip(), thus always scores
responses as faster than event.getKeys() which timestamps according
to the time that the function is called.

Jonas Kristoffer Lindeløv, 2015.
"""
import psychopy
psychopy.useVersion('1.81.02')

from psychopy import iohub, visual, event
win = visual.Window()
textStim = visual.TextStim(win, text='press now', height=0.1, wrapWidth=100)
io = iohub.launchHubServer()
keyboard = io.devices.keyboard

# Comparing iohub.
while True:
    # Animate and show results
    textStim.ori += 0.1
    textStim.draw()
    win.flip()
        
    # Get responses
    event_getkeys = event.getKeys(timeStamped=True)
    io_getpresses = keyboard.getPresses()
    
    # Update text if a matching response was found
    if len(event_getkeys) and len(io_getpresses):
        textStim.text = """
            event.getKeys time: %.3f s
            iohub.getPresses time: %.3f s
            io time is %i ms before event
            """ %(event_getkeys[0][1], io_getpresses[0].time, 1000*(event_getkeys[0][1] - io_getpresses[0].time))
        
        if io_getpresses[0].char == 'q': 
            break
