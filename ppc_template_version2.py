# -*- coding: utf-8 -*-
"""
PSYCHOPY EXPERIMENT SCRIPT TEMPLATE, VERSION 2012-10
Free to use for any purpose. Credit is nice but not required.
By Jonas Lindeløv: jonas@cnru.dk

----------

This is a template for scripting psychopy experiments while following good
practicies. The template is thoroughly commented in order to explain the code
as well as the rationale of doing it this particular way. The actual code
length without comments and initial variables is just around 75 lines, so it's
not as overwhelming as it might look :-) This script is targeted at psychopy
beginners with a few general purposes: (1) it introduces the basic psychopy
functions you're most likely to need in a full experiment, (2) proposes an
effecient and flexible code structure which you can use as a head-start when
coding most experiments, (3) prevent rookie mistakes in timing and crashes.

This is a silly experiment in which users are asked to indicate the position
of a briefly presented white circle. The important thing is that this
experiment incorporates most features that experiments will use:
- Initial dialogue box
- Display messages and ask questions to participants (intro, instructions,
    per-trial-questions etc.). Records reaction time. Also pauses at
    regular intervals of trials.
- Nice control of blocks and conditions. Easy to run conditions in multiple
    orders to counterbalance possible order effects.
- Accurate timing of stimulus presentation (by monitor frames instead of
     milliseconds) and assessment of this timing. Read why this is important
     here: http://www.psychopy.org/general/timing/millisecondPrecision.html
- Use eye-degrees as units of visual size.
- Save data after each trial to minimize data loss in the event of a crash.
- Easily scalable to complex experiments

The general coding strategy is to prepare absolutely everything before the
critiacal data-collection part begins. The purpose is to minimize computational
load and complexity during the actual presentation of the stimuli. As such,
lag and potential errors is minimized prevented during stimulus presentation.
Most of the stuff is done before the welcome screen even hits the participant
(initiate stimuli). Some is done before each block (prepare each trial in
advance). Only a little is left to be done before each trial (change relevant
stimulus parameters for this trial).

Another general coding strategy is to keep stuff-you-or-others-might-change-often
in dedicated sections. This is the VARIABLES and the RUN EXPERIMENT sections.
This is the stuff that you would usually report in your method's section
(like the ISI, number of trials, question text, sequence of blocks etc.).
The philosophy is to keep function and "content" separate so that you (and
others) can easily adapt the experiment without having to scroll down through
the code to change these variables in a lot of obscure places.

The overall code structure of this template goes like this:
- IMPORT the python modules to be used. The python convention is to import in
     the beginning of the script.
- VARIABLES: variables pertaining to trials and stimulus presentation.
- DIALOGUE AND STIMULI: Initiate psychopy stimuli and handy variables. This is
     computationally heavy.
- FUNCTIONS: Define functions that does all the stimulus presentation.
- RUN EXPERIMENT: actually execute the experiment, with the instructions and
     blocks in any order you'd like.

Further info:
- If you are new to python or programming in general, use a few hours to
     really play with and understand the "learn python in ten minutes" guide:
     http://www.korokithakis.net/tutorials/python/
- If you are new to psychopy scripting, take a look at the tutorials here:
     http://psychopy.org/coder/coder.html

"""

# Import what you need
from __future__ import division
import ppc
from psychopy import core, visual, event, gui, monitors
from random import sample

"""
SET VARIABLES
"""
# Monitor
monDistance = 60                 # Distance between subject's eyes and monitor
monWidth = 34.4                  # Width of your monitor in cm
monitorSizePix = [1366, 768]     # Pixel-dimensions of your monitor

# Stimulus
stimSize = 2                     # Radius of the stimulus in degrees
stimPositionsX = [-9, -3, 3, 9]  # Allowed positions of the circle
stimOris = [0, 90]               # Possible orientations
stimOris = {'up': 0, 'right': 90}# If particular values goes together with particular response keys

# Timing of stimulus
frameN = {                       # Timing information in monitor frames!
    'trialDuration': 60,
    'onset': 40,
    'offset': 42
}

# Other stuff
pauseInterval = 10           # Pause after this number of trials. For no breaks, set to infinite: pauseInterval = inf
repTrialFactor = 10          # Number of repitions of each unique trial type within a block
saveFolder = 'templateData'  # Log is saved to this folder. The folder is created if it does not exist.
saveCategories = ['ans', 'ansTime', 'onset', 'realDuration', 'score'] # The data fields to be collected for each trial

# Questions and answers.
"""
Note that questions, response options and response keys are combined in
python dictionaries ({'key':value}). Keeping this in standard structures
simplifies stuff by avoiding the introduction of too many variables and
makes it easy to write a single simple function to display all questions,
thus avoiding code duplication.
"""
quitKeys = ['esc', 'escape', 'q']	                  # Keys that immediately quits the experiment
qPos = [0, 3]                            # Position of question message

