''' Just and easy way to start from the command line '''

from SimpleController import SimpleController
from ConsoleView import ConsoleView
from SuperConductorModel import SuperConductorModel
from PlayerView import PlayerView

m = SuperConductorModel()
p = PlayerView(m)
#v = ConsoleView(m)
#c = SimpleController(m)
