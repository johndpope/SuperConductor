Required:
    - Python 2.7
    - Pygame
    - Py-notify
    - enum34 0.9.23
    - LeapMotion
    - python-midi-master (custom)

To run:
    run superconductor.py

Controls:
    Keyboard:
        W, S to cycle current control
        A, D to cycle current track
        Spacebar to restore a control to its default value
        E, toggle leap motion
        Esc to quit
        
    LeapMotion:
        Swipe Left/Right, change value of current control
        Swipe Up/Down, cycle current control
        Vertical movement (when E key is pressed), quickly go through values of current control