# Welcome message.
# The u before the string allows for non-ASCII characters.
# The \n makes a new line when text is rendered.
qInstruction = {
    'text': u"""
        Welcome to this PsychoPy experiment.
        You will be shown a very brief striped figure at four different locations.
    \n\nPress UP if the stripes were vertical.
      \nPress LEFT if the stripes were horizontal.
    \n\nKeep your gaze at the fixation cross at all times.
      \nPress RETURN to continue...""",
    'allowedKeys': ['space']                 # Only these keys will be recognized as responses. All other will be ignored. Leave blank ('keys':[]) to accept any response.
}
qPosition = {
    'text': u'Were the stripes vertical (UP) or horizontal (LEFT)?',
    'allowedKeys': ['up', 'left']
}
qPause = {
    'text': u'Pause\nPress SPACE to continue...',
    'allowedKeys': ['space']
}


"""
 SHOW DIALOGUE AND INITIATE PSYCHOPY STIMULI
 This is computationally heavy stuff. Thus we do it in the beginning of our experiment.
"""

# Intro-dialogue. Get subject-id and other variables.
# Save input variables in "V" dictionary (V for "variables")
V = {'id':'', 'order': ['withBlank first', 'noBlank first']}
if not gui.DlgFromDict(V).OK: core.quit()

# Create psychopy window, stimuli, questions and clock
myMon = monitors.Monitor('testMonitor', width=monWidth, distance=monDistance)   # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
myMon.setSizePix(monitorSizePix)
win = visual.Window(monitor=myMon, units='deg', fullscr=True)                   # Initiate psychopy Window as the object "win", using the myMon object from last line.
fix = visual.TextStim(win, '+')                                                 # Fixation cross is just the character "+". Units are inherited from Window when not explicitly specified.
stim = visual.GratingStim(win, mask='gauss', sf=4, size=stimSize, opacity=0.5)  # A Gabor patch
message = visual.TextStim(win=win, pos=qPos, height=1)                          # Message / question stimulus. Will be used to display instructions and questions.
clock = core.Clock()                                                       # A clock wich will be used throughout the experiment to time events on a trial-per-trial basis (stimuli and reaction times).

dataDict = dict(zip(saveCategories, [''] * len(saveCategories)))                # Creates a dictionary with the keys given by the saveCategories variable, declared earlier. This is useful when we make our trials in the createBlock() function.


"""
 FUNCTIONS
"""

def ask(Q):
    """ Ask subject something. Shows question and response options and
    returns answer (keypress) and reaction time"""
    # Show text and fixation cross
    message.setText(Q['text'])
    message.draw()
    fix.draw()          # Fixation cross also drawn with question. It's more relaxing for the subject.
    win.flip()          # Show the stimuli on next monitor update and ...
    clock.reset()  # immediately reset the clock. Reaction time is relative to text onset.

    # Halt everything and wait for responses matching the keys given in the Q object.
    key, rt = event.waitKeys(keyList=Q['allowedKeys'] + quitKeys, timeStamped=clock)[0]
    if key in quitKeys: core.quit()     # Quit everything if quit-key was pressed
    return key, rt    # return (keycode, response_time)


