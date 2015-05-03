# -*- coding: utf-8 -*-
"""
Demonstrate psychopy.useVersion()
Example: visual.TextStim.text attributeSettter was introduced in 1.81.00.

Jonas Kristoffer Lindeløv, 2015.
"""


import psychopy
psychopy.useVersion('1.80.06')  # older
#psychopy.useVersion('1.81.00')  # newer

# Now import modules and initiate stimuli from this psychopy version
from psychopy import visual, event
win = visual.Window()
stim = visual.TextStim(win)

# Set text and show it
stim.setText('Meh, this is the old stim.setAttribute(x) syntax.')  # set*()
stim.text = 'Whoa, stim.attribute = x works!'  # attributeSetter
stim.draw()
win.flip()
event.waitKeys()

