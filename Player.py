# UW CSE 481 Sound Capstone
# Requires Mido and Pygame external libraries

# SuperConductor, basic MIDI file player and manipulator

from mido.midifiles import MidiFile
import pygame.midi
import threading

# Global Variables
VELOCITY_OFFSET = 0
PITCH_OFFSET = 0
FILE = None
PLAYER = None

# Non-blocking midi player.
def midistart(filename):
	global FILE
	FILE = filename
	playback_thread = threading.Thread(target=mplay)
	playback_thread.daemon = True
	playback_thread.start()

def pitch_offset(pitch):
	## TODO: Restrict to octaves? (multiples of 12)
	# Specify a track. (change PITCH_OFFSET to an array of pitch offsets for each track)
	# Validate input is within acceptable range
	# Offsetting by other values can make it sound bad, but might be more interesting
	global PITCH_OFFSET
	PITCH_OFFSET = pitch

def velocity_offset(volume):
	## TODO: Validate input is within acceptable range
	# Specify a track. (change VELOCITY_OFFSET to an array of pitch offsets for each track)
	global VELOCITY_OFFSET
	VELOCITY_OFFSET = volume

# Changes instrument of currently playing file on the specified track
def change_instrument(instrument, track):
	global PLAYER
	PLAYER.set_instrument(instrument, track);
	
def change_tempo(tempo):
	## TODO: Implement
	#  mid.ticks_per_beat = int(mid.ticks_per_beat * tempo)
	pass

# Should not be called directly
def mplay():
	global PLAYER
	pygame.midi.init()
	PLAYER = pygame.midi.Output(0)
	
	# Store notes currently being played, so we know what they were when we turn them off
	notes_in_progress = {}  
	mid = MidiFile(FILE)
	for message in mid.play():
		if message.type == "note_off" or (hasattr(message, 'velocity') and message.velocity == 0):
			key = (message.note, message.channel)
			PLAYER.note_off(notes_in_progress[key], message.velocity, message.channel)
		elif message.type == "note_on":
			key = (message.note, message.channel)
			notes_in_progress[key] = message.note+PITCH_OFFSET 
			PLAYER.note_on(notes_in_progress[key], message.velocity+VELOCITY_OFFSET, message.channel)
		elif message.type == "program_change":
			PLAYER.set_instrument(message.program, message.channel) 

	PLAYER.close()
