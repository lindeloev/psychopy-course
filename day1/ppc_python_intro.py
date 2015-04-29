# -*- coding: utf-8 -*-
# All scripts starts with the line above. It allows special characters
# to be used in the script without python crashing! E.g. æøåöôé$¤£@§½.
"""
Some python syntax that is relevant for coding psychopy experiments.

The "print" command is used a lot here just to let you look into the machinery
of the code. We're going to use print a lot when building scripts as a diagnostic
tool. But once everything works, we remove them to avoid taking up unnecessary
code / console space / computational resources.

This script runs in way less than 50 ms (a 20th of a second). Base python
is really fast!

Jonas Lindeløv, 2015
"""

print """
--------- VARIABLES AND PRINTING -----------
We're going to rely heavily on variables. We're going to specify all values
in the beginning of our experimental scripts and then use these values throughout
the experiment. In addition, the "print" command is very helpful for diagnosing.
"""
#print theBigElephant  # wouldn't work because it's undefined here
#print globals().keys()  # pre-defined variables

the_big_elephant = 5  # variables can have all sorts of crazy names
print the_big_elephant  # print is your friend!
A_GOAT = 'hello'
aSparrow = A_GOAT + ' mister perfect'  # concatenating (or "adding") strings
print aSparrow
print 'hello' + ' mister perfect'
print the_big_elephant + 4
print A_GOAT, aSparrow, the_big_elephant + 4, ['and', 'a', 'list']
a, b, c = 1, 2, 3
print c, b, a
print type(the_big_elephant), type(A_GOAT), type([1,2,3])  # assess type of variable
print bool, int, float, str, list, tuple, dict  # built-in types of variables (objects)
print 'æøå', u'æøå'  # "u" in front shows special characters appropriately
print 'These variables are defined now:', globals().keys()

"""
Exercise on variables and printing:
     * define a variable and print it

    * define a variable with the value 55 and another with the value 7. Then print
       'one variable is 55 and the other variable is 7. The sum is 62 and the difference is 48'
       ... using the variable values.
     * change the value of the variables and run the script again to verify that it works.

     * try adding a string and an integer using +
       Why is there an error?
       try adding again, this time putting putting str() around the integer.
       Why/how does it work?

    * pro: explore what this does and play with it:
       print 'the number %.2f and %i is %s' %(5.3455, 2.454, 'mighty fine')
"""

# SOLUTIONS:
fun = 5
print fun
number1 = 55
number2 = 7
print 'one variable is', number1, 'and the other variable is', number2, \
    '. The sum is', number1 + number2, 'and the difference is', number1 - number2
#print 'five' + 5
print 'five' + str(5)


print """
----------- LISTS -----------
Lists are an ordered sequence of elements. Just like shopping lists.
The elements can be anything: numbers, strings, lists etc.

We're going to use lists a lot when generating a list of conditions and trials.
"""
# Indexing
my_list = [0, 'hello', [7,2], (1,4), {'goat': 5, 'fish': 2}]
print my_list
print my_list[0]  # why 0? Because it means "shift 0 to the right"
print my_list[0] + my_list[2][1] + my_list[3][0]  # 0 + 2 + 1

# Built-in operations
count = range(5)  # [0, 1, 2, 3, 4]. Notice that range and index starts at zero.
print count
print sum(count), min(count), max(count), len(count)  # works if all elements are numeric
print sum(count) / len(count)  # cheap average

print count[0], count[-1]  # first and last item
print count[:4], count[-4:]  # first and last four items as list

# Modifying lists
count[2] = 99  # change index 2 (third element). Was previously a 2.
count += [11, 12, 13]  # or: count.append(10) or count.append([10, 11, 12])
print count

"""
Exercise on lists:
    * create a list with the numbers 11 through 100, including both.
     * print the first and the last element
     * print index 5 to 15.
     * what is the mean of index 5 to 15?

    * create a list with every fourth number between 200 and 266.
      hint: google "python range" to see the documentation or use spyder :-)

     * try creating a list with some strings.
     * Append a few new strings using the list +=[new, fancy, elements] syntax.

     * pro: make a list and explore sorted(), list.count() and list.remove()
     * pro: range(10) + 5 doesn't work. Try this:
           import numpy as np  # numpy deals with matrices - like MATLAB
           print np.array(range(10)) + 5  # viola!
       Now try to multiply it with an int or maybe even another array? Is it
       matrix multiplication or element-wise?
"""

