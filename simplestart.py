''' Just and easy way to start from the command line '''

from SimpleController import SimpleController
from ConsoleView import ConsoleView
from SuperConductorModel import SuperConductorModel

m = SuperConductorModel()
v = ConsoleView(m)
c = SimpleController(m)