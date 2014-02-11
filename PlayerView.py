'''
This view for the SuperConductor project
implements a MIDI file player. Received changed value 
events are reflected in the generated sound output.
'''

from SuperConductorModel import SuperConductorModel
from AbstractView import AbstractView

from mido.midifiles import MidiFile
import pygame.midi
import threading
import sys

# Global Variables
VELOCITY_OFFSET = [0]*16
PITCH_OFFSET = [0]*16
EXITED = False
PLAYER = None
PARSER = None
THREAD = None

class PlayerView(AbstractView):

    def __init__(self, model):
        model.register_track_listener(self.update_track)
        model.register_current_note_listener(self.update_note)
        model.register_volume_listener(self.update_volume)
        model.register_pitch_listener(self.update_pitch)
        model.register_speed_listener(self.update_speed)
        model.register_instrument_listener(self.update_instrument)
    
    # Loads a midi file
    def load_file(self, filename):
        global PARSER
        PARSER = MidiFile(filename)
    
    # Stars playing back the file in a new thread
    # (A file must be loaded first)
    def play(self):
        global THREAD, PARSER
        THREAD = threading.Thread(target=self.mplay)
        THREAD.daemon = True
        THREAD.start()        
    
    def pause(self):
        # TODO: Implement
        pass
    
    def cont(self):
        # TODO: Implement
        pass
    
    # Stops playing the current track
    def stop(self):
        global EXITED
        EXITED = True
    
    def update_volume(self, volume_level, track):
        global VELOCITY_OFFSET
        VELOCITY_OFFSET[track-1] = volume_level
    
    def update_pitch(self, pitch_level, track):
        global PITCH_OFFSET
        PITCH_OFFSET[track-1] = pitch_level

    # Sets tempo of the track. Only works when updated before playback starts.
    # Tempo is ratio of default speed:
    # 1 is default speed, 0.5 is half speed, 2 is double speed, etc.        
    def update_speed(self, speed_level):
        global PARSER
        PARSER.ticks_per_beat = int(480 * speed_level)
    
    # Changes the midi instrument on the specified track.
    # Only works AFTER playback has started.
    def update_instrument(self, instrument_number, track):
        global PLAYER
        PLAYER.set_instrument(instrument_number, track);
    
    def update_note(self, note_number):
        pass
    
    def update_track(self, track_name):
        pass

    # Should not be called directly
    def mplay(self):
        global PLAYER, PARSER, VELOCITY_OFFSET, PITCH_OFFSET, EXITED
        pygame.midi.init()
        PLAYER = pygame.midi.Output(0)
    
        # Store notes that have been played, so we know what they were when we turn them off
        notes = {}
        for message in PARSER.play():
            if EXITED:
                EXITED = False
                break
            elif message.type == "note_off" or (hasattr(message, 'velocity') and message.velocity == 0):
                key = (message.note, message.channel)
                PLAYER.note_off(notes[key], message.velocity, message.channel)
            elif message.type == "note_on":
                key = (message.note, message.channel)
                notes[key] = message.note+PITCH_OFFSET[message.channel-1] 
                PLAYER.note_on(notes[key], message.velocity+VELOCITY_OFFSET[message.channel-1], message.channel)
            elif message.type == "program_change":
                PLAYER.set_instrument(message.program, message.channel) 

        PLAYER.close()
        