# SOLUTIONS:
my_list = range(11, 101)
print my_list[0], my_list[-1]
my_string = 'hello world'
print my_string[0], my_string[-1]
print my_list[5:15]
print 'the mean is', sum(my_list[5:15]) / 10  # or len(my_list[5:15])
print range(200, 267, 4)
my_string_list = ['hello', 'python', 'coder']
my_string_list += ['way', 'to', 'go!']
print my_string_list

var = sorted(range(10), reverse=True)
print var.count(5)


print """
------------- DICTIONARIES ------------
Dictionaries are just like real dictionaries. You look up a keyword and
read out the value. There's no ordering so you just access values using keys!
I guess it's like an online dictionary.

We are going to represent a trial using a dictionary. The keys are the
parameters of the trial (duration, condition etc.) including the answers
that we get while running the experiment (reaction time, keys, score etc.).
"""

my_dict = {'first': 2, 'second': 4, 'third': [1, 2, 3], 'fourth': 'goat'}
print my_dict  # notice that order doesn't matter
print my_dict['first']
print my_dict.keys()  # a list of keys
print my_dict.values()  # a list of values

# Modifying dictionaries
my_dict['somethingNew'] = 'a flower'  # add a key-value pair
my_dict['second'] = 99  # if key already exists, just modify value
print my_dict

"""
Exercise on dictionaries and indexing:
    * Make two dictionaries with the keys 'condition' and 'answer' and some values
    * Make a list called "trial_list" with [dictonary1, dictionary2]
    * Print the value of 'condition' in the second dict by indexing trial_list.
      Hint: first index the list to get the dictionary and
      then the dictionary to get the value.
    * extend each of the two dictionaries with the key 'subject' and some values
      hint: dict['newValue']=something or dict.update({'key':value}) or...

    * pro: another way of "adding" multiple dictionaries in one line is
      newDict = dict(dict1.items() + dict2.items())  # ... and so on
      what does the .items() do and why can we add them?
"""

# SOLUTIONS
dict1 = {'condition': 'fun', 'answer': False}
dict2 = {'condition': 'boring', 'answer': True}
trial_list = [dict1, dict2]
print trial_list[1]['condition']
dict1.update({'subject': 'jonas'})
dict2.update({'subject': 'bodil'})
print dict(dict1.items() + dict2.items())



print """
---------- LOOPING ----------
Looping allows you to run the same code using different parameter(s).

We're going to loop over individual trials during the experiment.
We also pre-create the trials in a loop.
Finally, we time visual stimuli to monitor frames using a "flip-loop"
in which every iteration is synchronized to the monitor update.
"""
# for-loop
for i in range(4):
    print 'iteration number', i
my_list = ['a', 'fancy', 'goat']
for i, word in enumerate(my_list):
    print 'index', i, 'has the value', word

# cool syntax #1: for-else
for i in range(4):
	if i == 5:
		print 'that was a five!'
		break
else:
	print 'five not found'

# cool syntax #2: for-list (list comprehension)
fancy_goat = [i * 2 for i in [1, 5, 8]]
print fancy_goat

# Generate a list of trials!
trial_list = []
for condition in ['fun', 'meh', 'boring']:
    for duration in [2, 4, 6]:
        trial_list += [{'condition': condition, 'duration': duration}]
print trial_list

# while-loop.
counter = 1
while counter <= 4:
    print 'still true on iteration number', counter
    counter += 1
    #if counter > 2:
    #    break  # break stops the loop. You can use "while True" and then
                # end the loop using break.


