''' Just and easy way to start from the command line '''

from sccui import Controller
from scm import Model
from scpv import PPPlayerView
import Leap, pygame, sys
import Tkinter, tkFileDialog, tkMessageBox

m = Model()

c = Controller()
lc = Leap.Controller()
c.setup(m, lc)
lc.add_listener(c)
p = PPPlayerView(m)

while True:
    # To exit cleanly, if controller thread has ended we need to end
    # player thread and this thread.
    if c.exited:
        p.exited = True
        exit()
    """
    if c.replay:
        c.replay = False
        p.play()
    """
    pass