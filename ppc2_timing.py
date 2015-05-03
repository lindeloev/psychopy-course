# -*- coding: utf-8 -*-
"""
Timing python code and psychopy using the handy ppc.timer() function.
It's used to identify bottlenecks in the script, especially the part
   within the flip()-loop.

Jonas Kristoffer Lindeløv, 2013. Revised in 2015.
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
        How long does it take to do textStim.text = 'hi'
        How long does it take to do textStim.text = 'hi there my dear old friend. I\'m very happy to see you again! We should meet more often'
	
	5. Pro: Do a multi-line alteration of a GratingStim (rotation, color etc.)
		   and time it including the draw but excluding the flip.	
    6. Pro: How large a text can you put into visual.TextStim.text without loosing frames on your system?
"""

# SOLUTIONS #1-#3
ppc.timer('win = visual.Window()', 'visual')
ppc.timer('clock.reset()', 'clock')
ppc.timer('clock.getTime()', 'clock')

# 4 short vs. long text
stim = visual.TextStim(win)
ppc.timer('stim.text = "hi"', 'stim')
ppc.timer('stim.text = "hi there my dear old friend. I\'m very happy to see you again! We should meet more often"', 'stim')

# 6 milti-line
stim = visual.GratingStim(win)
script = """
    stim.pos = [0, 1]
    stim.ori = 45
    stim.color = 'black'
    stim.draw()
    #win.flip()
    duration = clock.getTime()
    clock.reset()
"""
ppc.timer(script, 'stim, clock')


# You can time stuff in the actual experiment to get more ecologically valid timing
# However, they give identical results (as they should) so ppc.timer() is simpler.
# ppc.timer() might be too optimistic but close enough to be useful for identifying 
# bottlenecks.
stim = visual.TextStim(win)
clock = core.Clock()
def testUsingClock(code):
    times = []    # we'll fill this list with individual execution times
    for trial in range(1000):
        clock.reset()
        eval(code)
        times += [clock.getTime()]
    return 1000 * sum(times) / len(times)

def compare(code):
    # Calculate mean execution time and compare to "timer" function
    ppc.timer(code, setup='core, stim')
    print '\nclock baseline:', testUsingClock(code), 'ms'  # negligeble, therefore not used

compare('stim.pos = (1,1)')
compare('core.wait(0.0017)')  # should be close to 1.7 ms
compare('stim.text = "Setting a long text is slow"')
