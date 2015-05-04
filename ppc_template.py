# -*- coding: utf-8 -*-
"""
PSYCHOPY EXPERIMENT SCRIPT TEMPLATE
The script is a part of a PsychoPy course which you can learn more about here:
http://lindeloev.net/?page_id=134

It does require that you have the ppc.py in the same folder as the script.
Find ppc.py on the course website.

Version 2015-05
Free to use for any purpose. Credit is nice but not required.
By Jonas Kristoffer Lindeløv: jonas@cnru.dk

----------

PURPOSE OF THIS SCRIPT:
This is a template for scripting psychopy experiments while following good
practicies. The template is thoroughly commented in order to explain the code
as well as the rationale of doing it this particular way. The actual code
length without comments and initial variables is just around 80 lines, so it's
not as overwhelming as it might look :-) This script is targeted at psychopy
beginners with a few general purposes: (1) it introduces the basic psychopy
functions you're most likely to need in a full experiment, (2) proposes an
effecient and flexible code structure which you can use as a head-start when
coding most experiments, (3) prevent rookie mistakes in timing and crashes.


THE EXPERIMENT:
This is a silly experiment in which users are asked to indicate the orientation
of a gabor patch. It can show up at different locations and is either preceeded
by a fixation cross indicating it's true position or a false position.
Furthermore, it has various durations. Maybe we want to see the impact of cue
and stimulus duration on identification performance.

Formally the design is factorial:
    orientation x duration x repetitions x positions x trueCue


FEATURES OF THE SCRIPT:
The important thing is that this experiment incorporates most features that
experiments will use:
    * Initial dialogue box
    * Display messages and ask questions to participants (intro, instructions,
      per-trial-questions etc.). Records reaction time. Also pauses at
      regular intervals of trials.
    * Nice control of blocks and conditions. Easy to run conditions in multiple
      orders to counterbalance possible order effects.
    * Accurate timing of stimulus presentation (by monitor frames instead of
      milliseconds) and assessment of this timing. Read why this is important
      here: http://www.psychopy.org/general/timing/millisecondPrecision.html
      Also accurate timing of keyboard responses.
    * Use eye-degrees as units of visual size.
    * Save data after each trial to minimize data loss in the event of a crash.
    * Easily scalable to complex experiments.
    * Note that iohub should be used to get keyboard events in general, but in 
      this experiment, event is fine since all answers are during wait-periods.

CODE STRATEGY / PHILOSOPHY
The general coding strategy is to prepare absolutely everything before the
critical data-collection part begins. The purpose is to minimize computational
load and complexity during the actual presentation of the stimuli. As such,
lag and potential errors is minimized prevented during stimulus presentation.
Most of the stuff is done before the welcome screen even hits the participant.
Only a little is left to be done before each trial (change relevant
stimulus parameters for this trial) and this is done before the timing critical
part.

Another general coding strategy is to keep stuff-you-or-others-might-change-often
in dedicated sections. This is the VARIABLES and the RUN EXPERIMENT sections.
This is the stuff that you would usually report in your method's section
(like the ISI, number of trials, question text, sequence of blocks etc.).
The philosophy is to keep function and "content" separate so that you (and
others) may easily adapt the experiment without having to scroll down through
the code to change these variables in a lot of obscure places.


CODE STRUCTURE:
The overall code structure of this template goes like this:
    * VARIABLES: variables pertaining to trials and stimulus presentation.
    * IMPORT the python modules to be used. The python convention is to import in
      the beginning of the script.
    * DIALOGUE AND STIMULI: Initiate psychopy stimuli and handy variables. This is
      computationally heavy.
    * FUNCTIONS: Define functions that does all the stimulus presentation.
    * RUN EXPERIMENT: actually execute the experiment, with the instructions and
      blocks in any order you'd like.

"""


"""
SET VARIABLES
"""
# General variables
mon_distance = 60  # Distance between subject's eyes and monitor
mon_width = 50  # Width of your monitor in cm
mon_size = [1024, 768]  # Pixel-dimensions of your monitor
save_folder = 'templateData'  # Log is saved to this folder. The folder is created if it does not exist.

# Setting up stimulus
gabor_sf = 4  # 4 cycles per degree visual angle
gabor_opacity = 0.5  # 50 %
gabor_size = 5  # in degrees visual angle
fix_height = 1  # Text height of fixation cross

frames_fix = 30  # in frames. ~ 500 ms on 60 Hz
frames_stim = [6, 9, 12]  # in frames. ~ 100, 150 and 200 ms on 60 Hz
frames_mask = 3  # in frames. ~ 50 ms on 60 Hz

