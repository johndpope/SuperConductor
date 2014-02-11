# UW CSE 481 Sound Capstone
# Requires Mido and Pygame external libraries

# SuperConductor, basic MIDI file player and manipulator

from mido.midifiles import MidiFile
import pygame.midi
import threading

# Global Variables
VELOCITY_OFFSET = [0]*16
PITCH_OFFSET = [0]*16
EXITED = False
PLAYER = None
PARSER = None
THREAD = None

# Loads a midi file
def load_file(filename):
    global PARSER
    PARSER = MidiFile(filename)

# Stars playing back the file in a new thread
# (so we can continue to use this thread to change playback parameters)
def play():
    global THREAD
    THREAD = threading.Thread(target=mplay)
    THREAD.daemon = True
    THREAD.start()
    
def stop():
    global EXITED
    EXITED = True
    
def pause():
    # TODO: Implement
    pass

def set_pitch_offset(p_offset, track):
    ## TODO: Restrict to octaves? (multiples of 12)
    # Specify a track. (change PITCH_OFFSET to an array of pitch offsets for each track)
    # Validate input is within acceptable range
    # Offsetting by other values can make it sound bad, but might be more interesting
    global PITCH_OFFSET
    PITCH_OFFSET[track-1] = p_offset

def set_velocity_offset(v_offset, track):
    ## TODO: Validate input is within acceptable range
    # Specify a track. (change VELOCITY_OFFSET to an array of pitch offsets for each track)
    global VELOCITY_OFFSET
    VELOCITY_OFFSET[track-1] = v_offset

# Changes instrument of currently playing file on the specified track
# Can only be called after playback has started
def change_instrument(instrument, track):
    global PLAYER
    PLAYER.set_instrument(instrument, track);

# Sets tempo of the track. Only works before playback starts.
# Tempo is ratio of default speed:
# 1 is default speed, 0.5 is half speed, 2 is double speed, etc.
def set_tempo(tempo):
    global PARSER
    PARSER.ticks_per_beat = int(480 * tempo)


# Should not be called directly
def mplay():
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
