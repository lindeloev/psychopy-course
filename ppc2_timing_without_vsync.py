# -*- coding: utf-8 -*-
"""
If your computer does not sync to vertical frames (show something strange in 
demos --> timing --> timesByFrames.py), you can hack yourself out of it. 
Here's the problem simulated and the fix. BEWARE that this will run fine 
90% of the time you start it but the last 10% is in the danger zone of trying 
to push frames at the exact update time of the monitor, thus causing a jitter 
in actual onset latency.

Jonas Kristoffer Lindeløv, 2014. Revised 2015.
"""
# Setting up stimuli
from psychopy import visual, core
win = visual.Window()
stim_grating = visual.GratingStim(win, mask='gauss', sf=10)
clock = core.Clock()

# when win.flip() waits for flip:
win.callOnFlip(clock.reset)  # will reset the clock. Could also be a
for frame in range(60):  # 1 second on 60 Hz monitors
    stim_grating.phase += 0.02
    stim_grating.draw()
    win.flip()  # win.flip() waits for next monitor update
win.flip()
print clock.getTime()  # Actual duration


# Disable wait for vertical blanking, simulating a bad pc
win.close()
win = visual.Window(waitBlanking=False)

# Hack for computers that don't wait for win.flip().
# It's useful for development but don't it use for data collection!
# Note: takes a total of 5 lines more than the above version.
clock_frame = core.Clock()
duration_frame = 0.01666667  # measure it physically or use ppc.getActualFrameRate()
win.callOnFlip(clock.reset)
for frame in range(60):
    stim_grating.phase += 0.02
    stim_grating.draw()

	# these three lines replaces the properly working win.flip()
    while clock_frame.getTime() < duration_frame: pass  # wait for imaginary flip
    clock_frame.reset()
    win.flip()
win.flip()
print clock.getTime()  # Actual duration
