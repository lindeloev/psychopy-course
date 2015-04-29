# These iohub classes are largely obsolete, now that keyboard.getPresses() etc.
# are implemented in iohub. I keep them here because they do contain useful bits
# for special cases.

class _ioClass(object):
    def __init__(self):
        # Set up iohub and internal clock. Use existing ioHubServer if it exists.
        from psychopy import iohub, core, sys
        self._sys = sys
        self._core = core
        self._timeAtLastReset = core.getTime()

        self._EventConstants = iohub.EventConstants
        existing_iohub = iohub.ioHubConnection.ACTIVE_CONNECTION
        self._io = existing_iohub if existing_iohub else iohub.launchHubServer()

        import numpy
        self._np = numpy

    def _getBaseTime(self, clock=None):
        return self._timeAtLastReset if not clock else clock._timeAtLastReset - self._core.monotonicClock._timeAtLastReset

    def __del__(self):
        self._io.quit()

class Keyboard(_ioClass):
    def __init__(self):
        """
        A iohub-based replacement for psychopy.event.getKeys() and event.waitKeys().
        Allows accurate timing responses during core.wait() and win.flip().
        It also provides information about key release times.

        Typical usage::

            # Somewhere in the beginning of your script do:
            keyboard = ppc.Keyboard()
            # then set up some stuff here

            # Within a visual trial:
            win.callOnFlip(keyboard.reset)  # reference time
            win.flip()  # present stimulus
            # ... and then sometime later in the trial do:
            responses = keyboard.getKeys(keyList=['f', 't', 'RETURN'])
            keyboard.waitKeys(keyList=[' '])  # wait for space

            # Using audio and clock, within an audio trial do:
            beep.play()
            myClock.reset()
            # ... and then sometime later in the trial do:
            responses = keyboard.getKeys(clock=myClock)
        """
        _ioClass.__init__(self)
        self._io.clearEvents('keyboard')

    def reset(self):
        """ clear all keyboard events so far and resets internal clock"""
        self._timeAtLastReset = self._core.getTime()
        self._io.clearEvents('keyboard')

    def getKeys(self, keyList=[], clock=None, releaseAsUnique=False, clearEvents=True):
        """
        Get keyboard events since init or last getKeys(). Returns a list of dictionaries representing keyboard events, e.g.
        [{'key':'j', 'unicode':106, 'tDown':0.54325, 'tUp': 0.588435},  # pressed and released
         {'key':'y', 'unicode':110, 'tDown':0.94325, 'tUp': None}]  # not released yet
            :keyList: a list of strings (key character representations) to register. All other keys will be ignored. An empty list means that all responses will be registered. It is case insensitive.
            :clock: a core.Clock to time events relative to. Defaults to time since init, reset() or last getKeys()
            :releaseAsUnique: whether key release without matching key press are registered.
            :clearEvents: whether to clear the responses (True) or keep them (False)

        This is a wrapper around psychopy.iohub.devices.keyboard.getEvents().
        """
        # Get base time for internal and external clock
        baseTime = self._getBaseTime(clock)
        keys = []  # will be filled with responses
        keyList = [key.lower() for key in keyList]  # make it case insensitive by converting everything to lowercase

        for event in self._io.devices.keyboard.getEvents(clearEvents=clearEvents):
            # If keyList is specified, only register matching responses
            keycode = event.key.lower()
            if not keyList or keycode in keyList:
                # Register keyboard presses
                if event.type == self._EventConstants.KEYBOARD_PRESS:
                    keys += [{
                        'key': keycode,
                        'unicode': event.ucode,
                        'tDown': event.time - baseTime,
                        'tUp': None,
                        'duration': None}]

                # Register keyboard releases - search for first matching keydown without tUp registered.
                elif event.type == self._EventConstants.KEYBOARD_RELEASE:
                    for key in keys:
                        if key['key'] == keycode and not key['tUp']:
                            key['tUp'] = event.time - baseTime  # add release time
                            key['duration'] = key['tUp'] - key['tDown']  # add duration
                            break
                    # If matching keydown wasn't found, register this as a new event without tDown
                    else:
                        if releaseAsUnique:
                            keys += [{
                                'key': keycode,
                                'unicode': event.ucode,
                                'tDown': None,
                                'tUp': event.time - baseTime,
                                'duration': None}]

        return keys

    def waitKeys(self, keyList=[], clock=None, eventType='down', clearEvents=True):
        """
        Halts everything and waits for the first key event of type eventType.
        Calls getKeys() with the arguments. See getKeys() documentation.

        OBS: waitKeys calls reset() at initiation, thus all previous keyboard
        events are cleared and timing is relative to call time if no clock is
        provided.
        """
        # These lines are just selectively copied from getKeys() so that
        # timing is good
        self.reset()
        keyList = [key.lower() for key in keyList]
        if eventType == 'down': event_type_id = self._EventConstants.KEYBOARD_PRESS
        #if eventType == 'up': event_type_id = self._EventConstants.KEYBOARD_RELEASE
        if eventType == 'all': event_type_id = None

        while True:
            for event in self._io.devices.keyboard.getEvents(event_type_id=event_type_id, clearEvents=False):
                if not keyList or event.key.lower() in keyList:
                    return self.getKeys(keyList=keyList, clock=clock, clearEvents=clearEvents)

