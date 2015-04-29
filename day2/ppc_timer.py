# -*- coding: utf-8 -*-
"""
Timing python code and psychopy using the handy ppc.timer() function.
It's used to identify bottlenecks in the script, especially the part
   within the flip()-loop.

Jonas Lindeløv, 2013.
"""

import ppc

# -------------------------
# TIMING BASIC PYTHON STUFF
# Basic stuff is very fast!
# -------------------------

ppc.timer('pass')  # should give something close to 0
ppc.timer('if 99 == 99: pass')
ppc.timer('if "a" == "a": pass')
ppc.timer('if "abracadabra" == "abracadabra": pass')  # string length means nothing
ppc.timer('myVariable = 4 + 5 * 2 / 3')

# Putting stuff in __main__ and time them
three = 3
ppc.timer('4 + three', 'three')  # using a variable is slower


# -------------------------
# TIMING PSYCHOPY STUFF
#   * Initating stimuli is slow, > 10ms
#   * Setting properties is medium. 0.1 - 5 ms (slower for text)
#   * Drawing is fast
# -------------------------

from psychopy import core, visual
win = visual.Window()
stim = visual.TextStim(win)
clock = core.Clock()

# Checking core.Clock() timing:
clock.reset()  # set clock to zero
core.wait(0.1)  # wait a little
print '\'core.wait(0.1)\'', clock.getTime()  # check the clock. It should be pretty accurate.



"""
TIMING EXERCISES:
    1. How long does it take to create a win = visual.Window()?
    2. How long does it take to reset a clock?
    3. How long does it take to get current time of clock?
	4. Test whether core.wait() is accurate, e.g. by setting it to 7 ms
	   OBS: core.wait() is a slow first-runner. Run once before doing the timing.
    4. Create a TextStim.
        How long does it take to do textStim.setText('hi')
        How long does it take to do textStim.setText('hi there my dear old friend. I\'m very happy to see you again! We should meet more often')
	
	5. Pro: Do a multi-line alteration of a GratingStim (rotation, color etc.)
		   and time it including the draw but excluding the flip.	
    6. Pro: How large a text can you put into visual.TextStim.setText() without loosing frames?
"""

# SOLUTIONS #1-#3
ppc.timer('win = visual.Window()', 'visual')
ppc.timer('clock.reset()', 'clock')
ppc.timer('clock.getTime()', 'clock')

# 4 short vs. long text
stim = visual.TextStim(win)
ppc.timer('stim.setText("hi")', 'stim')
ppc.timer('stim.setText("hi there my dear old friend. I\'m very happy to see you again! We should meet more often")', 'stim')

# 6 milti-line
stim = visual.GratingStim(win)
script = """
    stim.setPos([0, 1])
    stim.setOri(45)
    stim.setColor('black')
    stim.draw()
    #win.flip()
    duration = clock.getTime()
    clock.reset()
"""
ppc.timer(script, 'stim, clock')


# You can time stuff in the actual experiment to get more ecologically valid timing
# However, they give identical results (as they should) so ppc.timer() is simpler.
# It's too optimistic but close enough to be useful for identifying bottlenecks.
stim = visual.TextStim(win)
clock = core.Clock()
timesPos, timesWait, timesClock, timesText = [], [], [], []  # we'll fill these lists with individual execution times
for trial in range(1000):
    # Do stuff here. And then in the critical part:
    clock.reset()
    timesClock += [clock.getTime()]

    clock.reset()
    stim.setPos((1,1))
    timesPos += [clock.getTime()]

    clock.reset()
    stim.setText('Setting a long text is slow')
    timesText += [clock.getTime()]

    clock.reset()
    core.wait(0.0017)
    timesWait += [clock.getTime()]

# Calculate mean execution time and compare to "timer" function
clockBaseline = 1000 * sum(timesClock) / len(timesClock)
print '\nclock baseline:', clockBaseline, 'ms'  # negligeble, therefore not used

ppc.timer('stim.setPos((1,1))', setup='stim')
print 'RESULT:', 1000 * sum(timesPos) / len(timesPos), 'ms (in-script test)'

ppc.timer('core.wait(0.0017)', setup='core')  # should be close to 1.7 ms
print 'RESULT:', 1000 * sum(timesWait) / len(timesWait), 'ms (in-script test)'  # should be close to 1.7 ms

ppc.timer('stim.setText("Setting a long text is slow")', setup='stim')
print 'RESULT:', 1000 * sum(timesText) / len(timesText), 'ms (in-script test)'