# Trial parameters
repetitions = 2  # number of trials per condition
positions = [-3, 0, 3]  # x-positions
oris = {'right': 0, 'left': 90}  # Orientations and corresponding responses! values = oris.values() and keyboard keys = oris.keys()
pause_interval = 10  # Number of trials between breaks

# Questions and messages
message_pos = [0, 3]  # [x, y]
message_height = 1  # Height of the text, still in degrees visual angle
text_break = 'Press SPACE to continue...'  # text of regular break
keys_break = [' ', 'space']  # Keys to accept at regular break
keys_quit = ['escape']  # Keys that quits the experiment

text_instruct = """
    Press LEFT if the lines are horizontal.
    Press RIGHT if the lines are vertical.

    Keep your gaze at the cross at all times."""


"""
 SHOW DIALOGUE AND INITIATE PSYCHOPY STIMULI
 This is computationally heavy stuff. Thus we do it in the beginning of our experiment
"""

# Import stuff
import ppc
print 'the physical diameter of the gabor patch should be', ppc.deg2cm(gabor_size, mon_distance), 'cm'
print 'the physical size of the fixation cross should be', ppc.deg2cm(fix_height, mon_distance), 'cm'

from psychopy import core, visual, gui, monitors, sound, event
import random

# Intro-dialogue. Get subject-id and other variables.
# Save input variables in "V" dictionary (V for "variables")
V = {'subject':'', 'condition': ['trueFix', 'falseFix'], 'age':'', 'gender':['male', 'female']}
if not gui.DlgFromDict(V, order=['subject', 'age', 'gender']).OK:
    core.quit()

# Stuff
clock = core.Clock()  # A clock wich will be used throughout the experiment to time events on a trial-per-trial basis (stimuli and reaction times).
writer = ppc.csvWriter(str(V['subject']), saveFolder=save_folder)  # writer.write(trial) will write individual trials with low latency

# Create psychopy window
my_monitor = monitors.Monitor('testMonitor', width=mon_width, distance=mon_distance)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(mon_size)
win = visual.Window(monitor=my_monitor, units='deg', fullscr=True, allowGUI=False, color='black')  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!

# Stimuli.
stim_gabor = visual.GratingStim(win, mask='gauss', sf=gabor_sf, opacity=gabor_opacity, size=gabor_size)  # A gabor patch. Again, units are inherited.
stim_fix = visual.TextStim(win, '+', height=fix_height)  # Fixation cross is just the character "+". Units are inherited from Window when not explicitly specified.
stim_text = visual.TextStim(win, pos=message_pos, height=message_height, wrapWidth=999)  # Message / question stimulus. Will be used to display instructions and questions.
sound_success = sound.Sound('C', secs=0.1, octave=6)  # Obs, ppc.Sound() is much more accurate, but only works on windows.
sound_fail = sound.Sound('C', secs=0.4, octave=4)


"""
 FUNCTIONS
"""

def ask(text='', keyList=None):
    """
    Ask subject something. Shows question and returns answer (keypress)
    and reaction time. Defaults to no text and all keys.
    """
    # Draw the TextStims to visual buffer, then show it and reset timing immediately (at stimulus onset)
    stim_text.setText(text)
    stim_text.draw()
    time_flip = win.flip()  # time of core.monotonicClock.getTime() at flip

    # Halt everything and wait for (first) responses matching the keys given in the Q object.
    if keyList:
        keyList += keys_quit
    response = event.waitKeys(keyList=keyList, timeStamped=True)  # timestamped according to core.monotonicClock.getTime() at keypress
    if response[0][0] in keys_quit:  # Look at first reponse [0]. Quit everything if quit-key was pressed
        core.quit()
    return response[0][0], response[0][1] - time_flip  # When answer given, return it.


