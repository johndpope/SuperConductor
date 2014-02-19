'''
This class is the Model for the SuperConductor
project. It stores the state of the program
and registers views to listen for events.
'''

from notify.all import *
from Globals import Controls, GLOBAL, NUM_TRACKS
import midi

class Model:

    def __init__(self):
        # current controlling track
        # values range from 0-16
        # value 0 reserved for global changes

        # current control
        self.current_control = Controls.VOLUME
        self.current_track = GLOBAL

        self.controls = {   Controls.VOLUME: {},
                            Controls.PITCH: {},
                            Controls.TEMPO: {},
                            Controls.INSTRUMENT: {},
                            Controls.PLAY: {} }



        # initialize controls
        for control in self.controls.keys():
            for track in range(NUM_TRACKS + 1):
                self.controls[control][track] = 0

        self.controls[Controls.PLAY][GLOBAL] = 1

        # signals for notification of control change and value changes
        self.control_change = Signal()
        self.value_change = Signal()

    def register_control_listener(self, listen):
        self.control_change.connect(listen)

    def register_value_listener(self, listen):
        self.value_change.connect(listen)

    def set_value(self, value):
        self.controls[self.current_control][self.current_track] = value
        self.value_change(self.current_control, self.current_track, value)

    def set_global_value(self, value):
        self.controls[self.current_control][GLOBAL] = value
        self.value_change(self.current_control, GLOBAL, value)

    def set_control(self, value):
        self.current_control = value
        self.control_change(value)

    def set_track(self, value):
        self.current_track = value % NUM_TRACKS
        self.value_change(Controls.TRACK, value, value)

    # Loads a midi file
    def load_file(self, filename):
        self.pattern = midi.read_midifile(filename)
        self.pattern.make_ticks_abs()
        self.inistialResolution = self.pattern.resolution
        self.events = []
        for track in self.pattern:
            for event in track:
                self.events.append(event)

        self.events.sort()

        # find and set TEMPO
        for event in self.events:
            if isinstance(event, midi.SetTempoEvent):
                self.controls[Controls.TEMPO][GLOBAL] = event.bpm
                break