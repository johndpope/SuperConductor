'''
This view for the SuperConductor project
implements a MIDI file self.player. Received changed value 
self.events are reflected in the generated sound output.
'''

from scm import Model
from AbstractView import AbstractView
from Globals import Controls, State, GLOBAL

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
        model.register_state_listener(self.update_state)
        self.exited = False
        self.paused = False
        self.player = None
        self.thread = None
        self.model = model
        self.secPerTick = self.tempo_to_spt(self.model.controls[Controls.TEMPO][GLOBAL])

    # Starts playing back the file in a new self.thread
    # (A file must be loaded first)
    def play(self):
        self.waitevent = threading.Event()  # call self.waitevent.set() to interrupt
        self.thread = threading.Thread(target=self.mplay)
        self.thread.daemon = True
        self.thread.start()
    
    # Stops playing the current track
    def stop(self):
        self.waitevent.set()
        self.exited = True
    
    def pause(self):
        self.waitevent.set()
        self.paused = True
        
    def resume(self):
        self.waitevent.set()
        self.paused = False 
    
    def update_control(self, value):
        pass

    def update_value(self, control, track, value):
        if(control == Controls.INSTRUMENT):
            self.player.set_instrument(value, track);
            print("Instrument {0} on track {1}".format(value, track))
        elif (control == Controls.TEMPO):
            self.secPerTick = self.tempo_to_spt(value)

    def update_state(self, state):
        print "State: ", state
        if (state == State.READY):
            self.puased = False
            self.exited = False
        elif (state == State.PLAY):
            if self.paused:
                self.resume() 
            else:
                if (self.model.fileName != None):
                    self.play()
        elif (state == State.PAUSE):
            self.pause()
        elif (state == State.STOP):
            self.stop()

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
            model.current_time = event.tick
            delta = event.tick - tickTime
            tickTime = event.tick
            while not model.globals[Controls.PLAY]:
                pass
            if self.paused:
                for key in notes.keys():
                    self.player.note_off(notes[key], 0, key[1])
                """    
                while self.paused and not self.exited:
                    time.sleep(1)
                """
                self.waitevent.clear()
                self.waitevent.wait()
                          
                if not self.exited:
                    for key in notes.keys():
                        self.player.note_on(notes[key], 0, key[1])
            if self.exited:
                self.paused = False
                self.exited = False
                break
            if delta:
                # time.sleep(delta * self.secPerTick)
                self.waitevent.clear()
                self.waitevent.wait(delta * self.secPerTick)
            if isinstance(event, midi.NoteOnEvent):
                key = (event.pitch, event.channel)

                # 'Convert' note on events with velocity 0 to note off events
                if event.velocity == 0:
                    self.player.note_off(notes[key], event.velocity, event.channel)
                    continue
                
                # record mapping of actual note to note played
                # Don't add a global offset to track 10, so percussion doesn't change
                if event.channel == 9:
                    global_pitch_offset = 0
                else:
                    global_pitch_offset = model.globals[Controls.PITCH]
                
                notes[key] = event.pitch \
                            + model.controls[Controls.PITCH][event.channel] \
                            + global_pitch_offset

                velocity = event.velocity \
                             + model.controls[Controls.VOLUME][event.channel] \
                             + model.globals[Controls.VOLUME]

                # limit pitch and velocity to their ranges
                notes[key] = min(max(notes[key], 0), 127)
                velocity = min(max(velocity, 0), 127)

                self.player.note_on(notes[key], velocity, event.channel)
            elif isinstance(event, midi.NoteOffEvent):
                key = (event.pitch, event.channel)
                if key not in notes: 
                    continue
                self.player.note_off(notes[key], event.velocity, event.channel)
            elif isinstance(event, midi.ProgramChangeEvent):
                # Save instrument change so it is reflected in the UI
                model.controls[Controls.INSTRUMENT][event.channel] = event.value
                model.default_instruments[event.channel] = event.value
                self.player.set_instrument(event.value, event.channel)
            elif isinstance(event, midi.SetTempoEvent):
                # convert tempo to secPerTick
                tempo_offset = model.globals[Controls.TEMPO] - model.default_tempo
                model.default_tempo = event.bpm
                model.globals[Controls.TEMPO] = event.bpm + tempo_offset
                self.secPerTick = self.tempo_to_spt(event.bpm + tempo_offset)
            elif not (isinstance(event, midi.MetaEvent) or isinstance(event, midi.SysexEvent)):
                # channel = event.channel if hasattr(event, 'channel') else 0
                # print("Status: {}, Channel: {}, Data 0: {}, Data 1: {}".format(
                #         event.statusmsg, channel, event.data[0], event.data[1]))
                self.player.write([[[event.statusmsg + event.channel, event.data[0], event.data[1]],0]])

        self.player.close()
        
