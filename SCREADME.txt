Required:
    - Python 2.7
    - Pygame
    - Py-notify
    - enum34 0.9.23
    - LeapMotion
    - python-midi-master (custom)

To run:
    python superconductor.py

Description:
    SuperConductor allows a user to interact with midi files as they are being
    played, by dynamically changing volume, pitch, tempo, and midi instruments.
    These controls can either be applied to the entire song, or to individual tracks.
    
Use:
    When SuperConductor starts, a file selector will appear for the user to select a midi file.
    The user must select a file with a '.mid' extension.
    
    Once a file is selected, playback will begin.
    The main window displays the control values for the current track on the left, and all tracks on the right.
    
    Press A or D to select a track, or "All" to change all tracks. The current track appears in the left
    column on the "track" row
    
    Press W or S to select the current control. The current control will be highlighted.
    
    To change the value of a control, hold down the E key. When the E key is held, vertical motion over
    the LeapMotion will change the value of the control. 
    
    Controls can also be changed by using a left-right swipe gesture over the leap motion. This allows for
    more precision control. The E Key does not need to be held.
    
    Press the Spacebar to restore the current control to its default value.
    
    If the Pitch control is selected on All tracks, press and hold Q to use multi-control. In this mode,
    vertical motion over the Leap will constrol pitch, and horizontal motion will control tempo.
    
    When playback ends, press the spacebar to restart the song, or press Esc to exit.
    
    SuperConductor responds to control change events within MIDI files, so tempo and instruments may change without the user
    directly controlling them.
    
    Following the MIDI standard, track 10 is the percussion track. The percussion track has a special control
    called "Type" that changes the type of percussion.
    
    