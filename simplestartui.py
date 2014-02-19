''' Just and easy way to start from the command line '''

from sccui import Controller
from scm import Model
from scpv import PPPlayerView
import Leap, pygame, sys

m = Model()
m.load_file('songs\lady_gaga-monster.mid')
c = Controller()
lc = Leap.Controller()
c.setup(m, lc)
lc.add_listener(c)
p = PPPlayerView(m)
p.play()

while True:
    pass