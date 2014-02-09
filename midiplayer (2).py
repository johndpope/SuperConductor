# UW CSE 481 Sound Capstone
# Requires Mido and Pygame external libraries

# SuperConductor, basic MIDI file player and manipulator

from mido.midifiles import MidiFile
import pygame.midi
import threading

# Global Variables
VOLUME_OFFSET = 0
PITCH_OFFSET = 0
FILE = None
PLAYER = None
INIT = False

# Non-blocking midi player.
def midistart(filename):
	global FILE
	FILE = filename
	playback_thread = threading.Thread(target=mplay)
	playback_thread.daemon = True
	playback_thread.start()

def pitch_offset(pitch):
	global PITCH_OFFSET
	PITCH_OFFSET = pitch

def volume_offset(volume):
	global VOLUME_OFFSET
	VOLUME_OFFSET = volume

# Changes instrument of currently playing file on the specified track
def change_instrument(instrument, track):
	global PLAYER
	PLAYER.set_instrument(instrument, track);

# Should not be called directly
def mplay():
	global PLAYER, INIT
	# Prevent initialization from happening twice
	if not init:
	  pygame.midi.init()
	  PLAYER = pygame.midi.Output(0)
	  INIT = True
	
	# Store notes currently being played, so we know what they were when we turn them off
	notes_in_progress = {}  
	mid = MidiFile(FILE)
	for message in mid.play():
		if message.type == "note_on":
			key = (message.note, message.channel)
			notes_in_progress[key] = (message.note+PITCH_OFFSET, message.velocity+VOLUME_OFFSET) 
			PLAYER.note_on(notes_in_progress[key][0], notes_in_progress[key][1], message.channel)
			PLAYER.note_on(message.note, message.velocity, message.channel)
		elif message.type == "note_off":
			key = (message.note, message.channel)
			PLAYER.note_off(notes_in_progress[key][0], notes_in_progress[key][1], message.channel)
		else:
		  PLAYER.write(message)
#			del notes_in_progress[key]