def make_trial_list(condition):
    """
    Return a list of trials (list of dictionaries) in advance of actually displaying them.
    A makeTriallList('falseFix') with repetitions=1 could generate a trial list like this::

    trial_list = [
         {'xpos': 0, 'ori': 90, 'durationReal': '', 'response': '', 'condition': 'falseFix', 'subject': u'nick', 'rt': '', 'no': 0, 'gender': u'male', 'age': u'42', 'score': '', 'fixPos': -3},
         {'xpos': -3, 'ori': 90, 'durationReal': '', 'response': '', 'condition': 'falseFix', 'subject': u'nick', 'rt': '', 'no': 1, 'gender': u'male', 'age': u'42', 'score': '', 'fixPos': 0},
         {'xpos': -3, 'ori': 0, 'durationReal': '', 'response': '', 'condition': 'falseFix', 'subject': u'nick', 'rt': '', 'no': 2, 'gender': u'male', 'age': u'42', 'score': '', 'fixPos': 3},
         {'xpos': 3, 'ori': 0, 'durationReal': '', 'response': '', 'condition': 'falseFix', 'subject': u'nick', 'rt': '', 'no': 3, 'gender': u'male', 'age': u'42', 'score': '', 'fixPos': -3},
         {'xpos': 0, 'ori': 0, 'durationReal': '', 'response': '', 'condition': 'falseFix', 'subject': u'nick', 'rt': '', 'no': 4, 'gender': u'male', 'age': u'42', 'score': '', 'fixPos': -3},
         {'xpos': 3, 'ori': 90, 'durationReal': '', 'response': '', 'condition': 'falseFix', 'subject': u'nick', 'rt': '', 'no': 5, 'gender': u'male', 'age': u'42', 'score': '', 'fixPos': -3}
    ]

    Calling trials[0] gives the first trial, trials[1] the 2nd trial etc.
    When the experiment executes, it will simply loop over these trials from first to last using

    for trial in trial_list:
        # do something with the trial here

    It is suggested to keep all non-constant information in trials instead of
    external variables, "non-constant" being what is not the same for all trials
    and all subjects. This is stuff that you want to do statistics on.
    Remember, the problem is never too much data - it's too little data.

    Note that every trial-dictionary should have the same fields. Note also
    that there are placeholders for answers to be collected (e.g. ans and ansTime).

    You could use psychopy.data.TrialHandler instead of the code below, which
    would be great for this simple case. But building your trials like below
    is scaleable to more complex cases and you remain in control.
    """

    # Factorial design
    trial_list = []
    for ori in oris.values():
        for pos in positions:
            for dur in frames_stim:
                for rep in range(repetitions):
                    # Add a dictionary for every trial
                    trial_list += [{
                        'ori': ori,
                        'xpos': pos,
                        'fixPos': pos if condition == 'trueFix' else random.choice([x for x in positions if x is not pos]),
                        'subject': V['subject'],
                        'age': V['age'],
                        'gender': V['gender'],
                        'condition': condition,
                        'duration': dur,
                        'durationReal': '',
                        'response': '',
                        'rt': '',
                        'score': ''
                    }]

    # Randomize order
    from random import sample
    trial_list = sample(trial_list, len(trial_list))

    # Add trial numbers and return
    for i, trial in enumerate(trial_list):
        trial['no'] = i + 1  # start at 1 instead of 0
    return trial_list


def run_block(condition):
    """
    Runs a block of trials. This is the presentation of stimuli,
    collection of responses and saving the trial
    """
    ask(text_instruct)  # Instruction

    # Displays trials. Remember: prepare --> timing critical stuff --> score, save etc.
    for trial in make_trial_list(condition):
        # Prepare trial here, before entering the time-critical period
        stim_gabor.setOri(trial['ori'])
        stim_gabor.setPos([trial['xpos'], 0])
        stim_fix.setPos([trial['fixPos'], 0])

        # A break at regular interval. Also at the beginning of the experiment
        # Show break message when trial['no'] is a multiple of pause_interval (% is modulus)
        if trial['no'] % pause_interval is 0:
            ask(text_break, keys_break)

        # ACTION: THIS IS THE TIMING CRITICAL PART
        # Fixation cue
        win.callOnFlip(clock.reset)
        for frame in range(frames_fix):
            stim_fix.draw()
            win.flip()

        # Stimulus
        for frame in range(trial['duration']):
            stim_gabor.draw()
            stim_fix.draw()
            win.flip()

        # Mask
        for frame in range(frames_mask):
            for ori in oris.values():
                stim_gabor.setOri(ori)
                stim_gabor.draw()
            stim_fix.draw()
            win.flip()

        # Get actual duration at offset
        stim_fix.draw()
        win.flip()  # blank screen
        trial['durationReal'] = clock.getTime()

        # END OF TIMING CRITICAL SECTION
        # Ask question and record responses.
        stim_fix.draw()
        trial['response'], trial['rt'] = ask(' ', oris.keys())
        trial['score'] = 1 if oris[trial['response']] == trial['ori'] else 0  # 1 if key corresponds to the shown orientation
        sound_success.play() if trial['score'] else sound_fail.play()  # feedback

        # Save trial
        writer.write(trial)


"""
 RUN EXPERIMENT
 Now it's really simple. You simply execute things using the functions ask and
 run_block. Here we order block types given input from dialogue box
"""
ask()
if V['condition'] == 'trueFix':
    run_block('trueFix')
    run_block('falseFix')

elif V['condition'] == 'falseFix':
    run_block('falseFix')
    run_block('trueFix')