"""
Exercise on lists and loops:
    * Make a for-loop over this list and print each word within the loop:
      ['just', 'looping', 'and', 'looping', 'and', 'looping']

    * Now loop over trial_list which we defined earlier!
      Outside (above) the loop, define a variable called "subjectID" with your surname.
      Modify each trial within the loop so that each dictionary has a key
      'subject' with your name (the value of subjectID).
    * Add the keys 'ans' (answer) and 'rt' (reaction time) to each trial
      (dictionary) with '' (empty string) as values.
      trial['rt'] = ''
      They are placeholders for the subject's answers when we run the experiment.

    * Pros: make the same trial_list using the trial_list = [value for var in list] syntax.
      hint: value is a dictionary
"""

# SOLUTIONS:
for a_fancy_goat in ['just', 'looping', 'and', 'looping', 'and', 'looping']:
    print a_fancy_goat

subjectID = 'jonas'
for trial in trial_list:
    trial['name'] = subjectID
    trial['ans'] = ''
    trial['rt'] = ''
    print trial

# Method 1 (brief)
trial_list = [{'condition':condition, 'repetition':N} for condition in ['exiting', 'boring'] for N in range(10)]
print trial_list

# Method 2 (easier to understand)
trial_list = []
for condition in ['exciting', 'boring']:
    for repetition in range(10):
        trial_list += [{'condition': condition, 'repetition':repetition}]

		
print """
-------- LOGIC ----------
Logic is really simple. Something is either True of False. Nothing else.
Python logic is usually very easy to understand if you read it aloud. E.g.
"is 5 equal to 6?"
"is 8 smaller than 6 or larger than 6?"

We're mostly going to use logic to display stimuli differently based
on some condition. We're also going to use it to score trials.
"""
# keywords: True, False, if, elif, else
# and combination of logic: not, and, or, is
if True:
    print 'True -->', True
if False:
    print 'False -->', False

# prints the result of a lot of logical tests
print 'not True -->', not True
print 'True and false -->', True and False
print 'False or True -->', False or True
print '1 == 1 -->', 1 == 1
print '1 is 1 -->', 1 is 1
print '1 == 2 or 1 == 2 -->', 1 == 2 or 1 == 2
print 'the_big_elephant == 3 + 2 -->', the_big_elephant == 3 + 2
print '2 < 5 < 4 -->', 2 < 5 < 4

# Running code dependent on conditions
if False:
    print 'false'
elif False or False:
    print 'False or False'
else:
    print 'else...'

# A short and convenient way to assign values dependent on conditions
my_test = 'horse' if 1 == 2 else 'goat'  # useful for scoring trials!
my_test2 = 'horse' if 1 == 2 else 'goat' if False or True else 'sparrow'
print my_test, my_test2  # goat goat


"""
Exercise on logic:
    * Is the following True or False?
      5 < 8
    * What about
      5 < 8 and 5 + 2 == 6
    * Then what about
      5 < 8 and 5 + 2 == 6 or 'horse' == 'goat' or range(3) == [0, 1, 2]

    * Define a variable called "do_test" and set it to True.
      Then use an if-statement and run the above three tests if do_test is True
    * Your participant responds either 'left', 'right' or something else.
      Print different things depending on her response.

    * Pros: determine whether empty lists, strings and dictionaries
      are interpreted as False in a logical test.
      Hint: You can coerce variables into boolean type using the bool() method.
"""

# SOLUTIONS
do_test = True
if do_test:
    print 5 < 8
    print 5 < 8 and 5 + 2 == 6
    print 5 < 8 and 5 + 2 == 6 or 'horse' == 'goat' or range(3) == [0, 1, 2]

response = 'up'
if response == 'left':
    print 'she pressed left!'
elif response == 'right':
    print 'she pressed right!'
else:
    print 'she pressed something else :-('

# Pro: the truth value of empty vs. non-empty stuff
print bool(''), bool('left')
print bool(0), bool(99)
print bool([]), bool([5,8])
print bool({}), bool({'hi':2})



print """
----- METHODS (FUNCTIONS) -------
Methods run a segment of code anywhere you'd like. It's useful for code-reuse and
it helps you to keep your code clean and consistent.

We're going to create two methods in the experiment. A runBlock(condition) and a
makeTrialList(condition).
"""
# a chunk of code that can be run using a single command, usually returning something
def add_plus_one(a, b):
    a += 1
    b += 1
    return a + b

