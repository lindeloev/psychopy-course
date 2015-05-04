# -*- coding: utf-8 -*-
"""
PsychoPy keyboard input intro

Jonas Kristoffer Lindeløv, 2014. Revised 2015.
"""

# Initiate keyboard
from psychopy import iohub
io = iohub.launchHubServer()
keyboard = io.devices.keyboard

# WAITING FOR KEYBOARD
print 'Listening now...'
keyboard.waitForKeys(chars=['@', '!'])
print 'key event!'

print keyboard.state  # print keyboard state

keyboard.waitForReleases(keys=['f'], mods=['lalt', 'ralt'])
print 'key release!'

keyboard.waitForPresses(chars=['F', '@', '!'])
print 'key press!'


"""
EXERCISE:
    * Make a small script that waits until the subject has 
      written 'Dawg!' 
      Hint: (D, a, w, g, !).
      
    * Now start a psychopy Window with a TextStim that updates to show
      this in text, as if one was typing in a text field.
      (Maybe the text should turn green upon success?)
      
    * Pro: use keyboard.state to determine if the subject is currently
      holding down a, s, d, f, and g. 
      Hint: dict.keys() and set(lista) == set(listb)
"""

# Identical to doing this (although there is no hog duration here):
io.wait(1)
io.clearEvents('all')
print 'listening now!'
keep_listening = True
while keep_listening:
    events = keyboard.getEvents()
    for event in events:
        print event
        if event.type == iohub.EventConstants.KEYBOARD_RELEASE:
            keep_listening = False
print 'finish'



"""
TO DO:
"""

# GETTING KEYBOARD DURING RUNTIME

# Waiting for mouse events
mouse = io.devices.mouse
