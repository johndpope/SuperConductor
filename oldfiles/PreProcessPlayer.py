import mido
import pygame.midi
import midi
import time

def load_file(filename):
    pygame.midi.init()
    player = pygame.midi.Output(0)

    pattern = midi.read_midifile(filename)
    pattern.make_ticks_abs()
    events = []
    for track in pattern:
        for event in track:
            events.append(event)

    events.sort()
    delta = 0
    tickTime = 0
    secPerTick = .0005  # set it until we see a tempo event
    for event in events:
        delta = event.tick - tickTime
        tickTime = event.tick
        if delta:
            time.sleep(delta * secPerTick)
        if isinstance(event, midi.NoteOnEvent):
            player.note_on(event.pitch, event.velocity, event.channel)
        elif isinstance(event, midi.NoteOffEvent):
            player.note_off(event.pitch, event.velocity, event.channel)
        elif isinstance(event, midi.ProgramChangeEvent):
            player.set_instrument(event.value, event.channel)
        elif isinstance(event, midi.SetTempoEvent):
            # convert tempo to secPerTick
            mpb = 60.0 * 1000000.0 / event.bpm
            mpt = mpb / pattern.resolution
            secPerTick = mpt / 1000000.0

    player.close()

