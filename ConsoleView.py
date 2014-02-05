'''
This is a testing view for the SuperConductor project
that just prints out received changed value events
to stdout
'''

from SuperConductorModel import SuperConductorModel
from AbstractView import AbstractView
import sys

class ConsoleView(AbstractView):

    def __init__(self, model):
        model.register_track_listener(self.update_track)
        model.register_current_note_listener(self.update_note)
        model.register_volume_listener(self.update_volume)
        model.register_pitch_listener(self.update_pitch)
        model.register_speed_listener(self.update_speed)
        model.register_instrument_listener(self.update_instrument)

    def update_volume(self, volume_level):
        print('Volume updated to: {0}'.format(volume_level))

    def update_pitch(self, pitch_level):
        print('Pitch updated to: {0}'.format(pitch_level))

    def update_speed(self, speed_level):
        print('Speed updated to: {0}'.format(speed_level))

    def update_instrument(self, instrument_number):
        print('Instrument updated to: {0}'.format(instrument_number))

    def update_note(self, note_number):
        print('Note updated to: {0}'.format(note_number))

    def update_track(self, track_name):
        print('Track updated to: {0}'.format(track_name))
