# enum support
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

Controls = enum("VOLUME", "PITCH", "TEMPO", "INSTRUMENT", "TRACK", "PLAY")
NUM_CONTROLS = 6
GLOBAL = 0
NUM_TRACKS = 16