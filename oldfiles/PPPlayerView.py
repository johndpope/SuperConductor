'''
This view for the SuperConductor project
implements a MIDI file self.player. Received changed value 
self.events are reflected in the generated sound output.
'''

from SuperConductorModel import SuperConductorModel
from AbstractView import AbstractView

import pygame.midi
import midi
import sys
import threading
import time

class PPPlayerView(AbstractView):

    def __init__(self, model):
        pygame.midi.init()
        model.register_track_listener(self.update_track)
        model.register_current_note_listener(self.update_note)
        model.register_volume_listener(self.update_volume)
        model.register_pitch_listener(self.update_pitch)
        model.register_speed_listener(self.update_speed)
        model.register_instrument_listener(self.update_instrument)
        self.velocity_offset = [0]*16
        self.pitch_offset = [0]*16
        self.exited = False
        self.player = None
        self.thread = None
        self.events = None
        self.pattern = None
        self.secPerTick = .0005  # set it until we see a tempo event
        self.paused = False
    
    # Loads a midi file
    def load_file(self, filename):
        self.pattern = midi.read_midifile(filename)
        self.pattern.make_ticks_abs()
        self.inistialResolution  = self.pattern.resolution
        self.events = []
        for track in self.pattern:
            for event in track:
                self.events.append(event)

        self.events.sort()

    # Stars playing back the file in a new self.thread
    # (A file must be loaded first)
    def play(self):
        self.thread = threading.Thread(target=self.mplay)
        self.thread.daemon = True
        self.thread.start()        
    
    def pause(self):
        self.paused = True
    
    def cont(self):
        self.paused = False
    
    # Stops playing the current track
    def stop(self):
        self.exited = True
    
    def update_volume(self, volume_level, track):
        self.velocity_offset[track-1] = volume_level
    
    def update_pitch(self, pitch_level, track):
        self.pitch_offset[track-1] = pitch_level

    # Sets tempo of the track.      
    def update_speed(self, speed_level):
        self.pattern.resolution = self.inistialResolution + speed_level
        mpb = 60.0 * 1000000.0 / self.tempo
        mpt = mpb / self.pattern.resolution
        self.secPerTick = mpt / 1000000.0
    
    # Changes the midi instrument on the specified track.
    # Only works AFTER playback has started.
    def update_instrument(self, instrument_number, track):
        self.player.set_instrument(instrument_number, track);
    
    def update_note(self, note_number):
        pass
    
    def update_track(self, track_name):
        pass

    # Should not be called directly
    def mplay(self):
        self.player = pygame.midi.Output(0)
    
        # Store notes that have been played, so we know what they were when we turn them off
        notes = {}        
        delta = 0
        tickTime = 0
        for event in self.events:
            delta = event.tick - tickTime
            tickTime = event.tick
            while self.paused:
                pass
            if self.exited:
                self.exited = False
                break
            if delta:
                time.sleep(delta * self.secPerTick)
            if isinstance(event, midi.NoteOnEvent):
                key = (event.pitch, event.channel)
                notes[key] = event.pitch+self.pitch_offset[event.channel-1]
                # Don't offset the velocity if it is 0.
                velocity = event.velocity+self.velocity_offset[event.channel-1] if event.velocity > 0 else 0
                self.player.note_on(notes[key], velocity, event.channel)
            elif isinstance(event, midi.NoteOffEvent):
                key = (event.pitch, event.channel)
                self.player.note_off(notes[key], event.velocity, event.channel)
            elif isinstance(event, midi.ProgramChangeEvent):
                self.player.set_instrument(event.value, event.channel)
            elif isinstance(event, midi.SetTempoEvent):
                # convert tempo to secPerTick
                self.tempo = event.bpm
                mpb = 60.0 * 1000000.0 / self.tempo
                mpt = mpb / self.pattern.resolution
                self.secPerTick = mpt / 1000000.0

        self.player.close()
        
