'''
This class is the Model for the SuperConductor
project. It stores the state of the program
and registers views to listen for events.
'''

from notify.all import *

class SuperConductorModel:

    def __init__(self):
        self.track = Variable()
        self.current_note = Variable()
        self.volume = Variable()
        self.pitch = Variable()
        self.speed = Variable()
        self.instrument = Variable()

    def register_track_listener(self, listen):
        self.track.changed.connect(listen)

    def register_current_note_listener(self, listen):
        self.current_note.changed.connect(listen)

    def register_volume_listener(self, listen):
        self.volume.changed.connect(listen)

    def register_pitch_listener(self, listen):
        self.pitch.changed.connect(listen)

    def register_speed_listener(self, listen):
        self.speed.changed.connect(listen)

    def register_instrument_listener(self, listen):
        self.instrument.changed.connect(listen)
