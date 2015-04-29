# -*- coding: utf-8 -*-
"""
How to synchronize to monitor frames with a functional win.flip() and without.
On "good" computers with a 60Hz monitor, this script should result in two
identical numbers close to 1.

Jonas Lindeløv, 2014.
"""
# Setting up stimuli
from psychopy import visual, core
win = visual.Window()
stimGrating = visual.GratingStim(win, mask='gauss', sf=10)
clock = core.Clock()

# when win.flip() waits for flip:
win.callOnFlip(clock.reset)  # will reset the clock. Could also be a
for frame in range(60):  # 1 second on 60 Hz monitors
    stimGrating.setPhase(0.02, '+')
    stimGrating.draw()
    win.flip()  # win.flip() waits for next monitor update
win.flip()
print clock.getTime()  # Actual duration


# Disable wait for vertical blanking, simulating a bad pc
win.close()
win = visual.Window(waitBlanking=False)

# Hack for computers that don't wait for win.flip().
# It's useful for development but don't it use for data collection!
# Note: takes a total of 5 lines more than the above version.
frameClock = core.Clock()
frameDuration = 0.01666667  # measure it physically or use ppc.getActualFrameRate()
win.callOnFlip(clock.reset)
for frame in range(60):
    stimGrating.setPhase(0.02, '+')
    stimGrating.draw()

	# these three lines replaces the properly working win.flip()
    while frameClock.getTime() < frameDuration: pass  # wait for imaginary flip
    frameClock.reset()
    win.flip()
win.flip()
print clock.getTime()  # Actual duration