def makeTrials(condition):
    """
    Return a list of trials (list of dictionaries) in advance of actually displaying them.
    A makeTrials('noBlank') with repTrialFactor=2 could generate a trial list like this::

    trials = [
         {'realDuration': '', 'xpos': -9, 'trialDuration': 60, 'ans': '', 'offset': 28, 'onset': 25, 'no': 1, 'ansTime': '', 'id': u'testtest', 'condition': 'withBlanks'},
         {'realDuration': '', 'xpos': 3, 'trialDuration': 60, 'ans': '', 'offset': 28, 'onset': 25, 'no': 2, 'ansTime': '', 'id': u'testtest', 'condition': 'withBlanks'},
         {'realDuration': '', 'xpos': -3, 'trialDuration': 60, 'ans': '', 'offset': 28, 'onset': 25, 'no': 3, 'ansTime': '', 'id': u'testtest', 'condition': 'withBlanks'},
         {'realDuration': '', 'xpos': -9, 'trialDuration': 60, 'ans': '', 'offset': 28, 'onset': 25, 'no': 4, 'ansTime': '', 'id': u'testtest', 'condition': 'withBlanks'},
         {'realDuration': '', 'xpos': 3, 'trialDuration': 60, 'ans': '', 'offset': 28, 'onset': 25, 'no': 5, 'ansTime': '', 'id': u'testtest', 'condition': 'withBlanks'},
         {'realDuration': '', 'xpos': 9, 'trialDuration': 60, 'ans': '', 'offset': 28, 'onset': 25, 'no': 6, 'ansTime': '', 'id': u'testtest', 'condition': 'withBlanks'},
         {'realDuration': '', 'xpos': 9, 'trialDuration': 60, 'ans': '', 'offset': 28, 'onset': 25, 'no': 7, 'ansTime': '', 'id': u'testtest', 'condition': 'withBlanks'},
         {'realDuration': '', 'xpos': -3, 'trialDuration': 60, 'ans': '', 'offset': 28, 'onset': 25, 'no': 8, 'ansTime': '', 'id': u'testtest', 'condition': 'withBlanks'}
    ]

    Calling trials[0] gives the first trial, trials[1] the 2nd trial etc.
    When the experiment executes, it will simply loop over these trials from first to last

    I suggest that you keep all presentation information in trials instead of
    external variables. In that way you know exactly how each trial was presented.
    The problem is never too much data - it's too little data.

    Note that every trial-dictionary should have the same fields. Note also
    that there are placeholders for answers to be collected (e.g. ans and ansTime). We
    defined these fields in the beginning in saveCategories which was later converted
    to dataDict.

    You could use psychopy.data.TrialHandler instead of the code below, which
    would be great for this simple case. But building your trials like below
    is scaleable to more complex cases.
    """

    trials = []
    for xpos in stimPositionsX:
        for ori in stimOris.values():
            blanks = [True, False] if condition == 'withBlank' else [True, True]  ## have just as many blank trials if this is a "withBlank" condition
            for blank in blanks:
                trials += [{'xpos': xpos, 'ori': ori, 'blank': blank}]
    # or: trials = [{'xpos': xpos, 'ori': ori} for xpos in stimPositionsX for ori in stimOris]
    trials = repTrialFactor * trials  # Multiple number of trials for each trial type
    trials = sample(trials, len(trials))  # Randomize trial order (sample all trials)

    """
    Add extra fieds to each trial. Here: dataDict fields (for responses),
    trial fields (trial-specific information defined just above), frames
    (info about onset/offset/trial length) and then 'no', 'id', 'condition'.
    The result is a complete trial description as that shown in the
    description of this function above.
    """
    trials = [dict(dataDict.items() + trial.items() + frameN.items() +
        {'no': i + 1, 'id': V['id'], 'condition': condition}.items())
        for i, trial in enumerate(trials)]

    return trials


def runBlock(condition):
    """Runs a block of trials. Handles everything around the actual stimulus presentation.
    It should then be clear """
    # Get list of trials to loop through and show instruction using our "ask" function.
    trials = makeTrials(condition)
    ask(qPause)

    # Displays trials using our "runTrial(trial) function. Then save data of updated trial using the csvWriter defined above.
    for trial in trials:
        # Prepare trial here, before entering the time-critical period
        if not trial['blank']:
            stim.setPos((trial['xpos'], 0))
            stim.setOri(trial['ori'])

        # Action! Everything is in place. Present trial
        for frame in range(trial['trialDuration']):
            if frame in range(trial['onset'], trial['offset']) and not trial['blank']:  # Note: range(6,9) gives [6,7,8]. 9th will be blank and mark end of stimulus
                stim.draw()  # In "withBlank" condition, somtimes pos=False and stimulus will not get drawn.
            fix.draw()
            win.flip()  # Halts everything until next monitor frame, then updates display. This means that the following lines are executed almost simultaneous with the stimulus display (within a small fraction of a millisecond)

            # Record the actual duration of the stimulus: Set clock to zero immediately after stimulus is displayed. Record time immediately after stimulus disappears (no draw + flip = blank screen)
            if frame is trial['onset']:
                clock.reset()
            if frame is trial['offset']:
                trial['realDuration'] = clock.getTime()

        # Collect responses using our ask(Q) function and score it
        trial['ans'], trial['ansTime'] = ask(qPosition)
        trial['score'] = 1 if stimOris[trial['ans']] == trial['ori'] else 0  # very neat, I think!


        # Save trial and show break message when trial['no'] is a multiple of pauseInterval (% is modulus)
        writer.write(trial)
        if trial['no'] % pauseInterval is 0:
            ask(qPause)


"""
 RUN EXPERIMENT
 Now it's really simple. You simply execute things using the functions ask,
 runBlock, runTrial. Here we order block types given input from dialogue box
"""

writer = ppc.csvWriter(str(V['id']), saveFolder=saveFolder, headerTrial=makeTrials('')[0]) # create writer and write headings to csv.

if V['order'] == 'withBlank first':
    ask(qInstruction)
    runBlock('withBlank')

    ask(qInstruction)
    runBlock('noBlank')
elif V['order'] == 'noBlank first':
    ask(qInstruction)
    runBlock('noBlank')

    ask(qInstruction)
    runBlock('withBlank')
