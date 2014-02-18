'''
This view for the SuperConductor project
implements a MIDI file self.player. Received changed value 
self.events are reflected in the generated sound output.
'''

from scm import Model
from AbstractView import AbstractView
from Globals import Controls, GLOBAL

import pygame.midi
import midi
import sys
import threading
import time

class PPPlayerView(AbstractView):

    def __init__(self, model):
        pygame.midi.init()
        model.register_control_listener(self.update_control)
        model.register_value_listener(self.update_value)
        self.exited = False
        self.player = None
        self.thread = None
        self.model = model
        self.secPerTick = self.tempo_to_spt(self.model.controls[Controls.TEMPO][GLOBAL])

    # Starts playing back the file in a new self.thread
    # (A file must be loaded first)
    def play(self):
        self.thread = threading.Thread(target=self.mplay)
        self.thread.daemon = True
        self.thread.start()
    
    # Stops playing the current track
    def stop(self):
        self.exited = True
    
    def update_control(self, value):
        pass

    def update_value(self, control, track, value):
        if(control == Controls.INSTRUMENT):
            self.player.set_instrument(value, track);
        elif (control == Controls.TEMPO):
            self.secPerTick = self.tempo_to_spt(value)

    def tempo_to_spt(self, tempo):
        if tempo <= 0:
            return .001
        # convert tempo to secPerTick
        mpb = 60.0 * 1000000.0 / tempo
        mpt = mpb / self.model.pattern.resolution
        secPerTick = mpt / 1000000.0
        return secPerTick

    # Should not be called directly
    def mplay(self):
        self.player = pygame.midi.Output(0)
        model = self.model
    
        # Store notes that have been played, so we know what they were when we turn them off
        notes = {}
        delta = 0
        tickTime = 0
        for event in model.events:
            delta = event.tick - tickTime
            tickTime = event.tick
            while not model.controls[Controls.PLAY][GLOBAL]:
                pass
            if self.exited:
                self.exited = False
                break
            if delta:
                time.sleep(delta * self.secPerTick)
            if isinstance(event, midi.NoteOnEvent):
                key = (event.pitch, event.channel)

                # record mapping of actual note to note played
                notes[key] = event.pitch \
                            + model.controls[Controls.PITCH][event.channel+1] \
                            + model.controls[Controls.PITCH][GLOBAL]

                # Don't offset the velocity if it is 0.
                velocity = event.velocity \
                            + model.controls[Controls.VOLUME][event.channel + 1] \
                            + model.controls[Controls.VOLUME][GLOBAL] \
                            if event.velocity > 0 else 0

                # limit pitch and velocity to their ranges
                notes[key] = min(max(notes[key], 0), 127)
                velocity = min(max(velocity, 0), 127)

                self.player.note_on(notes[key], velocity, event.channel)
            elif isinstance(event, midi.NoteOffEvent):
                key = (event.pitch, event.channel)
                self.player.note_off(notes[key], event.velocity, event.channel)
            elif isinstance(event, midi.ProgramChangeEvent):
                self.player.set_instrument(event.value, event.channel)
            elif isinstance(event, midi.SetTempoEvent):
                # convert tempo to secPerTick
                self.secPerTick = self.tempo_to_spt(event.bpm)

        self.player.close()
        
