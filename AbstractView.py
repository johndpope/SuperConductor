'''
This file is an abstract class defining the methods
that must be implemented for a view in the SuperConductor
project
'''

from abc import ABCMeta, abstractmethod

class AbstractView(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_volume(self, volume_level):
        pass

    @abstractmethod
    def update_pitch(self, pitch_level):
        pass

    @abstractmethod
    def update_speed(self, speed_level):
        pass

    @abstractmethod
    def update_instrument(self, instrument_number):
        pass

    @abstractmethod
    def update_note(self, note_number):
        pass

    @abstractmethod
    def update_track(self, track_name):
        pass
    