class Mouse(_ioClass):
    """
    TO DO:
        use named tuples instead of dictionaries? (true of Keyboard class as well!)
        self.mouse should simply be self (and updated with the wrappers)!
        "rate" argument for getPositions and getButtons
    """
    def __init__(self, win, units=None):
        """
        A class to get information about mouse events (clicks, movements etc.).
            :win: a visual.Window()
            :units: units of mouse positions. If None, units are inherited from window
        """
        _ioClass.__init__(self)
        self._io.clearEvents('mouse')
        self._timeAtLastReset = self._core.getTime()
        self.mouse = self._io.devices.mouse
        
        from psychopy import misc
        self._misc = misc
        self.win = win
        self.units = units if units else win.units
        
    def _convertUnits(self, value, newUnit=None, oldUnit='pix'):
        """ Converts coordinates from one unit to another
            :size: is the value to be converted
            :oldUnit: if None it defaults to visual.Window.units
            :newUnit: if None it defaults to visual.Window.units
        """
        # Same same. No need to convert.
        if oldUnit == newUnit:
            return value
        
        # If not specified, use defaults
        if not oldUnit:
            oldUnit = self.win.units
        if not newUnit:
            newUnit = self.units
        
        # PsychoPy uses cm as "global" unit. Convert to cm and then convert to
        # something else. Otherwise the misc-functions would do too much work.
        if oldUnit == 'pix': 
            sizeCm = self._misc.pix2cm(self._np.array(value), self.win.monitor)
        elif oldUnit == 'cm': 
            sizeCm = self._np.array(value)
        elif oldUnit == 'deg': 
            sizeCm = self._misc.deg2cm(self._np.array(value), self.win.monitor)
        elif oldUnit == 'norm': 
            sizeCm = self._misc.pix2cm(self._np.array(value) * self.win.size / 2.0)
        else: 
            raise ValueError('invalid unit %s' %oldUnit)
        
        # Now convert cm to the desired newUnit
        if newUnit == 'cm': 
            return sizeCm
        elif newUnit == 'deg': 
            return self._misc.cm2deg(sizeCm, self.win.monitor)
        elif newUnit == 'pix': 
            return self._misc.cm2pix(sizeCm, self.win.monitor)
        elif newUnit == 'norm':
            return self._misc.cm2pix(sizeCm, self.win.monitor) * 2.0 / self.win.size 
        else:
            raise ValueError('invalid unit %s' %newUnit)

    def reset(self):
        """ clear all keyboard events so far and resets internal clock"""
        self._timeAtLastReset = self._core.getTime()
        self._io.clearEvents('mouse')

    def getPositions(self, clock=None, rate=None, units=None):
        """
        Returns a list of (x, y, time) tuples, representing all positions since first movement since last call.
        Around 100 positions are recorded every second, depending on the system.

        This is a wrapper around psychopy.iohub.devices.mouse.getEvents(self._EventConstants.MOUSE_MOVE).
        See also Mouse.getCurrentPositionAndDelta.
        """
        baseTime = self._getBaseTime(clock)
        trace = []
        events = self.mouse.getEvents(self._EventConstants.MOUSE_MOVE)
        """
        times = self._np.arange(events[0].time, events[-1].time, 1/float(rate))
        pos0x = (events[0].x_position, events[0].y_position)
        for i, event in enumerate(events):
            pass
        """

        for event in events:
            trace += [(self._convertUnits(event.x_position, units), self._convertUnits(event.y_position, units), event.time - baseTime)]

        return trace

    def getButtons(self, buttonList=[], clock=None, releaseAsUnique=False, drag=False, units=None, clearEvents=True):
        """
            :buttonList: ['left', 'middle', 'right', 'scroll'] or a subset.
            :drag: a list of (x, y, time) tuples including the start and endpoint of the drag. None there was no drag or drag=False
                   OBS, if drag=True, processing time increases with around 1-2 ms per second mouse movement recorded.
            :clock: a psychopy.core.Clock relative to which timing is recorded. If None, defaults to internal clock controlled by .reset()
            :units: what unit to return coordinates in. Defaults to Window units.
            :clearEvents: True/False. whether to delete events that are returned.

        This is a wrapper around psychopy.iohub.devices.mouse.getEvents().
        """
        baseTime = self._getBaseTime(clock)

        # Convert buttonList to iohub button_id's
        buttonNames = [None, 'left', 'right', None, 'scroll']  #index of name corresponds to button_id
        if buttonList:
            buttonList = [buttonNames.index(button) for button in buttonList]

        # Get mouse events
        button_events = \
            self.mouse.getEvents(self._EventConstants.MOUSE_BUTTON_PRESS, clearEvents=clearEvents) + \
            self.mouse.getEvents(self._EventConstants.MOUSE_BUTTON_RELEASE, clearEvents=clearEvents)

        # Register them in buttons
        buttons = []
        for event in button_events:
            # If there is a keyList, only register those events (buttons and move - if saveTrace is True)
            if not buttonList or event.button_id in buttonList:
                eventTime = event.time - baseTime

                # Presses
                if event.type == self._EventConstants.MOUSE_BUTTON_PRESS:
                    buttons += [{
                        'posDown': self._convertUnits((event.x_position, event.y_position), units),
                        'posUp': None,
                        'tDown': eventTime,
                        'tUp': None,
                        'duration':None,
                        'id': event.button_id,
                        'button': buttonNames[event.button_id],
                        'drag': None}]

                # Releases - register with matching button-press
                elif event.type == self._EventConstants.MOUSE_BUTTON_RELEASE:
                    for button in buttons:
                        if button['id'] == event.button_id and not button['tUp']:
                            button['tUp'] = eventTime
                            button['duration'] = button['tUp'] - button['tDown']
                            button['posUp'] = self._convertUnits((event.x_position, event.y_position), units)

                            # Include release point as end of drag
                            #if drag:
                            #    button['drag'] += [(event.x_position, event.y_position, event.time - baseTime)]
                            break  # Button found, we can break the for-loop

                    # If no matching button-press is found, optionally register as unique event.
                    else:
                        if releaseAsUnique:
                            buttons += [{
                                'posDown': None,
                                'posUp': self._convertUnits((event.x_position, event.y_position), units),
                                'tDown': None,
                                'tUp': eventTime,
                                'duration': None,
                                'id': event.button_id,
                                'button': button,
                                'drag': None}]

        # Drags (optional) - register with time-matching unreleased button-presses
        # Note: this is kept separate as getEvents(MOUSE_DRAG) is process heavy
        if drag:
            drag_events = self.mouse.getEvents(self._EventConstants.MOUSE_DRAG, clearEvents=clearEvents)
            # For every button, check for matching drag events
            for button in buttons:
                button['drag'] = []  # temporarily. Will be set to None again if no matching drag events were found.
                for event in drag_events:
                    eventTime = event.time - baseTime
                    # This drag event was recorded while this button was pressed
                    if button['tDown'] < eventTime < button['tUp']:
                        pos = self._convertUnits((event.x_position, event.y_position), units)
                        button['drag'] += [(pos[0], pos[1], eventTime)]

                # If drag, include endpoints
                button['drag'] = None if not button['drag'] else [tuple(list(button['posDown']) + [button['tDown']])] + button['drag'] + [tuple(list(button['posUp']) + [button['tUp']])]

        return buttons

    def getState(self, units=None):
        """
        Returns a dictionary with information about the current state of the mouse:
            whether left, right and middle button is down, position, speed, and scroll state.
            :units: yeah...

        This is a wrapper around:
            psychopy.iohub.devices.mouse.getCurrentButtonStates()
            psychopy.iohub.devices.mouse.getPositionAndDelta()
            psychopy.iohub.devices.mouse.getScroll()
        """
        left, middle, right = self.mouse.getCurrentButtonStates()
        pos, posDelta = self.mouse.getPositionAndDelta()
        if self._sys.platform == 'darwin':
            wheelPosX,wheelPosY = self.mouse.getScroll()
        else:
            wheelPosY = self.mouse.getScroll()

        state = {
            'pos': self._convertUnits(pos, units),
            'speed': posDelta,
            'leftDown': left,
            'rightDown': right,
            'middleDown': middle,
            'scroll': wheelPosY
        }
        return state

