'''
This class is the Model for the SuperConductor
project. It stores the state of the program
and registers views to listen for events.
'''

from notify.all import *
from Globals import Controls, State, GLOBAL, NUM_TRACKS
import midi

class Model:

    def __init__(self):
        self.initVars()
        
        # signals for notification of control change and value changes
        self.control_change = Signal()
        self.value_change = Signal()
        self.state_change = Signal()
        
    def initVars(self):
        # current controlling track
        # values range from 0-16
        # value 0 reserved for global changes

        # current control
        self.current_control = Controls.VOLUME
        self.current_track = GLOBAL
        
        self.current_time = 0
        self.final_time = 0
                
        self.state = State.INIT
        self.fileName = None
        
        # Defaults
        self.default_tempo = 0
        self.default_instruments = [0]*16

        # Controls for all tracks
        self.globals = {}
        
        # Individual parameters for each track
        self.controls = {   Controls.VOLUME: {},
                            Controls.PITCH: {},
                            Controls.TEMPO: {},
                            Controls.INSTRUMENT: {},
                            Controls.PLAY: {} }

        # initialize globals and controls       
        for control in self.controls.keys():
            self.globals[control] = 0
            for track in range(NUM_TRACKS):
                self.controls[control][track] = 0

        self.globals[Controls.PLAY] = 1
        
    def register_control_listener(self, listen):
        self.control_change.connect(listen)

    def register_value_listener(self, listen):
        self.value_change.connect(listen)
              
    def register_state_listener(self, listen):
        self.state_change.connect(listen)

    def set_value(self, value):
        if self.current_track == GLOBAL:
            self.set_global_value(value)
            return
        self.controls[self.current_control][self.current_track] = value
        self.value_change(self.current_control, self.current_track, value)

    def set_global_value(self, value):
        self.globals[self.current_control] = value
        self.value_change(self.current_control, GLOBAL, value)

    def set_control(self, value):
        self.current_control = value
        self.control_change(value)

    def set_state(self, value):
        self.state = value
        self.state_change(value)

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
        self.final_time = self.events[-1].tick
        
        # find and set TEMPO
        for event in self.events:
            if isinstance(event, midi.SetTempoEvent):
                print("Found starting tempo: {0}".format(event.bpm))
                self.default_tempo = event.bpm
                self.globals[Controls.TEMPO] = event.bpm
                break