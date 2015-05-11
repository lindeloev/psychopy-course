# -*- coding: utf-8 -*-
"""
This is a small demo on using iohub to capture keyboard and mouse responses.
psychopy.iohub can be used to replace psychopy.event

psychopy.iohub is superior to psychopy.event in the following ways:
 * Listen for input while the main python session is busy with stimuli.
   This is good for timing!
 * Listen for keyboard releases and currently pressed keys.
 * Easily capture combinations of keys and the characters they return.

NOTE: If you're running Mac OS, you may need to elevate psychoopy's permissions
for iohub to work properly. Otherwise it will only capture moderator keys.
Drag-drop psychopy into the Accessibility: http://kb.parallels.com/en/116418.

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

io.wait(1)
io.clearEvents('all')
print 'listening now!'

# iohub wait* methods above are identical to doing this, although they do 
# it in a different process than the main python session:
while True:
    events = keyboard.getEvents(iohub.EventConstants.KEYBOARD_RELEASE)  # listening for releases
    if events:  # if non-empty
        break

print 'finish'



"""
TO DO:
  * GETTING KEYBOARD RESPONSE DURING FLIP-LOOP.
  * MOUSE STUFF
"""
