# -*- coding: utf-8 -*-
"""
SOME WAYS TO HANDLE TRIALS. PICK YOUR FAVOURITE!
    1. using psychopy TrialHandler. If you want it short and easy
    2. using generic python only. When you want maximal control and clean code (my favourite)
    3. using pandas. When you want to calculate/extract cross-trial or cross-category information
    4. using python + pandas. Combines the best from 2. and 3.

All three implementations do the following:
    1. Generate a randomized factorial list of trials (3 images x 2 conditions x 2 repetitions --> 12 trials)
    2. Loop through trials and collect two responses on each
    3. Saves to a csv on a trial-by-trial basis

Benchmark results on my laptop shows that all of them are very quick:
    psychopy:
    generic:
    pandas:

Jonas Lindeløv, 2013.
"""


# -----------------------
# ----- PREPARATION -----
# -----------------------

import random
import time
from ppc import csvWriter

opacities = [0.2, 1.0]
images = ['cat.jpg', 'lion.jpg', 'fish.gif']
reps = 2


"""
1. PSYCHOPY VERSION
  % No ability to save on trial-to-trial basis! (reason enough to discard)
  + Short and simple
  i Suitable for simple factorial designs but not much more
  % Messy output: adds extra columns ("ran" and "order") and floats integers (1 becomes 1.0)
"""

from psychopy import data
conditions = data.createFactorialTrialList({'opacity': opacities, 'image': images})  # tuple list of unique trials
trials = data.TrialHandler(conditions, reps, method='fullRandom')  # as a TrialHandler object with repetitions of trials

for trial in trials:
    trials.addData('answer', random.choice(['left', 'right']))
    trials.addData('score', random.randint(0,1))

trials.saveAsWideText('result_trialHandler (' + time.strftime('%Y-%m-%d %H-%M-%S', time.localtime()) +').csv', appendFile=False)


"""
2. GENERIC PYTHON VERSION
  + good control
  + pure core python (occam's razor)
  % Sensitive to identical keys in all trial-dicts
"""

# Generate trial list
trials = [{'opacity': opacity, 'image': image, 'answer':'', 'score':''}
    for opacity in opacities for image in images for rep in range(reps)]
trials = random.sample(trials, len(trials))
for i, trial in enumerate(trials):
    trial['no'] = i + 1  # randomize and add trial numbers

# Update trials and save
writer = csvWriter('results_manual', '', trials[0])
for trial in trials:
    trial['answer'] = random.choice(['left', 'right'])
    trial['score'] = random.randint(0,1)
    writer.write(trial)


"""
3. PANDAS VERSION
  + Great for analysis of cross-trial data
  % Too complex. Rather do the manual version and convert trials to DataFrame when you need to process data
"""

# Generate trial list
trials = [{'opacity': opacity, 'image': image, 'answer':'', 'score':''}
    for opacity in opacities for image in images for rep in range(reps)]
trials = random.sample(trials, len(trials))

# Convert to pandas
import pandas as pd
trials = pd.DataFrame(trials)
filename = 'result_pandas (' + time.strftime('%Y-%m-%d %H-%M-%S', time.localtime()) +').csv'
for i, trial in trials.iterrows():
    #trials['answer'][i] = random.choice(['left', 'right'])  # more python-like syntax that does the same
    trials.answer[i] = random.choice(['left', 'right'])
    trials.score[i] = random.randint(0,1)
    trials[i:i+1].to_csv(filename, header=True if i == 0 else False, mode='a')  # write data. Write header on first trial.


"""
4. POWER VERSION
When you want all the power you can get or just full control. Useful for staircasing too.
This is a Python-Pandas hybrid: basically the python-version with a pandas dataframe updated "on the side"
"""

# Generate trial list
trials = [{'opacity': opacity, 'image': image, 'answer':'', 'score':''}
    for opacity in opacities for image in images for rep in range(reps)]
trials = random.sample(trials, len(trials))
for i, trial in enumerate(trials):
    trial['no'] = i + 1  # randomize and add trial numbers

writer = csvWriter('results_manual', headerTrial=trials[0])
trialsPD = pd.DataFrame(columns=trials[0].keys())  # a pandas dataframe
for trial in trials:
    # Collect data and save to file
    trial['answer'] = random.choice(['left', 'right'])
    trial['score'] = random.randint(0,1)
    writer.write(trial)  # save to csv

    # Update dataframe and do analysis
    trialsPD = trialsPD.append(trial, True)
    print 'mean score at trial', trial['no'], 'was', round(100 * trialsPD['score'].mean()), '%'
    answerCounts = trialsPD['answer'].value_counts()

