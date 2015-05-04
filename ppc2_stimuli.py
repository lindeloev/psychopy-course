# -*- coding: utf-8 -*-
"""
Introduction to different stimulus types in Python.
 * different stimulus types and properties
 * cross-monitor consistent stimulus size in cm and degrees
 * within-monitor equal stimulus luminsities using the DKL colorspace

Jonas Kristoffer Lindeløv, 2014. Revised 2015.
"""

# -----------------------------
# STIMULUS TYPES AND PROPERTIES
# -----------------------------

# Generic layout
from psychopy import visual, event
win = visual.Window()
stim_text = visual.TextStim(win, text='Welcome', color='black')
stim_text.draw()
win.flip()
event.waitKeys()

"""
Exercise on changing parameters:
    * change background color of the Window to black. And don't do fullscreen.
	  Hint: if you want to do this while running the experiment, you can either:
          (1) change win.color and call win.flip() twice for it to take effect.
          (2) close the current window using win.close() and create a new.

    * change the height and orientation of the TextStim.
    * event.waitKeys() waits infinitely. Make it wait for a maximum of 5 seconds
      and only react to the keys ['space', 'n', 'm'].
"""

# SOLUTION:
win.color = 'black'
win.flip()
win.flip()
event.waitKeys()

stim_text = visual.TextStim(win, text='Welcome', color='gray', height=0.2, ori=30)
stim_text.draw()
win.flip()
event.waitKeys(maxWait=5, keyList=['space', 'n', 'm'])


# ImageStim
stim_image = visual.ImageStim(win, image='xkcd.png')
stim_image.size *= [1, -1]  # flip vertically
print stim_image.size  # the size of the stimulus in current units
stim_text.pos = [0, 0.6]

stim_image.draw()
stim_text.draw()
win.flip()
event.waitKeys()
"""
Exercise on GratingStim, parameters and drawing:
    * make a GratingStim (call it e.g. stim_grating) and show it to see what it does
    * change various parameters after it is initiated,
      e.g. make a gabor patch by setting mask to a gaussian and spatial 
      frequency (sf) to 10.
    * show it on top of stim_image and stim_text with reduced opacity
	  hint: to draw on top, simply draw last.
   
    * pros: try animating stuff by wrapping draw(), flip() and a change of
      stimulus attributes in a loop, e.g. with the following per-frame change:
          stim_image.ori += 0.1   # change stim, attribute and value
          if event.getKeys(): break  # to end on a keypress
"""
# SOLUTION
stim_grating = visual.GratingStim(win)
stim_grating.mask = 'gauss'
stim_grating.sf = 10
stim_grating.pos = [-0.1, -0.1]
stim_grating.opacity = 0.5

stim_image.draw()
stim_text.draw()
stim_grating.draw()
win.flip()
event.waitKeys()

# Animate
while True:
    stim_image.ori += 0.5
    stim_grating.size += 0.01
    stim_grating.sf *= 1.005
    stim_image.draw()
    stim_grating.draw()
    win.flip()
    if event.getKeys(): break  # to end on a keypress


# SHOW SLIDES HERE
# -----------------------------
# STIMULUS SIZE
# Handling actual stimulus size for consistent presentation across monitors!
# -----------------------------

# Demonstrate monitor center!
from psychopy import visual, monitors
my_monitor = monitors.Monitor('testMonitor', width=34.3, distance=65)
my_monitor.setSizePix([1024, 768])

# Start a new window with degrees as default unit
win.close()
win = visual.Window(monitor=my_monitor, color='black')

# In cm
stim_image = visual.ImageStim(win, image='xkcd.png', size=[10, 10], units='cm')
stim_image.draw()
win.flip()
event.waitKeys()

# in degrees
stim_image.units = 'deg'
stim_image.draw()
win.flip()
event.waitKeys()

"""
Exercise on visual size precision:
    * Specify your own monitor dimensions in monitor center (using Coder or Builder)
    * Specify your own monitor dimensions in code

    * change the size of the image, e.g. to [3, 6] and verify that it actually
      is the expected size.
    * Draw some different kinds of stimuli using cm as units and verify size.
    * Some stimuli aren't the actual expected size. Adjust the parameters
      so that they are the size that you want.

    * Pro: draw different kinds of stimuli using deg and verify whether they
	  have the expected size. (hint: math.tan, math.radians)
    * Pro: textStims are smaller than the expected size. The relationship is
	  however approximately linear. Determine the linear function that makes
	  the actual size correspond to the specified size. Do you think it would
	  be general across monitors? And/or general across fonts?
"""

# Checking size in degrees. size = tan(angle_in_radians) * distance
import ppc
print ppc.deg2cm(10, 65)
print ppc.deg2cm(3, 60)


# ----------------------
# EQUILUMINANT STIMULI
# ... especially if you calibrate your monitor and get a conversion matrix
# ----------------------

# Specify colors using the DKL colorspace
# It is DKL = [luminance, hue, saturation] where
# luminance is degrees -90 to 90
# hue is degrees 0 to 360
# saturation is excentricity 0 to 1
stim_shape1 = visual.ShapeStim(win, units='cm', size=5,
    fillColorSpace='dkl', fillColor=[0, 45, 1], pos=[0, 2])  # strong, medium luminance
stim_shape2 = visual.ShapeStim(win, units='cm', size=5,
    fillColorSpace='dkl', fillColor=[0, 215, 0.3], pos=[0, -2],  # should be a pale isoluminant contrast color
    vertices=[[0,0], [1,0], [1,1], [0,1]])
stim_shape2.vertices -= [0.5, 0.5]

stim_shape1.draw()
stim_shape2.draw()
win.flip()
event.waitKeys()

# Convert them to "normal" RGB just to see
print ppc.dkl2rgb([0, 45, 1])  # first parameter should be the same
print ppc.dkl2rgb([0, 0, -1])  # first parameter should be the same

"""
Exercise on colors:
    * make a ShapeStim and change its line and fill colors to something in DKL.
      hint: ShapeStim has the attibutes fillcolor and linecolor.
    * try changing the color of the stim_image from earlier.
"""



# ----------------------
# SOUNDS
# ... are continuous so now we can use core.wait().
# ----------------------

# Psychopy sounds
from psychopy import sound, core
clock = core.Clock()
sound_pygame = sound.SoundPygame('beep.wav', secs=0.1)

sound = sound.Sound('beep.wav', secs=0.1)
sound.play()
core.wait(0.5)


#playing
sound_pygame.play()
core.wait(0.5)


# winsound
sound_winsound = ppc.Sound('beep.wav')
sound_winsound.play()
core.wait(0.5)

"""
Exercise:
   * sound.Sound can generate sounds. Try setting value to either 440 and 'C'. 
   * Look at other parameters such as octave, secs, and volume.
   
   * Extreme pros: create an Nx2 numpy array containing the actual audio
     samples and play it!
"""