two_plus_three = add_plus_one(2, 3)  # method returns 7 (2+1 + 3+1) and assigns to var
print two_plus_three
five_plus_ten = add_plus_one(5, 10)  # 17
print five_plus_ten
add_plus_one(10, 10)  # output is not assigned to anything and thus does nothing

# default values!
def add_plus_X(a, b=2, x=1):
    return a + b + 2*x

print add_plus_X(1)
print add_plus_X(0, x=5)
print add_plus_X(5, 10)  # no keywords uses default order

"""
Exercise on methods:
    * Define a method that takes a string as input and returns the first
      and last character of it as a single string.
      Hint: indexing works on strings!
    * Try printing the output.
    * Save the output to a variable and print it.

    * Define a method that takes a number as input and returns 'too low', 'just right'
	  or 'too high' depending on the size of the number. You choose the criteria!
    * Modify your method so that you can specify the criteria as
      arguments with default values.

    * Pros: make a method "makeTrialList" that takes a condition as input
      and returns a trial_list. You decide what kind of trials you want and
      what difference the condition makes for the generation of the trial_list.
"""

# SOLUTIONS
def fancy_string(string):
    return string[0], string[-1]
print fancy_string('Hello World')

def evaluate_magnitude(number, below=2, above=7):
    if number < below:
        return 'too low'
    elif number > above:
        return 'too high'
    else:
        return 'just right!'
print evaluate_magnitude(5)
print evaluate_magnitude(6, above=5)

# You can make multiline strings
common_mistakes = """
---------- COMMON MISTAKES ----------
Here is a list of simple common mistakes. Remember:
    * every character counts. A single typo/ommision causes the script to crash.
    * the script runs from the top and down. Things not defined yet cannot be referenced (used).

Python is really helpful to let you debug errors.
    * in every error, the top line tells you the line at which the error
      occurred. You probably mistyped something.
    * in every error, the bottom line tells you the type of error. Examples:
        * NameError: the variable is not defined above.
              myVariable = 2
              print myvariable  # doesn't exist because python is case sensitive

        * TypeError: the variables are of different types and you did something illegal.
              my_list = [1,2,3]
              myString = 'hello world'
              print my_list + myString  # TypeError

        * SyntaxError: the line didn't follow the python syntax.
              my Variable = 2  # SyntaxError. variables cannot contain spaces!
              for i in range(10)   # SyntaxError. forgot colon!
                  print i 'is a number'  # SyntaxError. Space is not an operation!

        * IndexError: you called a list index which does not exist.
              list = [1,2,3]
              print list[7]  # IndexError
        * KeyError: you called a dictionary key which does not exist.
              dict = {'name': 'jonas'}
              print dict['age']  # KeyError

    * more generally, see http://i.imgur.com/WRuJV6r.png
    * for the pros, see http://stackoverflow.com/questions/1011431/common-pitfalls-in-python
"""

"""
Exercise on errors:
    Commit the errors above, just to see that it "works".
    Note the type of error and line number of the error. Useful stuff for debugging!
"""

# There's a lot of useful built-in operations on each variable type. Let's
# play with the string above.
print common_mistakes.count('c')  # counts number of small c's in the text above.
print common_mistakes.split('\n')[3]  # a list of lines. Prints 4th line.
cm_words = common_mistakes.split(' ')  # a list of words.
print cm_words[1].lower()  # lowercase. prints 'common' instead of 'COMMON'


print """
--- COMBINING STUFF ------'
We often combine multiple sequential commands in one line. It works because
each command simply returns an output on which the next operation takes as input.
For example:
"""
print common_mistakes.split('\n')[1][2].capitalize().startswith('a')
"""
... returns False because:
    * common_mistakes.split('\n') returns a list with individual lines.
    * [1] gets the second line, "Here's a list of simple..."
    * [2] gets the third character of that line, 'r'
    * .capitalize() makes it capitalized, 'R'
    * .startswith('a') tests whether the first character in 'R' equals 'a'.
       i.e. 'R'[0] == 'C' --> False
"""


