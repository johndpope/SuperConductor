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
        sys.stdout.write('Volume updated to: {0}          \r'.format(volume_level))

    def update_pitch(self, pitch_level):
        sys.stdout.write('Pitch updated to: {0}          \r'.format(pitch_level))

    def update_speed(self, speed_level):
        sys.stdout.write('Speed updated to: {0}          \r'.format(speed_level))

    def update_instrument(self, instrument_number):
        sys.stdout.write('Instrument updated to: {0}          \r'.format(instrument_number))

    def update_note(self, note_number):
        sys.stdout.write('Note updated to: {0}          \r'.format(note_number))

    def update_track(self, track_name):
        sys.stdout.write('Track updated to: {0}          \r'.format(track_name))

