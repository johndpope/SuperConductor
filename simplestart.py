''' Just and easy way to start from the command line '''

from scc import Controller
from scm import Model
from scpv import PPPlayerView
import Leap, pygame, sys

m = Model()
m.load_file('songs\miley_cyrus-wrecking_ball.mid')
c = Controller()
lc = Leap.Controller()
c.setup(m, lc)
lc.add_listener(c)
p = PPPlayerView(m)
p.play()

while True:
    pass


# pygame.init()
# screen = pygame.display.set_mode((640, 480))
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 print "quit"
#                 # user pressed ESC
#                 sys.exit()
#                 # Remove the sample listener when done
#                 # self.leap_controller.remove_listener(self)
#                 break
#             elif event.key == pygame.K_e:
#                 print "E key down"