print '\n -------- MATH -----------'
print 5 / 2  # is 2 in python 2.x
print 5 / 2.0, float(5) / 2  # is 2.5 because there's a float. Tip: use "from __future__ import division"
print 1 + 2*2**3 - 1/5.0  # Python follows the order of operations
print 1 + (2*2)**(3 - 1) / 5.0  # Paranthesis prevail over other operations!
print 10 % 2  # modulus
# Style note: spacing in math should be used to make it easier to read by
# bringing primary operations closer together than lower operations.


print '\n ------ PICKING RANDOM ELEMENTS -------'
import random  # import a module
funny_list = ['one', 'mighty', 'fine', 'horse']
print random.choice(funny_list)  # picks one
print random.sample(funny_list, 3)  # picks three
print random.sample(funny_list, len(funny_list))  # randomizes order!


"""
---------------------------------------------------------
If you found the above very challenging, just stop here.
The below code is for the geeks / over-achievers.
---------------------------------------------------------
"""

print '\n ------- NUMPY ----------'
# Numpy module contains a lot of useful stuff
import numpy as np
print np.sin(np.pi), np.cos(2 * np.pi)
print np.ceil(3.6), np.floor(3.6)
print np.log(np.exp(3)), np.log2(4)  # logarithms
print np.abs(-5)  # absolute value

# Randomness
print np.random.randint(3, 7, 5)  # 5 random integers from [3, 4, 5, 6]
print np.random.randint(0, 2, 5)  # 5 random 1's and 0's (True and False!)
print np.random.uniform(0, 1, 5)  # 5 numbers between 0 and 1
print np.random.normal(5, 2, 5)  # 5 numbers with mu=5, sd=2

# MATLAB like operations on full array (and matrix calculations)
# print range(10) + 5  # won't work in classical python
print np.array(range(10)) + 5  # [5, 6, ...]
print np.array([1,2,3]) * np.array([1,2,3])  # elementwise: [1, 4, 9]


print '\n --- SOME CROSS-TYPE CONSISTENSIES ---'
# Adding / extending using '+' sign
print 'hello' + 'world'
print ['hello'] + ['world']
print dict({'a':'hello'}.items() + {'b':'world'}.items())

# Emptiness and 0 is False. Anything else is True
print bool([]), bool(''), bool({}), bool(0)  # emptiness and 0
print bool([0]), bool('False'), bool({'0': 0}), bool(-1)

# Counting number of elements using len() which is the same as .__len__()
print len('fun'), len([1,2,3]), len({'a':1, 'b':2, 'c':3})  # 3 3 3
print 'fun'.__len__(), [1,2,3].__len__(), {'a':1, 'b':2, 'c':3}.__len__()  # 3 3 3


print '\n -- IDENTITY/REFERENCE VERSUS SIMILARITY --'
# "is" tests for reference and is more strict than "==" which tests for similarity.
# Identical primitives are the same and therefore similar.
print 99 is 99, 'a' is 'a', (5) is (5)  # True True True
print 99 == 99, 'a' == 'a', (5) == (5)  # True True True

# Similar lists, tuples and dicts are not the same
print [99] is [99], {'a': 4} is {'a': 4}, (5,2) is (5,2)  # False False False
print [99] == [99], {'a': 4} == {'a': 4}, (5,2) == (5,2)  # True True True

# The same is true for variables
goat = [1, 2, 3]
goat_reference = goat  # reference to goat
goat_wannabe = [1, 2, 3]  # just a similar object
goat_copy = goat[:]  # useful way of copying a list!
print 'goat is goat1Reference -->', goat is goat_reference  # True
print 'goat is goat1Wannabe -->', goat is goat_wannabe  # False
print 'goat == goat_wannabe -->', goat == goat_wannabe  # True
print 'goat is goat_copy -->', goat is goat_copy  # False
print 'goat == goat_copy -->', goat == goat_copy  # True

# Reference is really useful but also source of much confusion when changing referring variables
goat[2] = 'surprise!'  # goat_reference is 'changed' here as well because it is simply a reference to goat
print goat, goat_reference, goat_wannabe
